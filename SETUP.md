# Setup

- (Git): For development, Install requirements in a venv and run `pre-commit install` to add black code auto-formatting on your commits
- Install postgres 13.9 with PGAdmin. This project assumes postgres runs on port 5432. (Default  for first time postgres installation).
- For postgres setup, I follow this tutorial: https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04
- In postgres shell:
```sql
CREATE DATABASE memefeed;
CREATE USER memefeeduser WITH PASSWORD 'PUT_YOU_PASSWORD_HERE';
ALTER ROLE memefeeduser SET client_encoding TO 'utf8';
ALTER ROLE memefeeduser SET default_transaction_isolation TO 'read committed';
ALTER ROLE memefeeduser SET timezone TO 'Australia/Sydney';
GRANT ALL PRIVILEGES ON DATABASE memefeed TO memefeeduser;
```
- Do the same for Database memefeed_prod with user memefeeduser_prod
Add the password to the .env file in root directory, `POSTGRES_PASSWORD=PUT_YOU_PASSWORD_HERE`. I would recommend generating a password with
```
openssl rand -hex 32
```
in another terminal.
- `docker-compose up -d --build`
- Run initial migration `docker-compose exec web python manage.py migrate --noinput`
- Check default Django tables were created `docker-compose exec db psql --username=memefeeduser --dbname=memefeed`
- Create a reddit web-app and personal use script in https://www.reddit.com/prefs/apps/
- Add praw.ini file to `src\memefeed`
```ini
[memefeedbot]
client_id=CLIENT_ID
client_secret=CLIENT_SECRET
password=YOUR_PASSWORD
username=YOUR_USERNAME
user_agent=Python-Slim:memefeed:v1.1.0 (by u/YOUR_USERNAME)

[memefeedscript]
client_id=SCRIPT_CLIENT_ID
client_secret=SCRIPT_CLIENT_SECRET
password=YOUR_PASSWORD
username=YOUR_USERNAME
user_agent=Python-Slim:memefeed-script:v1.1.0 (by u/YOUR_USERNAME)
```
- Change the list of subreddits if you want in `src\memefeed\reddit\data\subreddits.csv`
- Use black python code formatter

# Setup Grafana + Prometheus
- Install Docker plugin for Loki `docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions` in shell.
- Add a password `GF_SECURITY_ADMIN_PASSWORD=PASSWORD_HERE` to the `.env` file
- Go to localhost:3000
- Login to grafana (You added the password to the .env file)
- In your the grafana interface in your browser:
    - Go Configuration > Data Sources
    - Add data source > Pick Prometheus
    - Set URL as http://prometheus:9090
    - Save and Test
- Setup loki data source
    - Add data source > Pick Loki
    - Set URL as http://loki:3100
    - Save and Test
- Import the dashboards (*.json files) from the `data/grafana` directory
- (Unused) Define REDIS_USERNAME and REDIS_PASSWORD in .env file

# Production:
- See [#PROD.md](PROD.md) for deployment information

# ETL:
- For all the environment variables defined in the memefeed container, define them at the top of the etl script. E.G:
```bash
DEBUG=???
DATABASE_URL=???
POSTGRES_DBNAME=???
POSTGRES_USERNAME=???
POSTGRES_PASSWORD=???
DJ_LOGLEVEL=???
DJANGO_DEV_SECRET_KEY=???
```
- Run `git update-index --skip-worktree etl` to get git to stop tracking changes to the etl script