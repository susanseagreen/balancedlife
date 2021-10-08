

def get_fraction(meal_ingredients):

    for meal_ingredient in meal_ingredients:

        if '.' in str(meal_ingredient.measurement_value):
            num, dec = str(meal_ingredient.measurement_value).split('.')
            fraction = ''

            if dec != '00':
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
                    meal_ingredient.fraction = fraction
                else:
                    meal_ingredient.fraction = f"{num} {fraction}"

                meal_ingredient.measurement_value = 0
