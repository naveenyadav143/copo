# CO-PO Calculator Django App

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Apply migrations:
   ```
   python manage.py migrate
   ```

3. Run locally:
   ```
   python manage.py runserver
   ```

## Deployment (Render)

- Set environment variables:
  - `DJANGO_SECRET_KEY`
  - `DJANGO_DEBUG` (set to `False` for production)
- Use `gunicorn` as the web service start command:
  ```
  gunicorn copos.wsgi
  ```
- Static files are served using WhiteNoise.

## Features

- User registration and login
- Add courses, COs, POs
- CO-PO mapping
- Upload student marks via Excel
- CO and PO attainment calculation

## Requirements

See `requirements.txt` for all dependencies.
