from django.core import validators
from django_filters import rest_framework as filters
from django.db import models
from rest_framework import serializers


class Validators:
    product_name = [
        validators.MinLengthValidator(1, message="Минимум 1 символ"),
        validators.MaxLengthValidator(100, message="Максимум 100 символов"),
    ]
    catalog_name = product_name
    about = [
        validators.MaxLengthValidator(2048, message="Максимум 2048 символов"),
    ]
    description = about
    initials = [
        validators.MinLengthValidator(5, message="Минимум 5 символов"),
        validators.MaxLengthValidator(100, message="Максимум 100 символов"),
    ]
    age = [
        validators.MinValueValidator(18, message="Минимальный возраст 18"),
        validators.MaxValueValidator(120, message="Максимальное возраст 120")
    ]
    experience_year = [
        validators.MinValueValidator(0, message="Минимальный опыт 0"),
        validators.MaxValueValidator(100, message="Максимальный опыт 100")
    ]
    contact = [
        validators.MinLengthValidator(10, message="Минимально 10 символов"),
        validators.MaxLengthValidator(15, message="Максимально 15 символов"),
    ]

    @staticmethod
    def validate_no_profanity(value):
        profane_words = ['мат1', 'мат2', 'мат3']
        suggestion_words = ['Слово1', 'Слово2', 'Слово3']

        for word in profane_words:
            if word in value.lower():
                raise serializers.ValidationError(
                    {
                        'error': f'Текст содержит запрещенное слово: {word}, вы можете выбрать одно из этих слов',
                        'possible_words': suggestion_words
                    },
                    code=400
                )


class Employee(models.Model):
    initials = models.CharField(verbose_name='Имя и фамилия',
                                validators=Validators.initials + [Validators.validate_no_profanity], max_length=100)
    about = models.TextField(verbose_name='Обо мне', validators=Validators.about + [Validators.validate_no_profanity],
                             blank=True, null=True)
    age = models.IntegerField(validators=Validators.age, verbose_name='Возраст')
    experience_year = models.IntegerField(verbose_name='Опыт работы', validators=Validators.experience_year, default=0)
    contact = models.CharField(verbose_name='Номер телефона',
                               validators=Validators.contact + [Validators.validate_no_profanity], max_length=15,
                               unique=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['initials']
        db_table = 'employee'

    def __str__(self):
        return self.initials


class Catalog(models.Model):
    name = models.CharField(verbose_name='Название каталога', max_length=100,
                            validators=Validators.catalog_name + [Validators.validate_no_profanity])
    employee = models.ForeignKey(to='Employee', verbose_name='Владелец каталога', related_name='catalog',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'
        ordering = ['name']
        db_table = 'catalog'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Название продукта', max_length=100,
                            validators=Validators.product_name + [Validators.validate_no_profanity])
    description = models.TextField(
        verbose_name='Описание продукта', blank=True, null=True,
        validators=Validators.description + [Validators.validate_no_profanity]
    )
    price = models.IntegerField(verbose_name='Цена продукта')
    duration = models.DurationField(verbose_name='Продолжительность работы')
    catalog = models.ForeignKey(to='Catalog', verbose_name='Каталог продукта', related_name='product',
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']
        db_table = 'product'

    def __str__(self):
        return self.name


class ProductFilters(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte', label='Минимальная цена продукта')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte', label='Максимальная цена продукта')
    name = filters.CharFilter(field_name="name", lookup_expr='icontains', label='Название продукта')
    catalog_name = filters.CharFilter(field_name='catalog__name', lookup_expr='icontains', label='Название каталога')
    employee_experience_year = filters.NumberFilter(field_name="catalog__employee__experience_year", lookup_expr='gte',
                                                    label='Опыт работника от')
    employee_age = filters.NumberFilter(field_name="catalog__employee__age", lookup_expr='gte',
                                        label='Возраст работника от')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'name', 'employee_experience_year', 'employee_age']
