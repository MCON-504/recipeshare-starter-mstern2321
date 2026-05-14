from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from .extensions import db
from .models import Recipe
from .forms import RecipeForm
from.forms import ProfileForm

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def api_home():
    return jsonify({"message": "RecipeShare API is running"})


@main_bp.route("/recipes", methods=["GET"])
def get_recipes():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    if request.is_json:
        return jsonify([recipe.to_dict() for recipe in recipes])
    return render_template("home.html", recipes=recipes)

@main_bp.route("/recipes/new", methods=["GET"])
@login_required
def get_new_recipe():

    return render_template("recipe_form.html", form=RecipeForm())


@main_bp.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.is_json:
        return jsonify(recipe.to_dict())
    return render_template("recipe_detail.html", recipe=recipe)


@main_bp.route("/recipes", methods=["GET", "POST"])
@login_required
def create_recipe():
    data = request.get_json() or {}
    if request.is_json:


        required_fields = ["title", "description", "instructions", "prep_time"]
        missing = [field for field in required_fields if field not in data]
        if missing:
            return {"error": f"Missing required fields: {', '.join(missing)}"}, 400

        recipe = Recipe(
            title=data["title"],
            description=data["description"],
            instructions=data["instructions"],
            prep_time=data["prep_time"],
            author=current_user,
        )

        db.session.add(recipe)
        db.session.commit()

        return jsonify(recipe.to_dict()), 201
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            instructions=form.instructions.data.strip(),
            prep_time=form.prep_time.data.strip(),
            author=current_user,
        )

        db.session.add(recipe)
        db.session.commit()
        flash("Recipe successfully created!")
        return redirect(url_for("main_bp.get_recipe(recipe.id)"))


@main_bp.route("/recipes/<int:recipe_id>", methods=["PATCH"])
@login_required
def update_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        return jsonify({"error": "forbidden"}), 403

    data = request.get_json() or {}
    updatable_fields = ["title", "description", "instructions", "prep_time"]
    for field in updatable_fields:
        if field in data:
            setattr(recipe, field, data[field])

    db.session.commit()
    return jsonify(recipe.to_dict()), 200


@main_bp.route("/recipes/<int:recipe_id>", methods=["DELETE"])
@login_required
def delete_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        return jsonify({"error": "forbidden"}), 403
    db.session.delete(recipe)
    db.session.commit()
    return "", 204

from flask import render_template, redirect, url_for, flash
from .forms import FeedbackForm


# FOR TEST

@main_bp.route("/feedback", methods=["GET", "POST"])
def feedback():
    form = FeedbackForm()

    if form.validate_on_submit(): # On post
        flash(f"Thanks, {form.name.data}! We received your feedback.", "success")
        return redirect(url_for("main_bp.feedback"))

    return render_template("feedback.html", form=form) # On get
"""
@main_bp.route("/profile", methods=["GET", "POST"])
def feedback():
    form = ProfileForm()

    if form.validate_on_submit():
        flash(f"Thanks, {form.display_name.data}! We received your profile.", "success")
        return redirect(url_for("main_bp.feedback"))

    return render_template("profiles.html", form=form) # On get

"""