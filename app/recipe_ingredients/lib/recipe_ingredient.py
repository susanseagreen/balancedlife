

def get_fraction(recipe_ingredients):

    for recipe_ingredient in recipe_ingredients:

        if '.' in str(recipe_ingredient.measurement_value):
            num, dec = str(recipe_ingredient.measurement_value).split('.')
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
                recipe_ingredient.fraction = fraction
            else:
                recipe_ingredient.fraction = f"{num} {fraction}"

            recipe_ingredient.measurement_value = 0
