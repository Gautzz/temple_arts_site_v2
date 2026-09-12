# Temple Arts & Heritage

A community website about temple arts, rituals, and history, with:

- User accounts (register/login) via Flask-Login
- A blog people can write, edit, and delete (their own posts)
- A temple events calendar, where events can be tagged with a Gregorian
  date **and** a Malayalam calendar month/day/nakshatram (star)
- A small helper (`malayalam_calendar.py`) that suggests an **approximate**
  Malayalam date for a given Gregorian date, to speed up data entry

## Important note on the Malayalam calendar

Malayalam months begin on a solar event (when the sun enters a zodiac sign),
so the exact start date shifts by a day or two each year. Getting this
exactly right requires panchangam/astronomical data. This app therefore:

- auto-suggests an approximate Malayalam month/day when you pick a Gregorian
  date (good enough to save typing), and
- always lets the person adding the event manually edit the Malayalam month,
  day, and nakshatram before saving, so real event details (which usually
  come from the temple's own panchangam) stay accurate.

## Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app (creates the SQLite database automatically on first run)
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## Project structure

```
temple_arts_site/
├── app.py                  # Routes / application entry point
├── config.py                # App configuration
├── models.py                 # User, BlogPost, TempleEvent database models
├── forms.py                   # WTForms form definitions
├── malayalam_calendar.py       # Malayalam calendar helper + approximate conversion
├── requirements.txt
├── static/
│   └── css/style.css
└── templates/
    ├── base.html, index.html, login.html, register.html,
    ├── blogs.html, blog_detail.html, blog_form.html,
    └── events.html, event_form.html, error.html
```

## Making yourself an admin

Admins can edit/delete anyone's blog post or event. To promote a user,
open a Python shell after registering:

```bash
python
>>> from app import app
>>> from models import db, User
>>> with app.app_context():
...     u = User.query.filter_by(email="you@example.com").first()
...     u.is_admin = True
...     db.session.commit()
```

## Next steps / ideas to extend this

- Add image uploads for blog posts and events (temple photos)
- Add comments on blog posts
- Add a proper panchangam-based Malayalam calendar library for exact
  conversions instead of the approximate one included here
- Add search and pagination for blogs
- Deploy with a production server (e.g. Gunicorn + Nginx) and switch
  `SECRET_KEY` / database to production values via environment variables
