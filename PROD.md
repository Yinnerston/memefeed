# Production Implementation:

- Build from docker-compose.prod.yml
- Comment out the line `path("reddit/", include("reddit.urls")),` in `src\memefeed\memefeed\urls.py` + save the file. Otherwise the migration in the next line will not work
- Run `docker-compose -f docker-compose.prod.yml exec memefeed python manage.py migrate --noinput`
- Uncomment the line `path("reddit/", include("reddit.urls")),`. 
- Can populate the Submissions with the command `docker-compose -f docker-compose.prod.yml exec memefeed bash` --> Execute `python manage.py shell < scripts/fast_populate_reddit_etl.py` in bash shell and `python manage.py collectstatic`
- If you've opened the site, use `python manage.py clear_cache` in the bash shell
- traced_sample_rate is lowered in `sentry_sdk.init` https://docs.sentry.io/platforms/python/guides/django/performance/
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
PROD_IP=??? # IP of your server
```
- Note that the production containers should not be run on a computer that is already using postgres/13. Otherwise, because a postgres_data volume is used, the volume can overwrite the existing postgres data on your computer. This includes the development containers.

# HTTPS:
- Replace memefeed.xyz with your server_name in `./data/nginx/nginx.conf` and `init-letsencrypt.sh`
- run ./init-letsencrypt.sh 

# Running Production:
- docker-compose -f docker-compose.prod.yml build
- ./init-letsencrypt.sh 
- docker-compose -f docker-compose.prod.yml up -d

# Stopping Production
- docker-compose -f docker-compose.prod.yml down --remove-orphans
- If down is not working: run `sudo systemctl daemon-reload` then `sudo systemctl restart docker`

# Selenium Touch Cache:
- Because the traffic on my site is too low and caches are timing out, use the script `src/memefeed/scripts/touch_memefeed.py` to 
- Run the python script in a venv with selenium (can use the `src/memefeed/requirements.txt`)
- Download a Chrome driver that matches your chrome version and add it to PATH https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
- Start `chromedriver`
- [Linux]: Schedule it with cron to run every X minutes
- [Windows]: Install pyinstaller `pip install pyinstaller`. Run `pyinstaller --onefile src/memefeed/scripts/touch_memefeed.py`. Add `dist/touch_memefeed.exe` to Task Scheduler to run every X minutes.