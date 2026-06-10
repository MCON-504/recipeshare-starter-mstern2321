from flask import render_template, flash, redirect, url_for  # already partly imported
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class RecipeForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=150)]
    )
    description = TextAreaField(
        "Description",
        validators=[DataRequired()]
    )
    instructions = TextAreaField(
        "Instructions",
        validators=[DataRequired()]
    )
    prep_time = IntegerField(
        "Prep Time (minutes)",
        validators=[DataRequired(), NumberRange(min=1)]
    )
    submit = SubmitField("Save Recipe")

 # FOR TEST

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class FeedbackForm(FlaskForm): # Create new class which extends FlaskForm
    name = StringField( # Put in fields
        "Name", # displayed as a label
        validators=[DataRequired(), Length(min=2, max=80)] # validators make it easy to check user's input
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)] # checks that it is a valid email
    )
    topic = StringField(
        "Topic",
        validators=[DataRequired(), Length(max=100)]
    )
    message = TextAreaField(
        "Message",
        validators=[DataRequired(), Length(min=10, max=500)]
    )
    submit = SubmitField("Send Feedback") # Submit button - give it text for button

class ProfileForm(FlaskForm):
    display_name = StringField(
        "Display Name",
        validators=[DataRequired(), Length(min=2, max=80)]
    )
    bio = TextAreaField(
        "bio",
        validators=[Optional(), Length(max=300)]
    )
    favorite_cuisine = StringField(
        "Favorite cuisine",
        validators = [Optional(), Length(max=80)]
    )
    years_cooking = IntegerField(
        "Years cooking",
        validators=[Optional(), NumberRange(min=0, max=100)]
    )
    submit = SubmitField("Save Profile")


class RecipeReviewForm(FlaskForm):
    rating = IntegerField(
        "Rating",
        validators=[DataRequired(), NumberRange(min=1, max=5)]
    )
    comment = TextAreaField(
        "Comment",
        validators=[DataRequired(), Length(min=5, max=300)]
    )
    submit = SubmitField("Submit Review")

