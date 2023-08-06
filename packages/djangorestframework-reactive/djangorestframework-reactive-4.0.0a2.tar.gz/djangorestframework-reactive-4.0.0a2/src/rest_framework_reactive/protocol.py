# Channel used for notifying workers from ORM signals.
CHANNEL_WORKER_NOTIFY = 'rest_framework_reactive.worker'
# Channel used for scheduling polling of observers.
CHANNEL_POLL_OBSERVER = 'rest_framework_reactive.poll_observer'
# Channel used for notifying workers from ORM signals.
CHANNEL_THROTTLE = 'rest_framework_reactive.throttle'
# Group used for individual sessions.
GROUP_SESSIONS = 'rest_framework_reactive.session.{session_id}'

# Message type for ORM table change notifications.
TYPE_ORM_NOTIFY_TABLE = 'orm.notify_table'
# Message type for evaluating an observer.
TYPE_EVALUATE_OBSERVER = 'observer.evaluate'
# Message type for polling observable evaluation.
TYPE_POLL_OBSERVER = 'poll.observer'
# Message type for observer item updates.
TYPE_ITEM_UPDATE = 'observer.update'
# Message type for throttling observer evaluation.
TYPE_THROTTLE = 'delay.observer_evaluate'

ORM_NOTIFY_KIND_CREATE = 'create'
ORM_NOTIFY_KIND_UPDATE = 'update'
ORM_NOTIFY_KIND_DELETE = 'delete'
