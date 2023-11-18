<p align="center">
    <img align="center" width="auto" height="auto" src="https://github.com/mad-hex0rzist-666/xxx_feed/assets/139306864/5ecb12e2-26c7-424a-b911-1fda706fe3b8">
</p>
<p align="center">
    <h3 align="center">BDSMLR Blogs Manager | NSFW 18 + </h3>
</p>

<br>

__Unofficial__ BDSMLR blog feed and django admin manager for managing content for pornographic websites, or
for collecting favorite bdsmlr blog posts.

> ⚠️ This application is not intended to be exposed publicly :warning:

### Features:

- Scrape the latest posts of one or multiple [:warning: BDSMLR](https://bdsmlr.com) (Don't click if you are not 18+) blogs.
- Manage bdsmlr blogs, manage by categories.
- Inspect images/gifs, download, etc.
- Migrate images/gifs to your own site for updating content on the regular and increase user engagement with daily new content.
- Track the status of the scrapes via the admin
- Check the status of the feed via the admin.
- Allows multiple bdsmlr credentials and management from manager admin -- for rotating multiple credentials.


### Configuration

Everything is built with `docker` and managed with `docker-compose` -- you could run everything and build manually, but the best way to build this is with docker.

#### Feed Configuration.

For the feed, check the `docker/feed/.env.example` 

| ENV Variable | Description |
| --- | --- |
| `USERNAME` | Your bdsmlr email (used to login) |
| `PASSWORD` | Your bdsmlr password (used to login) |

#### Manager Configuration

Add environment variables on `docker/manager/.env` check the `.env.example` in that same directory, if any doubts.

| ENV Variable | Description |
| --- | --- |
| `SECRET_KEY` | Your application secret key |
| `DB_NAME` | Database name (postgres db) |
| `DB_PASSWORD` | Postgres database password |
| `DB_USER` | Postgres database user |
| `XXX_SITE_ADMIN_API_KEY` | Key used to authenticate when making image migrations to your porn site. |
| `XXX_SITE_URL` | This is only used if you are migrating these images to you own porn site.and you have an api endpoint that can handle these migrations, there are admin actions that will allow you to select images and migrate them, but if you do not have a site to migrate them to, that action will fail |
| `XXX_SITE_TITLE` | Customize the admin title for the entire admin site. |
| `XXX_SITE_HEADER` | Customize the admin login page header/title. |
| `XXX_SITE_INDEX_TITLE`| Customize the welcome message for the admin, appears in the admin index page, upon login. |
| `API_AUTH` | You won't need this, but the app has a small not yet complete api for making a site out a this feed, this enables authentication on some endpoints, but the feed needs to authenticate when making requests so it needs modifying. |
|`JSON_WEB_TOKEN_AUTH` | Enable json web tokens for authentication, adds two endpoints which can be seen in the swagger api documentation `/api-docs`|

#### Database configuration.

For configuring the database check the `docker/database/.env.example` environment variables and make sure they match the database configuration for the `docker/manager/.env.example`

| ENV Variable | Description |
| --- | --- |
| `POSTGRES_USER` | The postgres database user -- same as `DB_USER` for the manager component |
| `POSTGRES_PASSWORD` | The postgres database password -- same as `DB_PASSWORD` for the manager component |
| `POSTGRES_DB` | The postgres database name -- same as the `DB_NAME` for the manager component |

---

### How to Run

`docker-compose up --detach` for running the app on the background
`docker-compose up` for running on the console.

### Usage Examples.

- Single task via manager.
    - Add blog
    - Check feed
    - Scrape blog
    - View images

https://github.com/mad-hex0rzist-666/xxx_feed/assets/139306864/70a6735a-3afc-4a3b-aaa0-b4ba41cf532d


### TO DO:

Add scheduled jobs via celery or apscheduler (lighter) and add a worker for them.
- Schedule scrapes per blog, and admin emails notifications for scrapes.
- Schedule automated migrations, and admin email notifications for migrations.
- Cleanup, backup, jobs, and admin email notifications for them.

