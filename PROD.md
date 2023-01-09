# Production Implementation:

- TODO: Migrate to cloud
- Lower traced_sample_rate in `sentry_sdk.init` https://docs.sentry.io/platforms/python/guides/django/performance/
- TODO: Production vs Dev database?
- Load balancing and cache server
- Loki and Django Debug Toolbar coinincide, as Django Debug Toolbar catches output to stdout before Loki can read it.
    - Disable Django Debug Toolbar in the `src\memefeed\memefeed\settings.py` file to query logs using Loki
