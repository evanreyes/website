from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
from datetime import date, datetime
from dateutil.parser import parse
import re, bcrypt

email_reg = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def checkReg(self, postData, request):
        first_name = postData['first_name']
        last_name = postData['last_name']
        username = postData['username']
        email = 'travel' + postData['email']
        pw = postData['pw']
        pwc = postData['pw_confirm']
        validReg = True
        if len(first_name) < 3 or len(last_name) < 3:
            messages.warning(request, 'First and last name must be at least 3 characters long.')
            validReg = False
        if len(username) < 3:
            messages.warning(request, 'Username must be at least 3 characters long.')
            validReg = False
        if not email_reg.match(postData['email']):
            messages.warning(request, 'Please enter a valid email address.')
            validReg = False
        if len(pw) < 8:
            messages.warning(request, 'Password must be at least 8 characters.')
            validReg = False
        if pw != pwc:
            messages.warning(request, 'Passwords do not match.')
            validReg = False
        if UserAccount.objects.using('travel_buddy').filter(email=email):
            messages.warning(request, 'A user with that email address already exists.')
			validReg = False
        if validReg == True:
            pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            UserAccount.objects.db_manager('travel_buddy').create(first_name=first_name, last_name=last_name, username=username, email=email, password=pw_hash)
            pull_user = UserAccount.objects.using('travel_buddy').get(email=email)
            request.session['user'] = {
            'id': pull_user.id,
            'first_name': pull_user.first_name,
            'last_name': pull_user.last_name,
            'username': pull_user.username,
            'email': pull_user.email
            }
        return validReg

    def checkLog(self, postData, request):
        username = postData['username_login']
        pw = postData['pw_login']
        validLog = True
        pull_user = UserAccount.objects.using('travel_buddy').filter(username=username)
        if len(username) < 1 or len(pw) < 1:
            messages.warning(request, 'Username or password is incorrect.')
            validLog = False
        elif not pull_user:
            messages.warning(request, 'Username or password is incorrect.')
            validLog = False
        else:
            db_pw = UserAccount.objects.using('travel_buddy').get(username=username).password.encode()
            pw_hash = pw.encode()
            pull_user = UserAccount.objects.using('travel_buddy').get(username=username)
            if bcrypt.hashpw(pw_hash, db_pw) == db_pw:
                request.session['user'] = {
                'id': pull_user.id,
                'first_name': pull_user.first_name,
                'last_name': pull_user.last_name,
                'username': pull_user.username,
                'email': pull_user.email
                }
                validLog = True
            else:
                messages.warning(request, 'Username or password is incorrect.')
                validLog = False
        return validLog

class UserAccount(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Destination(models.Model):
    destination = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TripManager(models.Manager):
    def checkTrip(self, postData, request):
        user = UserAccount.objects.using('travel_buddy').get(id=request.session['user']['id'])
        destination_name = postData['destination_name']
        destination_list = postData['destination_list']
        description = postData['description']
        departure_date = postData['departure_date']
        return_date = postData['return_date']
        validTrip = True
        validDestination = True
        destination_check = Destination.objects.using('travel_buddy').filter(destination=destination_name)
        if len(description) < 3:
            messages.error(request, 'Please enter a description of your trip.')
            validTrip = False
        if departure_date:
            departure_date = parse(departure_date).date()
            if departure_date < date.today():
                messages.error(request, 'Departure date cannot be in the past.')
                validTrip = False
        if not departure_date:
            messages.error(request, 'Please choose a departure date.')
            validTrip = False

        if return_date:
            return_date = parse(return_date).date()
            if return_date < date.today():
                messages.error(request, 'Return date cannot be in the past.')
                validTrip = False
        if not return_date:
            messages.error(request, 'Please choose a return date.')
            validTrip = False

        if departure_date and return_date:
            if departure_date > return_date:
                messages.error(request, 'You cannot return before you have departed!')
                validTrip = False

        if destination_list == "select" and validTrip == True:
            if len(destination_name) < 1:
                messages.error(request, 'Please enter a destination.')
                validDestination = False
                return validDestination
            if destination_check:
                messages.error(request, 'That destination already exists.')
                validDestination = False
            else:
                validDestination = True
                destination = Destination.objects.db_manager('travel_buddy').create(destination=destination_name)

        if destination_list != "select" and validTrip == True:
            if len(destination_name) > 0:
                messages.error(request, 'Cannot select an existing destination and create a new destination simultaneously.')
                validDestination = False
                return validDestination
            else:
                validDestination = True
                destination = Destination.objects.using('travel_buddy').get(destination=destination_list)
        if validTrip == True and validDestination == True:
                Trip.objects.db_manager('travel_buddy').create(description=description, departure_date=departure_date, return_date=return_date, planner=user, destination=destination)
                messages.success(request, 'Thank you for adding a trip!')
        return validTrip

    def jointrip(self, request, id):
        user = UserAccount.objects.using('travel_buddy').get(id=request.session['user']['id'])
        trip = Trip.objects.using('travel_buddy').get(id=id)
        trip.traveler.add(user)

class Trip(models.Model):
    description = models.CharField(max_length=100)
    departure_date = models.DateField(auto_now=False)
    return_date = models.DateField(auto_now=False)
    planner = models.ForeignKey(UserAccount, related_name="user_planner", on_delete=models.CASCADE)
    traveler = models.ManyToManyField(UserAccount, related_name="user_traveler")
    destination = models.ForeignKey(Destination, related_name="trip_destination")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()
