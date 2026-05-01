from flask import render_template, flash, redirect, url_for  # already partly imported
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

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
