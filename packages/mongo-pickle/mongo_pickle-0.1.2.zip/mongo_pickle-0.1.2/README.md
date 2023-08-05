# mongo_pickle
Schema-less Pythonic Mongo ORM.

Designed to allow quick prototyping when developing and designing systems.

Exposes an interface to store and query generic python objects from and to Mongo databases without the need
to declare schemas when creating an initial DAL.

### Usage:

Assuming you have some business logic  that creates event data:


```
from mongo_pickle.collection import CollectionConfig
from mongo_pickle.model import Model

from datetime import datetime

class EventsConfig(CollectionConfig):
    host = 'sample.mlab.com'
    port = 27017

    database = 'database_name'
    collection = "events_v1"
    username = ''
    password = ''


class Event(Model):
    COLLECTION = EventsConfig.get_collection()

    def __init__(self, title, description, event_time):
        super(Event, self).__init__()
        self.title = title
        self.description = description
        self.event_time = event_time


if __name___ == '__main__':
    python_event = Event('cool event', 'code generated output', datetime.now())

    # Stored to your collection
    python_event.save()

    # Retrieve data
    all_events = Event.load_objects()

    # Supports mongo query filters
    all_events = Event.load_objects({'title': 'cool_event')

```

