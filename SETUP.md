# Setup

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
Add the password to the .env file in root directory, `POSTGRES_PASSWORD=PUT_YOU_PASSWORD_HERE`. I would recommend generating a password with
```
openssl rand -hex 32
```
in another terminal.
- `docker-compose up -d --build`
- Run initial migration `docker-compose exec web python manage.py migrate --noinput`
- Check default Django tables were created `docker-compose exec db psql --username=memefeeduser --dbname=memefeed`
- Create a reddit app
- Add praw.ini file with format from reddit app
```ini
[memefeedbot]
client_id=CLIENT_ID
client_secret=CLIENT_SECRET
password=YOUR_PASSWORD
username=YOUR_USERNAME
user_agent=Alpine:memefeed:v1.0.0 (by u/YOUR_USERNAME)
```
- Change the list of subreddits if you want in `src\memefeed\reddit\data\subreddits.csv`