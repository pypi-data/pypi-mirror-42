from django.shortcuts import render
from django.views.generic.edit import View
from django.contrib import messages
from django.shortcuts import redirect
from django.core.validators import validate_email
from django import forms
from django.utils.translation import ugettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import NewsletterSubscription


class NewsletterSubscriptionView(View):
    model = NewsletterSubscription
    fields = ['email']
    
    def get(self, request):
        try:
            email = request.GET.get("email", "")
            if email == "":
                raise forms.ValidationError(_('Email not valid'))
            validate_email(email)
        except forms.ValidationError:
            messages.add_message(request, messages.ERROR, _('Email not valid'))
        else:
            try:
                n, new = NewsletterSubscription.objects.get_or_create(email=request.GET.get("email"))
                if new:
                    messages.add_message(request, messages.INFO, _('Succesfully subscribed {}').format(request.GET.get('email')))
                else:
                    messages.add_message(request, messages.INFO, _('Already subscribed.'))
            except:
                messages.add_message(request, messages.ERROR, _('Error'))
                
        return redirect('/')


class NewsletterSubscriptionAPIView(APIView):
    model = NewsletterSubscription
    fields = ['email']
    
    def get(self, request):
        try:
            email = request.GET.get("email", None)
            if email is None:
                raise forms.ValidationError(_('Email not valid'))
            validate_email(email)
        except forms.ValidationError:
            messages.add_message(request, messages.ERROR, _('Email not valid'))
        else:
            try:
                n, new = NewsletterSubscription.objects.get_or_create(email=request.GET.get("email"))
                if new:
                    messages.add_message(request, messages.INFO, _('Succesfully subscribed {}').format(request.GET.get('email')))
                else:
                    messages.add_message(request, messages.INFO, _('Already subscribed.'))
            except:
                messages.add_message(request, messages.ERROR, _('Error'))
                
        return redirect('/')


class NewsletterSubscriptionAPIView(APIView):
    """
    Creates a newsletter subscription for given email
    """

    def post(self, request, format=None):
        email = request.GET.get("email", None)
        
        if email is None:
            return Response(_('Email not present in GET params'), status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                validate_email(email)
            except forms.ValidationError:
                return Response(_('Email not valid'), status=status.HTTP_400_BAD_REQUEST)

        subscription, created = NewsletterSubscription.objects.get_or_create(email=email)
        if created:
            return Response(_('Succesfully subscribed'), status=status.HTTP_201_CREATED)
        else:
            return Response(_("Already subscribed."), status=status.HTTP_400_BAD_REQUEST)

