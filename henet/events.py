# encoding: utf8
from collections import defaultdict
from bottle_utils.i18n import lazy_gettext as _


_SUBSCRIBERS = defaultdict(list)

ALL_EVENTS = -1
EVENT_CHANGED_CONTENT = 0
EVENT_DELETED_CONTENT = 1
EVENT_CREATED_CONTENT = 2
EVENT_CREATED_COMMENT = 3
EVENT_START_BUILDING = 4
EVENT_ALREADY_BUILDING = 5
EVENT_BUILT = 5


def event2str(event):
    if event == EVENT_CHANGED_CONTENT:
        return _('Content changed.')
    elif event == EVENT_DELETED_CONTENT:
        return _('Content deleted.')
    elif event == EVENT_CREATED_CONTENT:
        return _('Content created')
    elif event == EVENT_START_BUILDING:
        return _('Update started.')
    elif event == EVENT_BUILT:
        return _('Update finished.')
    elif event == EVENT_ALREADY_BUILDING:
        return _('Update already in progress.')
    return event


def subscribe(event, callback):
    _SUBSCRIBERS[event].append(callback)


def emit(event, **data):
    for subscriber in _SUBSCRIBERS[event]:
        subscriber(event, **data)
    for subscriber in _SUBSCRIBERS[ALL_EVENTS]:
        subscriber(event, **data)
