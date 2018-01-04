# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.contrib import messages
from .models import UserAccount, Book, Author, Review

def index(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
        return redirect('book_review:index')
    if request.session['logged_in'] == True:
        return redirect('book_review:books')
    return render(request, "book_review/index.html")

def register(request):
    if request.method == "GET":
        return redirect('book_review:index')
    else:
        if UserAccount.objects.db_manager('book_review').checkReg(request.POST, request):
            validReg = True
            return redirect('book_review:books')
        else:
            validReg = False
            return redirect('book_review:index')

def login(request):
    if request.method == "GET":
        return redirect('book_review:index')
    else:
        if UserAccount.objects.db_manager('book_review').checkLog(request.POST, request):
            validLog = True
            request.session['logged_in'] = True
            return redirect('book_review:books')
        else:
            validLog = False
            return redirect('book_review:index')

def books(request):
    context = {
    'books': Book.objects.using('book_review').all().order_by('title'),
    'authors': Author.objects.using('book_review').all(),
    'reviews': Review.objects.using('book_review').all().order_by('-created_at')
    }
    return render(request, "book_review/books.html", context)

def newbook(request):
    context = {
        'authors': Author.objects.using('book_review').all()
    }
    return render(request, "book_review/newbook.html", context)

def createbook(request):
    Book.objects.db_manager('book_review').checkBook(request.POST, request)
    return redirect('book_review:newbook')

def bookinfo(request, id):
    context = {
    'books': Book.objects.using('book_review').get(id=id),
    'reviews': Review.objects.using('book_review').filter(book__id=id).order_by('-created_at')
    }
    return render(request, "book_review/bookinfo.html", context)


def userprofile(request, id):
    context = {
    'books': Book.objects.using('book_review').all(),
    'users': UserAccount.objects.using('book_review').filter(id=id),
    'user_reviews': Review.objects.using('book_review').filter(user__id=id).count(),
    'reviews': Review.objects.using('book_review').filter(user__id=id)
    }
    return render(request, "book_review/userprofile.html", context)

def newreview(request, id):
    Book.objects.db_manager('book_review').newReview(request.POST, id, request)
    return redirect('book_review:bookinfo', id=id)

def deletereview(request, id):
    Review.objects.using('book_review').filter(id=id).delete()
    return redirect('book_review:books')

def logout(request):
    request.session.clear()
    return redirect('book_review:index')
