from rest_framework import serializers
from django.db import models

from django.utils import timezone

from skymarket.ads.models import Ad
from skymarket.skymarket import settings

NULLABLE = {'blank': True, 'null': True}


class CommentSerializer(serializers.ModelSerializer):
    title = models.CharField(max_length=200, verbose_name="название товара")
    price = models.PositiveIntegerField(verbose_name="цена")
    description = models.TextField(verbose_name="описание", max_length=500, **NULLABLE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ads", on_delete=models.CASCADE,
                               verbose_name="автор", **NULLABLE)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="время создания")
    image = models.ImageField(upload_to="ads/", verbose_name="Изображение", **NULLABLE)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "объявление"
        verbose_name_plural = "объявления"

    def __str__(self):
        return f'{self.title} - {self.price}'


class AdSerializer(serializers.ModelSerializer):
    text = models.TextField(verbose_name="текст отзыва")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE,
                               verbose_name="автор", **NULLABLE)
    ad = models.ForeignKey(Ad, related_name="reviews", on_delete=models.CASCADE, verbose_name="объявление")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="время создания")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"

    def __str__(self):
        return f"Отзыв от {self.author} для {self.ad}"


# class AdDetailSerializer(serializers.ModelSerializer):
#     # TODO сериалайзер для модели
#     pass
