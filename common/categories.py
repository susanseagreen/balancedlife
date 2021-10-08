from app.meals.models import Meal
from app.meal_categories.models import MealCategory


def meal_category():
    meals = Meal.objects.order_by('name')
    meal_categories = MealCategory.objects.order_by('name')

    meal_category_dict = {}

    for meal_category in meal_categories:
        meal_category_id = meal_category.id
        meal_category_dict[meal_category_id] = meal_category.name

    for meal in meals:
        categories_meal = []
        for category_meal in meal.categories_meal:
            categories_meal.append(category_meal)
        meal.categories_meal = categories_meal

    return meals
