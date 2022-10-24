from django.db import models
from users.models import CustomUser
from django.core.validators import MinValueValidator

class Tag(models.Model):
    name = models.CharField(
        verbose_name = 'Имя тега',
        max_length = 200,
    )
    color = models.CharField(
        verbose_name = 'Цвет',
        max_length = 7, 
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
    )
    
class Ingredient(models.Model):
    name = models.CharField(
        verbose_name = 'Имя ингредиента',
        max_length = 200,
    )
    measurement_unit = models.CharField(
        verbose_name = 'Единица измерения',
        max_length = 200,
    )


    class Meta:
        verbose_name = 'Ингредиент'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
    CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    pub_date = models.DateField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1, 'Значение не может быть меньше 1')],
        verbose_name='Время готовки в минутах',
    )
    description = models.TextField(null=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def str(self):
        return self.name
    

class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)],
        verbose_name='Количество ингредиентов'
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'


    def str(self):
        return f'{self.ingredient} {self.recipe}' 