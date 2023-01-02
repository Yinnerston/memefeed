# Memefeed

Meme image and caption database store and viewer.

Why make a CRUD app? I have much more to learn in terms of system architecture, performance monitoring, and optimization.
I've also never implemented a caching server nor have I delved deeply into postgres optimization, so I want to gain some experience with these things whilst picking up Django.

Server is run on localhost port 8000.

# Agile Proposal, Notes & System Architecture

https://drive.google.com/drive/folders/10FNr-SX2xRIu2HvutmdhYNkCW2Mc2M3k?usp=sharing

# Jira

https://memefeed.atlassian.net/

# What I want to learn from this project

A more comprehensive summary will be updated on https://docs.google.com/document/d/16yKagWcxLBqN6zkW80W9SA_MnSaP6UQx528HsZB_KFo/edit?usp=sharing
- Load balancing with Traefic
- WSGI web servers
- Caching with Redis
- Postgres optimizations such as different joins, relationship types, full text search, indexing, JSONB
- Celery / RabbitMQ task queues for serving images
- Cron to pull data from reddit with PRAW
- Security: SQL injection attack, SSL / HTTPS, XSS protection
- Jinja2 templating
- Backend monitoring and observability using Solarwind + Django admin panel
- Configure Apache production server for deployment
