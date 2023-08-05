from django.contrib import admin
from .models import NewsletterSubscription

class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    pass

admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)