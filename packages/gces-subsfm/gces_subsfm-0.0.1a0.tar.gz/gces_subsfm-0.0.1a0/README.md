# GCES Subscriber Framework

 * `listeners/collector/__init__.py`

 ```python
import logging
from gces import EventSubscriber


TOPIC_NAME = 'super_service_1.events'
SUBSCRIBER_NAME = 'collector'

def log_data(self, data):
    logger.info(data)

def subsetup_(config):
    es = EventSubscriber(TOPIC_NAME, SUBSCRIBER_NAME)
    es.register_fsub('LINK_ENABLE', log_data)
    es.register_fsub('LINK_DISABLE', log_data)

    config.register_subscriber(SUBSCRIBER_NAME, es)
 ```

 * `listeners/spammer/__init__.py`

 ```python
import logging
from gces import EventSubscriber


TOPIC_NAME = 'super_service_2.events'
SUBSCRIBER_NAME = 'spammer'

def log_data(self, data):
    logger.info(data)

def subsetup_(config):
    es = EventSubscriber(TOPIC_NAME, SUBSCRIBER_NAME)
    es.register_fsub('SPAM_DETECTED', log_data)
    es.register_fsub('SPAM_REGISTERED', log_data)

    config.register_subscriber(SUBSCRIBER_NAME, es)
 ```

 * `subscriber.py`

```python
import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel('INFO')

import signal, os
import importlib

from gces_subsfm import Configurator


def create_app():
    config = Configurator()
    config.include('listeners.collector')
    config.include('listeners.spammer')

    return config

app = application()

```

## Run Subscriber

```bash
$ gces-subsfm -A subscriber:app
```
