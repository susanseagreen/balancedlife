from app.shopping_list_items.models import ShoppingListItem


def build_shopping_list(self, ingredient_list):
    shopping_list_items = ShoppingListItem.objects \
        .filter(code_shopping_list_id=self.kwargs['pk']) \
        .values(
            'id',
            'added',
            'code_ingredient_id',
            'code_ingredient__name',
            'code_recipe_ingredient_id',
            'code_recipe_ingredient__code_recipe__name',
            'code_recipe_ingredient__code_recipe__servings',
            'code_recipe_ingredient__code_recipe__pax_serving',
            'measurement_type',
            'measurement_value',
            'day_of_week',
            'meal'
        ).order_by('code_ingredient__name')

    if shopping_list_items:

        for shopping_list_item in shopping_list_items:
            ingredient_id = shopping_list_item['code_ingredient_id']
            measurement_type = 'i'  # items

            if ',' in shopping_list_item['day_of_week']:
                shopping_list_item['day_of_week'] = shopping_list_item['day_of_week'].split(',')

            if ',' in shopping_list_item['meal']:
                shopping_list_item['meal'] = shopping_list_item['meal'].split(',')

            if shopping_list_item['measurement_type']:
                measurement_type = shopping_list_item['measurement_type']

            if ingredient_id not in ingredient_list:
                ingredient_list[ingredient_id] = {
                    'id': shopping_list_item['id'],
                    'ingredient_id': shopping_list_item['code_ingredient_id'],
                    'ingredient_name': shopping_list_item['code_ingredient__name'],
                    'recipe_ingredient_id': shopping_list_item['code_recipe_ingredient_id'],
                    'recipe_name': [],
                    'added': [],
                    'removed': [],
                    measurement_type: 0
                }
                ingredient_list[ingredient_id]['recipe_name'].append(
                    shopping_list_item['code_recipe_ingredient__code_recipe__name'])

            shopping_list_item['servings'] = \
                f"{shopping_list_item['code_recipe_ingredient__code_recipe__pax_serving']} pax for " + \
                f"{shopping_list_item['code_recipe_ingredient__code_recipe__servings']} servings"

            if shopping_list_item['added']:
                if measurement_type in ingredient_list[ingredient_id]:
                    ingredient_list[ingredient_id][measurement_type] = \
                        ingredient_list[ingredient_id][measurement_type] + \
                        (shopping_list_item['measurement_value'] or 0)
                else:
                    ingredient_list[ingredient_id][measurement_type] = \
                        (shopping_list_item['measurement_value'] or 0)

                ingredient_list[ingredient_id]['added'].append(shopping_list_item)
            else:
                ingredient_list[ingredient_id]['removed'].append(shopping_list_item)

    build_measurements(ingredient_list)

    return ingredient_list


def build_measurements(ingredient_list):
    for ingredient_id, ingredient in ingredient_list.items():

        convert_check(ingredient, 'kg', 'g', 1000)
        convert_check(ingredient, 'l', 'c', 4)
        convert_check(ingredient, 'c', 'tbsp', 16)
        convert_check(ingredient, 'tbsp', 'tsp', 3)
        convert_check(ingredient, 'tsp', 'ml', 5)

    for ingredient_id, ingredient in ingredient_list.items():
        convert_up(ingredient, 'tsp', 'ml', 5)
        convert_up(ingredient, 'tbsp', 'tsp', 3)
        convert_up(ingredient, 'c', 'tbsp', 16)
        convert_up(ingredient, 'l', 'c', 4)
        convert_up(ingredient, 'kg', 'g', 1000)

    for ingredient_id, ingredient in ingredient_list.items():
        get_fraction(ingredient, 'i')
        get_fraction(ingredient, 'tsp')
        get_fraction(ingredient, 'tbsp')
        get_fraction(ingredient, 'c')
        get_fraction(ingredient, 'ml')
        get_fraction(ingredient, 'l')
        get_fraction(ingredient, 'g')
        get_fraction(ingredient, 'kg')

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
        ingredient[bigger] = round(ingredient[smaller]/diff, 2)
        ingredient.pop(smaller)


def get_fraction(ingredient, value):

    if '.' in str(ingredient[value]):
        num, dec = str(ingredient[value]).split('.')
        fraction = ''
        if dec == '.25':
            fraction = '1/4'
        if dec == '.5':
            fraction = '1/2'
        if dec == '.75':
            fraction = '3/4'
        if '.3' <= dec <= '0.34':
            fraction = '1/3'
        if '.6' <= dec <= '0.67':
            fraction = '2/3'

        if num == '0':
            ingredient['fraction'] = fraction
        else:
            ingredient['fraction'] = f"{num} {fraction}"

        ingredient.pop(value)
