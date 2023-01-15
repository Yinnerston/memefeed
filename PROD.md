# Production Implementation:

- Build from docker-compose.prod.yml

- TODO: Migrate to cloud
- Lower traced_sample_rate in `sentry_sdk.init` https://docs.sentry.io/platforms/python/guides/django/performance/
- TODO: Production vs Dev database?
- Load balancing and cache server
- Loki and Django Debug Toolbar coinincide, as Django Debug Toolbar catches output to stdout before Loki can read it.
    - Disable Django Debug Toolbar in the `src\memefeed\memefeed\settings.py` file to query logs using Loki
- Define equivalent production env variables for docker-compose in the `.env` file:
```
PROD_POSTGRES_PASSWORD=???
PROD_DJANGO_DEV_SECRET_KEY=???
PROD_DJANGO_SUPERUSER_USERNAME=???
PROD_DJANGO_SUPERUSER_EMAIL=???
PROD_DJANGO_SUPERUSER_PASSWORD=???
PROD_GF_SECURITY_ADMIN_PASSWORD=???
PROD_REDIS_USERNAME=???
PROD_REDIS_PASSWORD=???
```