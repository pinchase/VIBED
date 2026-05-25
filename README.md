# Braymell Backend

This directory contains the Django application for the Braymell website. It powers the public pages, Django admin content management, uploaded media, and a small read-only API.

For the full project guide, see the root `README.md`.

## Quick Start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:

- Public site: `http://localhost:8000/`
- Admin: `http://localhost:8000/admin/`
- Swagger docs: `http://localhost:8000/api/docs/`
- ReDoc docs: `http://localhost:8000/api/redoc/`

## App Overview

The main app is `core`.

Primary content models:

- `Client`: company/client records with logos, captions, channel, and work story fields.
- `Brand`: brand records linked to clients.
- `BrandProgram`: program-level details for brand execution work.
- `BrandImage`: gallery images for brand detail pages.
- `Testimonial`: public testimonial content.
- `Project` and `ProjectImage`: legacy models retained in the codebase.

## Main Routes

| Route | Purpose |
| --- | --- |
| `/` | Homepage |
| `/clients/` | Client listing |
| `/clients/<slug>/` | Client detail page |
| `/brands/<slug>/` | Brand detail page |
| `/testimonials/` | Testimonial listing |
| `/about/` | About page |
| `/contact/` | Contact page |
| `/api/v1/testimonials/` | Testimonial API |
| `/api/docs/` | Swagger documentation |
| `/api/redoc/` | ReDoc documentation |

## Common Commands

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py collectstatic --no-input
```

## Deployment Files

- `Procfile` starts Gunicorn and runs migrations on release.
- `build.sh` installs dependencies, collects static files, and applies migrations.
- `.env.example` lists suggested production environment variables.

Before deploying publicly, review `config/settings.py`. It currently uses local defaults such as SQLite, `DEBUG = True`, and permissive allowed hosts.
