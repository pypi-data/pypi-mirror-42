import functools
import json
import datetime
import logging

import six
from six.moves import filter

import redis
import sseclient
from django.conf import settings

from vr.events import Sender


class EventSender(Sender):

    def publish(self, message, event=None, tags=None, title=None, **kw):
        # Make an object with timestamp, ID, and payload
        data = {
            'time': datetime.datetime.utcnow().isoformat(),
            'message': message,
            'tags': tags or [],
            'title': title or '',
        }

        # Used for optional keys such as the swarm id, trace id, etc.
        data.update(kw)

        payload = json.dumps(data)
        # Serialize it and stick it on the pubsub
        super(EventSender, self).publish(payload, event=event)

    def close(self):
        self.rcon.connection_pool.disconnect()


class ProcListener(six.Iterator):
    def __init__(self, rcon_or_url, channel):
        if isinstance(rcon_or_url, redis.StrictRedis):
            self.rcon = rcon_or_url
        elif isinstance(rcon_or_url, six.string_types):
            self.rcon = redis.StrictRedis.from_url(rcon_or_url)
        self.channel = channel
        self.pubsub = self.rcon.pubsub()
        self.pubsub.subscribe([channel])

        self.rcon.publish(channel, 'flush')

    def __iter__(self):
        return self

    def __next__(self):
        def is_message(msg):
            return msg['type'] == 'message'
        messages = filter(is_message, self.pubsub.listen())
        msg = next(messages)
        data = msg['data'].decode('utf-8')
        if data == 'flush':
            return ':\n'

        ev = sseclient.Event(data=data, retry=1000)
        return ev.dump()

    def close(self):
        self.rcon.connection_pool.disconnect()


def eventify(user, action, obj, detail=None, **kw):
    """
    Save a message to the user action log, application log, and events pubsub
    all at once.
    """
    fragment = '%s %s' % (action, obj)
    from vr.server import models  # Imported late to avoid circularity
    logentry = models.DeploymentLogEntry(
        type=action,
        user=user,
        message=fragment
    )
    logentry.save()
    # Also log it to actual python logging
    message = '%s: %s' % (user.username, fragment)
    logging.info(message)

    # put a message on the pubsub
    sender = EventSender(
        settings.EVENTS_PUBSUB_URL,
        settings.EVENTS_PUBSUB_CHANNEL,
        settings.EVENTS_BUFFER_KEY)
    tags = ['user', action]
    if 'tags' in kw:
        tags += kw['tags']
        del kw['tags']
    sender.publish(
        detail or message, tags=tags, title=message, **kw)
    sender.close()


def eventify_on_error(action):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(request, *args, **kwargs):
            try:
                return f(request, *args, **kwargs)
            except Exception as e:
                eventify(request.user, action, obj='',
                         detail=str(e), tags=['failed'])
                raise

        return wrapper
    return decorator
