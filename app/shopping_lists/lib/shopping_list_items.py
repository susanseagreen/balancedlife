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
            'measurement_type',
            'measurement_value',
        ).order_by('code_ingredient__name')

    if shopping_list_items:

        for shopping_list_item in shopping_list_items:
            ingredient_id = shopping_list_item['code_ingredient_id']
            measurement_type = 'i'  # items

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
                ingredient_list[ingredient_id]['recipe_name'].append(shopping_list_item['code_recipe_ingredient__code_recipe__name'])

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
        if ingredient.get('i'):
            pass

        # weight
        if ingredient.get('kg'):
            if not ingredient.get('g'):
                ingredient['g'] = ingredient['kg'] * 1000
            else:
                ingredient['g'] = ingredient['g'] + (ingredient['kg'] * 1000)
            ingredient.pop('kg')

        if ingredient.get('g') and ingredient.get('g') >= 1000:
            ingredient['kg'] = ingredient['g'] / 1000
            ingredient.pop('g')

        if ingredient.get('l'):
            if not ingredient.get('c'):
                ingredient['c'] = ingredient['l'] * 4
            else:
                ingredient['c'] = ingredient['c'] + (ingredient['l'] * 4)
            ingredient.pop('l')

        if ingredient.get('c'):
            if not ingredient.get('tbsp'):
                ingredient['tbsp'] = ingredient['c'] * 16
            else:
                ingredient['tbsp'] = ingredient['tbsp'] + (ingredient['c'] * 16)
            ingredient.pop('c')

        if ingredient.get('tbsp'):
            if not ingredient.get('tsp'):
                ingredient['tsp'] = ingredient['tbsp'] * 3
            else:
                ingredient['tsp'] = ingredient['tsp'] + (ingredient['tbsp'] * 3)
            ingredient.pop('tbsp')

        if ingredient.get('tsp') and ingredient.get('tsp') >= 3:
            ingredient['tbsp'] = ingredient['tsp'] / 3
            ingredient.pop('tsp')

        if ingredient.get('tbsp') and ingredient.get('tbsp') >= 16:
            ingredient['c'] = ingredient['tbsp'] / 16
            ingredient.pop('tbsp')

        if ingredient.get('c') and ingredient.get('c') >= 4:
            ingredient['l'] = ingredient['c'] / 4
            ingredient.pop('c')

    return ingredient_list
