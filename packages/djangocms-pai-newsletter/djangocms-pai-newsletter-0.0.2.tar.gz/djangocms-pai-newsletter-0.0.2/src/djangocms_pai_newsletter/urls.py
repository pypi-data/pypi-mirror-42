from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import NewsletterSubscriptionAPIView


urlpatterns = [
    url(r'^subscribe/$', NewsletterSubscriptionAPIView.as_view(), name="newsletter_subscribe"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
