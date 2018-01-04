# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages
from .models import UserAccount, Trip, Destination

def index(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
        return redirect('travel_buddy:index')
    if request.session['logged_in'] == True:
        return redirect('travel_buddy:travels')
    return render(request, "travel_buddy/index.html")

def register(request):
    if request.method == "GET":
        return redirect('travel_buddy:index')
    else:
        if UserAccount.objects.db_manager('travel_buddy').checkReg(request.POST, request):
            validReg = True
            return redirect('travel_buddy:travels')
        else:
            validReg = False
            return redirect('travel_buddy:index')

def login(request):
    if request.method == "GET":
        return redirect('travel_buddy:index')
    else:
        if UserAccount.objects.db_manager('travel_buddy').checkLog(request.POST, request):
            validLog = True
            request.session['logged_in'] = True
            return redirect('travel_buddy:travels')
        else:
            validLog = False
            return redirect('travel_buddy:index')

def travels(request):
    context = {
    'user_trips': Trip.objects.using('travel_buddy').filter(Q(planner__id=request.session['user']['id']) | Q(traveler__id=request.session['user']['id'])).order_by('departure_date'),
    'all_trips': Trip.objects.using('travel_buddy').exclude(traveler__id=request.session['user']['id']).exclude(planner__id=request.session['user']['id']).order_by('departure_date'),
    }
    return render(request, "travel_buddy/travels.html", context)

def addtrip(request):
    context = {
        'destinations': Destination.objects.using('travel_buddy').all().order_by('destination')
    }
    return render(request, "travel_buddy/addtrip.html", context)

def createtrip(request):
    if Trip.objects.db_manager('travel_buddy').checkTrip(request.POST, request):
        return redirect('travel_buddy:travels')
    else:
        return redirect('travel_buddy:addtrip')

def destination(request, id):
    context = {
    'users': UserAccount.objects.using('travel_buddy').all(),
    'destination_trips': Trip.objects.using('travel_buddy').filter(destination__id=id).order_by('departure_date'),
    'destinations': Destination.objects.using('travel_buddy').all()
    }
    return render(request, "travel_buddy/destination.html", context)

def join(request, id):
    Trip.objects.db_manager('travel_buddy').jointrip(request, id)
    return redirect('travel_buddy:travels')

def logout(request):
    request.session.clear()
    return redirect('travel_buddy:index')
