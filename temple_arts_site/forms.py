from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange
from malayalam_calendar import MALAYALAM_MONTHS, NAKSHATRAS


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    category = SelectField(
        "Category",
        choices=[
            ("Temple Arts", "Temple Arts"),
            ("Rituals", "Rituals"),
            ("History", "History"),
            ("Music & Dance", "Music & Dance"),
            ("Architecture", "Architecture"),
            ("General", "General"),
        ],
    )
    content = TextAreaField("Content", validators=[DataRequired()])


class TempleEventForm(FlaskForm):
    temple_name = StringField("Temple Name", validators=[DataRequired(), Length(max=200)])
    title = StringField("Event Title", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[Optional()])
    gregorian_date = DateField("Gregorian Date", validators=[DataRequired()], format="%Y-%m-%d")
    malayalam_month = SelectField("Malayalam Month", choices=[(m, m) for m in MALAYALAM_MONTHS], validators=[Optional()])
    malayalam_day = IntegerField("Malayalam Day", validators=[Optional(), NumberRange(min=1, max=32)])
    nakshatram = SelectField("Nakshatram (Star)", choices=[("", "-- None --")] + [(n, n) for n in NAKSHATRAS], validators=[Optional()])
    location = StringField("Location", validators=[Optional(), Length(max=200)])
