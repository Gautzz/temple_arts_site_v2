from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from malayalam_calendar import MALAYALAM_MONTHS, NAKSHATRAS


class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    author_name = StringField("Your Name", validators=[Optional(), Length(max=120)])
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
    author_name = StringField("Your Name", validators=[Optional(), Length(max=120)])
    description = TextAreaField("Description", validators=[Optional()])
    gregorian_date = DateField("Start Date", validators=[DataRequired()], format="%Y-%m-%d")
    end_date = DateField("End Date (optional, for multi-day events)", validators=[Optional()], format="%Y-%m-%d")
    malayalam_month = SelectField("Malayalam Month", choices=[(m, m) for m in MALAYALAM_MONTHS], validators=[Optional()])
    malayalam_day = IntegerField("Malayalam Day", validators=[Optional(), NumberRange(min=1, max=32)])
    nakshatram = SelectField("Nakshatram (Star)", choices=[("", "-- None --")] + [(n, n) for n in NAKSHATRAS], validators=[Optional()])
    location = StringField("Location", validators=[Optional(), Length(max=200)])
