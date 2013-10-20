# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from Data.models import *


def home(request):
    return render(request, 'home.html')
