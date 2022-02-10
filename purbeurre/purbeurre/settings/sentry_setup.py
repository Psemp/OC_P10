import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.django import DjangoIntegration


sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.INFO  # Send infos and above as events
)

sentry_sdk.init(
    dsn="https://d63bd79d8cf14c9e9aa592f4633bca77@o916582.ingest.sentry.io/5858313",
    integrations=[DjangoIntegration(), sentry_logging],

    traces_sample_rate=1.0,

    send_default_pii=True
)
