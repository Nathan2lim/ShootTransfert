from shootX.models import *
from django.shortcuts import get_object_or_404, render,redirect
from django.conf import settings
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

import stripe
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    return render(request, 'shootX/home.html')
