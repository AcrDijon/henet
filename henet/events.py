# encoding: utf8
from collections import defaultdict

_SUBSCRIBERS = defaultdict(list)

ALL_EVENTS = -1
EVENT_CHANGED_CONTENT = 0
EVENT_DELETED_CONTENT = 1
EVENT_CREATED_CONTENT = 2
EVENT_CREATED_COMMENT = 3


def event2str(event):
    if event == EVENT_CHANGED_CONTENT:
        return 'Contenu modifié'
    elif event == EVENT_DELETED_CONTENT:
        return 'Contenu supprimé'
    elif event == EVENT_CREATED_CONTENT:
        return 'Contenu créé'
    return ''


def subscribe(event, callback):
    _SUBSCRIBERS[event].append(callback)


def emit(event, **data):
    for subscriber in _SUBSCRIBERS[event]:
        subscriber(event, **data)
    for subscriber in _SUBSCRIBERS[ALL_EVENTS]:
        subscriber(event, **data)
