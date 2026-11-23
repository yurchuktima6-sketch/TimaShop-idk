from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL (slug)")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Категорія")
    title = models.CharField(max_length=200, verbose_name="Назва гри")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL (slug)")
    description = models.TextField(blank=True, verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    stock = models.PositiveIntegerField(default=0, verbose_name="Кількість на складі (ключі/диски)")
    available = models.BooleanField(default=True, verbose_name="В наявності")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name = "Гра (Товар)"
        verbose_name_plural = "Ігри (Товари)"
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['title']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name="Гра")
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name="Зображення")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортування")

    class Meta:
        verbose_name = "Зображення гри"
        verbose_name_plural = "Зображення ігор"
        ordering = ['order']

    def __str__(self):
        return f"Зображення для {self.product.title}"