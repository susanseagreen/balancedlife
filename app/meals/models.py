from django.db import models
from PIL import Image


class Meal(models.Model):
    name = models.CharField(max_length=50)
    image_link = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(default='default.png', blank=True)
    servings = models.IntegerField(default=1, blank=True, null=True)
    pax_serving = models.IntegerField("Pax per serving", default=2, blank=True, null=True)
    meal_category = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, null=True, blank=True)
    steps = models.TextField('Cooking Instructions', max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.pax_serving} pax / {self.servings} serving)"

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save()  # saving image first

        try:
            img = Image.open(self.image.path) # Open image using self

            if img.height > 300 or img.width > 300:
                new_img = (300, 300)
                img.thumbnail(new_img)
                img.save(self.image.path)  # saving image at the same path

        except FileNotFoundError:
            pass

        return super(Meal, self).save(*args, **kwargs)
