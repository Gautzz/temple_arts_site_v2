from datetime import date
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)

from config import Config
from models import db, User, BlogPost, TempleEvent
from forms import RegisterForm, LoginForm, BlogPostForm, TempleEventForm
from malayalam_calendar import approximate_malayalam_date

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------- Public pages ----------

@app.route("/")
def index():
    upcoming_events = (
        TempleEvent.query.filter(TempleEvent.gregorian_date >= date.today())
        .order_by(TempleEvent.gregorian_date.asc())
        .limit(5)
        .all()
    )
    latest_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(5).all()
    return render_template("index.html", events=upcoming_events, posts=latest_posts)


# ---------- Auth ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("An account with that email already exists.", "danger")
            return render_template("register.html", form=form)
        user = User(name=form.name.data, email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# ---------- Blogs ----------

@app.route("/blogs")
def blogs():
    category = request.args.get("category")
    query = BlogPost.query
    if category:
        query = query.filter_by(category=category)
    posts = query.order_by(BlogPost.created_at.desc()).all()
    return render_template("blogs.html", posts=posts, selected_category=category)


@app.route("/blogs/<int:post_id>")
def blog_detail(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template("blog_detail.html", post=post)


@app.route("/blogs/new", methods=["GET", "POST"])
@login_required
def blog_new():
    form = BlogPostForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            user_id=current_user.id,
        )
        db.session.add(post)
        db.session.commit()
        flash("Blog post published.", "success")
        return redirect(url_for("blog_detail", post_id=post.id))
    return render_template("blog_form.html", form=form, mode="new")


@app.route("/blogs/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def blog_edit(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    form = BlogPostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        db.session.commit()
        flash("Blog post updated.", "success")
        return redirect(url_for("blog_detail", post_id=post.id))
    return render_template("blog_form.html", form=form, mode="edit", post=post)


@app.route("/blogs/<int:post_id>/delete", methods=["POST"])
@login_required
def blog_delete(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Blog post deleted.", "info")
    return redirect(url_for("blogs"))


# ---------- Temple Events ----------

@app.route("/events")
def events():
    all_events = TempleEvent.query.order_by(TempleEvent.gregorian_date.asc()).all()
    return render_template("events.html", events=all_events)


@app.route("/calendar")
def malayalam_calendar_page():
    from malayalam_calendar import MALAYALAM_MONTHS, _APPROX_START
    today = date.today()
    today_month, today_day = approximate_malayalam_date(today)
    month_rows = list(zip(MALAYALAM_MONTHS, _APPROX_START))
    return render_template(
        "calendar.html",
        month_rows=month_rows,
        today=today,
        today_month=today_month,
        today_day=today_day,
    )


@app.route("/events/new", methods=["GET", "POST"])
@login_required
def event_new():
    form = TempleEventForm()
    suggestion = None
    if request.method == "GET" and request.args.get("date"):
        try:
            d = date.fromisoformat(request.args.get("date"))
            m_name, m_day = approximate_malayalam_date(d)
            suggestion = f"{m_name} {m_day} (approximate)"
        except ValueError:
            pass
    if form.validate_on_submit():
        event = TempleEvent(
            temple_name=form.temple_name.data,
            title=form.title.data,
            description=form.description.data,
            gregorian_date=form.gregorian_date.data,
            malayalam_month=form.malayalam_month.data,
            malayalam_day=form.malayalam_day.data,
            nakshatram=form.nakshatram.data or None,
            location=form.location.data,
            user_id=current_user.id,
        )
        db.session.add(event)
        db.session.commit()
        flash("Temple event added.", "success")
        return redirect(url_for("events"))
    return render_template("event_form.html", form=form, mode="new", suggestion=suggestion)


@app.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def event_edit(event_id):
    event = TempleEvent.query.get_or_404(event_id)
    if event.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    form = TempleEventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        event.nakshatram = form.nakshatram.data or None
        db.session.commit()
        flash("Temple event updated.", "success")
        return redirect(url_for("events"))
    return render_template("event_form.html", form=form, mode="edit", event=event, suggestion=None)


@app.route("/events/<int:event_id>/delete", methods=["POST"])
@login_required
def event_delete(event_id):
    event = TempleEvent.query.get_or_404(event_id)
    if event.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash("Temple event deleted.", "info")
    return redirect(url_for("events"))


# ---------- API helper: convert a Gregorian date to approx Malayalam date ----------

@app.route("/api/malayalam-date")
def api_malayalam_date():
    from flask import jsonify
    date_str = request.args.get("date")
    try:
        d = date.fromisoformat(date_str)
    except (TypeError, ValueError):
        return jsonify({"error": "invalid date"}), 400
    month, day = approximate_malayalam_date(d)
    return jsonify({"month": month, "day": day})


@app.errorhandler(403)
def forbidden(e):
    return render_template("error.html", code=403, message="You don't have permission to do that."), 403


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404, message="Page not found."), 404


def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
