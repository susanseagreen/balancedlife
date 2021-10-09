from app.meals.models import Meal
from app.meal_categories.models import MealCategory


def build_meal_category_dict():

    meal_categories = MealCategory.objects.order_by('name')

    meal_category_dict = {}

    for meal_category in meal_categories:
        meal_category_dict[str(meal_category.id)] = meal_category.name

    return meal_category_dict
