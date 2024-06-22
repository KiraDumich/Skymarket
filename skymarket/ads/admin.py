from django.contrib import admin

from skymarket.ads.models import Ad, Comment

admin.site.register(Ad, Comment)

