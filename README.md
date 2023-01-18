# http://memefeed.xyz

Meme image and caption database store and viewer. I wanted to create a database for reddit posts which allowed for more robust search capabilities. I also want to experiment with implementing multiple UIs and practice iterative development where I can rapidly innovate on this project based on user feedback. 

Why make a CRUD app? I have much more to learn in terms of system architecture, performance monitoring, and optimization.
I've also never implemented a caching server nor have I delved deeply into postgres optimization, so I want to gain some experience with these things whilst picking up Django.

I am self-hosting the docker containers. It is deployed at http://memefeed.xyz . I plan on providing support for this project throughout 2023 and gain experience in commiting to a project over an extended period of time (>1 year).

# Agile Proposal, Notes & System Architecture

https://drive.google.com/drive/folders/10FNr-SX2xRIu2HvutmdhYNkCW2Mc2M3k?usp=sharing

The project is built with Django, cached with Redis and uses the python PRAW api wrapper for reddit to get submissions daily. 
Logging is implemented through prometheus, which collects metrics from Django, the redis caching layer and system information with the docker containers. Sentry is used to store captured exceptions for debugging.


# Jira

https://memefeed.atlassian.net/

I am using Jira to monitor the Agile sprints, user stories and epics.

# What I want to learn from this project

A more comprehensive summary will be updated on https://docs.google.com/document/d/16yKagWcxLBqN6zkW80W9SA_MnSaP6UQx528HsZB_KFo/edit?usp=sharing
- Load balancing with Nginx production server for deployment
- gunicorn WSGI web server
- Caching with Redis
- Monitoring suite using Prometheus + Grafana dashboarding, Grafana Loki
- Postgres optimizations such as different joins, relationship types, full text search, indexing, JSONB
- Celery / RabbitMQ task queues for serving images
- Cron to pull data from reddit with PRAW
- Security: SQL injection attack, SSL / HTTPS, XSS protection.
- Django templating
- Backend monitoring and observability using Solarwind + Django admin panel
- General front-end dev.

# Setup:
- Follow instructions in [setup.md](SETUP.md)
- `docker-compose build`
- `docker-compose up -d`

# Deploying the project
- Follow instructions in [PROD.md](PROD.md)
- `docker-compose -f docker-compose.prod.yml build`
- `docker-compose -f docker-compose.prod.yml up -d`

# What are my long term goals with this project?
- I want to reimplement the frontend designs of popular social media sites like TikTok, Reddit and Imgur.
- I want to learn to scale my project up from one computer to a networked cluster

# What will not be in this project?
- I will most likely not be migrating to the cloud because I like managing my own database instance.
