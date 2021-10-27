from app.shopping_list_items.models import ShoppingListItem
from common import categories


def build_diary(food_diary):
    for x in range(0, 8):
        food_diary[str(x)] = {}
        for y in range(0, 6):
            food_diary[str(x)][str(y)] = []

    return


def build_food_diary(self, food_diary):
    shopping_list_items = ShoppingListItem.objects \
        .filter(code_shopping_list_id=self.kwargs['pk'], added=True) \
        .values(
        'id',
        'name',
        'code_ingredient_id',
        'code_ingredient__name',
        'code_meal_ingredient__code_meal_id',
        'code_meal_ingredient__code_meal__name',
        'day_of_week',
        'meal'
    ).order_by('id')

    if shopping_list_items:

        for shopping_list_item in shopping_list_items:

            if not shopping_list_item['name']:

                name = shopping_list_item['code_meal_ingredient__code_meal__name'] or \
                       shopping_list_item['code_ingredient__name']

                if ',' in shopping_list_item['day_of_week']:
                    shopping_list_item['day_of_week'] = shopping_list_item['day_of_week'].split(',')

                if ',' in shopping_list_item['meal']:
                    shopping_list_item['meal'] = shopping_list_item['meal'].split(',')

                if shopping_list_item['day_of_week']:
                    for day_of_week in shopping_list_item['day_of_week']:

                        if shopping_list_item['meal']:
                            for meal in shopping_list_item['meal']:
                                if name not in food_diary[day_of_week][meal]:
                                    food_diary[day_of_week][meal].append(name)
                        else:
                            if name not in food_diary[day_of_week]['0']:
                                food_diary[day_of_week]['0'].append(name)
                else:
                    if shopping_list_item['meal']:
                        for meal in shopping_list_item['meal']:
                            if name not in food_diary['0'][meal]:
                                food_diary['0'][meal].append(name)
                    else:
                        if name not in food_diary['0']['0']:
                            food_diary['0']['0'].append(name)

    return food_diary


def build_shopping_list(self, ingredient_list):
    shopping_list_items = ShoppingListItem.objects \
        .filter(code_shopping_list_id=self.kwargs['pk']) \
        .values(
            'id',
            'added',
            'name',
            'code_ingredient_id',
            'code_ingredient__name',
            'code_ingredient__code_category__name',
            'code_meal_ingredient_id',
            'code_meal_ingredient__code_meal__meal_category',
            'code_meal_ingredient__code_meal_id',
            'code_meal_ingredient__code_meal__name',
            'code_meal_ingredient__code_meal__servings',
            'code_meal_ingredient__code_meal__pax_serving',
            'measurement_type',
            'measurement_value',
            'day_of_week',
            'meal',
            'quantity'
        ).order_by('code_ingredient__code_category__name', 'code_ingredient__name')

    meal_category_dict = categories.build_meal_category_dict()

    if shopping_list_items:

        for shopping_list_item in shopping_list_items:

            meal_categories = []
            measurement_type = 'i'  # items
            ingredient_id = None

            shopping_list_item['quantity'] = float(shopping_list_item['quantity'])
            if shopping_list_item['measurement_value']:
                shopping_list_item['measurement_value'] = float(shopping_list_item['measurement_value'])

            if shopping_list_item['measurement_value'] and shopping_list_item['quantity']:
                shopping_list_item['measurement_value'] = float(
                    shopping_list_item['measurement_value'] * shopping_list_item['quantity'])

            if shopping_list_item['code_ingredient_id']:
                ingredient_id = shopping_list_item['code_ingredient_id']

            if shopping_list_item['name']:
                ingredient_id = shopping_list_item['name'].replace(' ', '').lower()

            if shopping_list_item['day_of_week']:
                if ',' in shopping_list_item['day_of_week']:
                    shopping_list_item['day_of_week'] = shopping_list_item['day_of_week'].split(',')

            if shopping_list_item['code_meal_ingredient__code_meal__meal_category']:
                if ',' in shopping_list_item['code_meal_ingredient__code_meal__meal_category']:
                    shopping_list_item['code_meal_ingredient__code_meal__meal_category'] = shopping_list_item[
                        'code_meal_ingredient__code_meal__meal_category'].split(',')

                for code in shopping_list_item['code_meal_ingredient__code_meal__meal_category']:
                    meal_categories.append(meal_category_dict[code])
                shopping_list_item['meal_categories'] = meal_categories
            else:
                shopping_list_item['meal_categories'] = ""

            if shopping_list_item['meal']:
                if ',' in shopping_list_item['meal']:
                    shopping_list_item['meal'] = shopping_list_item['meal'].split(',')

            if shopping_list_item['measurement_type']:
                measurement_type = shopping_list_item['measurement_type']

            if ingredient_id not in ingredient_list:
                ingredient_list[ingredient_id] = {
                    'id': shopping_list_item['id'],
                    'name': shopping_list_item['name'],
                    'ingredient_id': shopping_list_item['code_ingredient_id'],
                    'ingredient_name': shopping_list_item['code_ingredient__name'],
                    'ingredient_category': shopping_list_item['code_ingredient__code_category__name'],
                    'meal_categories': shopping_list_item['meal_categories'],
                    'meal_ingredient_id': shopping_list_item['code_meal_ingredient_id'],
                    'day_of_week': shopping_list_item['day_of_week'],
                    'meal': shopping_list_item['meal'],
                    'quantity': shopping_list_item['quantity'],
                    'meal_names': [],
                    'added': [],
                    'removed': [],
                    'measurement_type': {},
                }
                if shopping_list_item['code_meal_ingredient__code_meal__name']:
                    ingredient_list[ingredient_id]['meal_names'].append(
                        shopping_list_item['code_meal_ingredient__code_meal__name'])

            if shopping_list_item['code_meal_ingredient__code_meal__pax_serving']:
                shopping_list_item['servings'] = \
                    f"{shopping_list_item['code_meal_ingredient__code_meal__pax_serving']} pax for " + \
                    f"{shopping_list_item['code_meal_ingredient__code_meal__servings']} servings"

            if shopping_list_item['added']:

                if measurement_type in ingredient_list[ingredient_id]['measurement_type']:
                    ingredient_list[ingredient_id]['measurement_type'][measurement_type] = \
                        ingredient_list[ingredient_id]['measurement_type'][measurement_type] + \
                        (shopping_list_item['measurement_value'] or 0)
                else:
                    ingredient_list[ingredient_id]['measurement_type'][measurement_type] = \
                        (shopping_list_item['measurement_value'] or 0)

                ingredient_list[ingredient_id]['added'].append(shopping_list_item)
            else:
                ingredient_list[ingredient_id]['removed'].append(shopping_list_item)

    build_measurements(ingredient_list)

    return ingredient_list


def build_measurements(ingredient_list):
    for ingredient_id, ingredient in ingredient_list.items():
        convert_check(ingredient['measurement_type'], 'kg', 'g', 1000)
        convert_check(ingredient['measurement_type'], 'l', 'c', 4)
        convert_check(ingredient['measurement_type'], 'c', 'tbsp', 16)
        convert_check(ingredient['measurement_type'], 'tbsp', 'tsp', 3)
        convert_check(ingredient['measurement_type'], 'tsp', 'ml', 5)

    for ingredient_id, ingredient in ingredient_list.items():
        convert_up(ingredient['measurement_type'], 'tsp', 'ml', 5)
        convert_up(ingredient['measurement_type'], 'tbsp', 'tsp', 3)
        convert_up(ingredient['measurement_type'], 'c', 'tbsp', 16)
        convert_up(ingredient['measurement_type'], 'l', 'ml', 1000)
        convert_up(ingredient['measurement_type'], 'c', 'ml', 250)
        convert_up(ingredient['measurement_type'], 'kg', 'c', 4)
        convert_up(ingredient['measurement_type'], 'kg', 'g', 1000)
        convert_up(ingredient['measurement_type'], 'c', 'g', 250)

    for ingredient_id, ingredient in ingredient_list.items():
        get_fraction(ingredient['measurement_type'], 'i')
        get_fraction(ingredient['measurement_type'], 'tsp')
        get_fraction(ingredient['measurement_type'], 'tbsp')
        get_fraction(ingredient['measurement_type'], 'c')
        get_fraction(ingredient['measurement_type'], 'ml')
        get_fraction(ingredient['measurement_type'], 'l')
        get_fraction(ingredient['measurement_type'], 'g')
        get_fraction(ingredient['measurement_type'], 'kg')

    return ingredient_list


def convert_check(ingredient, bigger, smaller, diff):
    if ingredient.get(bigger):
        if not ingredient.get(smaller):
            ingredient[smaller] = round(ingredient[bigger] * diff, 2)
        else:
            ingredient[smaller] = round(ingredient[smaller] + (ingredient[bigger] * diff), 2)
        ingredient.pop(bigger)


def convert_up(ingredient, bigger, smaller, diff):
    if ingredient.get(smaller) and ingredient.get(smaller) >= diff:
        ingredient[bigger] = round(ingredient[smaller] / diff, 2)
        ingredient.pop(smaller)


def get_fraction(ingredient, value):
    if value in ingredient and '.' in str(ingredient[value]):
        num, dec = str(ingredient[value]).split('.')
        fraction = ''
        if dec == '25':
            fraction = '1/4'
        if dec == '50':
            fraction = '1/2'
        if dec == '75':
            fraction = '3/4'
        if '3' in dec:
            fraction = '1/3'
        if '6' in dec:
            fraction = '2/3'

        if num == '0':
            ingredient['fraction'] = fraction
        else:
            ingredient['fraction'] = f"{num} {fraction}"

        ingredient['measurement_type'] = value
        ingredient.pop(value)


def build_summary(self, ingredient_list):

    ingredient_summary = {}

    for ingredient in ingredient_list.values():
        ingredient_category = ingredient['ingredient_category']

        if ingredient['added']:
            if ingredient_category not in ingredient_summary:
                ingredient_summary[ingredient_category] = []

            ingredient_summary[ingredient_category].append({
                'id': ingredient['id'],
                'name': ingredient['name'],
                'ingredient_id': ingredient['ingredient_id'],
                'ingredient_name': ingredient['ingredient_name'],
                'ingredient_category': ingredient['ingredient_category'],
                'meal_categories': ingredient['meal_categories'],
                'meal_ingredient_id': ingredient['meal_ingredient_id'],
                'measurement_type': ingredient['measurement_type'],
            })

    return ingredient_summary
