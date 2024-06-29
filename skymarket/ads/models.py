from django.conf import settings
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Ad(models.Model):
    """Модель для объявления"""
    image = models.ImageField(
        upload_to="images/",
        verbose_name="фото",
        help_text="Разместите фото для объявления",
        **NULLABLE,
    )

    title = models.CharField(
        max_length=200,
        verbose_name="Название товара",
        help_text="введите название товара",
    )

    price = models.PositiveIntegerField(
        verbose_name="Цена товара", help_text="Добавьте цену товара"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор объявления",
        help_text="Выберите автора объявления",
        default='Anonymous',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания объявления",
        help_text="Введите время создания объявления",
    )

    description = models.CharField(
        max_length=1000,
        verbose_name="Описание товара",
        help_text="Введите описание товара",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ("-created_at",)  # сначала самые свежие


class Comment(models.Model):
    """Модель для комментариев под объявлениями"""
    text = models.CharField(
        max_length=1000,
        verbose_name="Комментарий",
        help_text="Оставьте свой комментарий здесь",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания комментария",
        help_text="Введите время создания комментария",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
        help_text="Выберите автора комментария",
    )
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Объявление",
        help_text="Объявление, к которому относится комментарий",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-created_at",)  # сначала самые свежие
