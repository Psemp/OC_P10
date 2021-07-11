import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://d63bd79d8cf14c9e9aa592f4633bca77@o916582.ingest.sentry.io/5858313",
    integrations=[DjangoIntegration()],

    traces_sample_rate=1.0,

    send_default_pii=True

)
