from django.db import models
from django.contrib.auth.models import User # импортируем авторизацию


class Section(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.CharField(null=True, blank=True, max_length=80, verbose_name='Название на английском (для ссылки)')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Стоимость')
    slug = models.CharField(max_length=80, verbose_name='Алиас')

    section = models.ForeignKey('Section', on_delete=models.CASCADE, verbose_name='Раздел')
    reviews = models.ManyToManyField('Review', related_name='Product', verbose_name='Отзывы', through='ReviewProductRelation')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=50, verbose_name='Заголовок')
    text = models.TextField(max_length=250, default='', verbose_name='Текст')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    products = models.ManyToManyField('Product', related_name='Article', verbose_name='Товары')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return str(self.name)


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    rating = models.PositiveIntegerField(verbose_name='Оценка')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    author = models.CharField(max_length=50, null=True, blank=True, verbose_name='Автор')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return str(self.author) + '(' + str(self.product.name) + ')' + ': ' + self.text[:50]


class ReviewProductRelation(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    review = models.ForeignKey('Review', on_delete=models.CASCADE, verbose_name='Отзыв')

    class Meta:
        verbose_name = 'Отзыв-Товар'
        verbose_name_plural = 'Отзывы-Товары'

    def __str__(self):
        return self.review


class Order(models.Model):
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Автор')
    products = models.ManyToManyField('Product', related_name='Order', verbose_name='Товары', through='OrderProductRelation')
    total = models.PositiveIntegerField(verbose_name='Общая стоимость заказа')
    complete = models.BooleanField(default=False, verbose_name='Завершен')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProductRelation(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    amount = models.PositiveIntegerField(verbose_name='Количество')
    total = models.PositiveIntegerField(verbose_name='Сумма')

    class Meta:
        verbose_name = 'Заказ-Товар'
        verbose_name_plural = 'Заказ-Товар'

    def __str__(self):
        return str(self.order) + ' ' + str(self.product.name)
