# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import re, bcrypt

email_reg = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def checkReg(self, postData, request):
        first_name = postData['first_name']
        last_name = postData['last_name']
        email = postData['email']
        pw = postData['pw']
        pwc = postData['pw_confirm']
        validReg = True
        if len(first_name) < 2 or len(last_name) < 2:
            messages.warning(request, 'First and last name must be at least two characters long.')
            validReg = False
        if not email_reg.match(postData['email']):
            messages.warning(request, 'Please enter a valid email address.')
            validReg = False
        if len(pw) < 8:
            messages.warning(request, 'Password must be at least 6 characters.')
            validReg = False
        if pw != pwc:
            messages.warning(request, 'Passwords do not match.')
            validReg = False
        if UserAccount.objects.using('book_review').filter(email=email):
			messages.error(request, 'A user with that email address already exists.')
			validReg = False
        if validReg == True:
            pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            UserAccount.objects.db_manager('book_review').create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
            pull_user = UserAccount.objects.using('book_review').get(email=email)
            request.session['user'] = {
            'id': pull_user.id,
            'first_name': pull_user.first_name,
            'last_name': pull_user.last_name,
            'email': pull_user.last_name,
            }
        return validReg

    def checkLog(self, postData, request):
        email = postData['email_login']
        pw = postData['pw_login']
        validLog = True
        pull_user = UserAccount.objects.using('book_review').filter(email=email)
        if len(email) < 1 or len(pw) < 1:
            messages.warning(request, 'Username or password is incorrect.')
            validLog = False
        elif not pull_user:
            messages.warning(request, 'Username or password is incorrect.')
            validLog = False
        else:
            db_pw = UserAccount.objects.using('book_review').get(email=email).password.encode()
            pw_hash = pw.encode()
            pull_user = UserAccount.objects.using('book_review').get(email=email)
            if bcrypt.hashpw(pw_hash, db_pw) == db_pw:
                request.session['user'] = {
                'id': pull_user.id,
                'first_name': pull_user.first_name,
                'last_name': pull_user.last_name,
                'email': pull_user.last_name,
                }
                validLog = True
            else:
                messages.warning(request, 'Username or password is incorrect.')
                validLog = False
        return validLog

class UserAccount(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BookManager(models.Manager):
    def checkBook(self, postData, request):
        user = UserAccount.objects.using('book_review').get(id=request.session['user']['id'])
        title = postData['title']
        review = postData['review']
        rating = postData['rating']
        author_name = postData['author_name']
        author_list = postData['author_list']
        author_name_check = Author.objects.using('book_review').filter(name=author_name)
        validBook = True
        validAuthor = True
        if len(title) < 1:
            messages.error(request, 'Please enter a title.')
            validBook = False
        if Book.objects.using('book_review').filter(title=title):
            messages.error(request, 'That book already exists in the database.')
            validBook = False
        if len(review) < 1:
            messages.error(request, 'Please write a review.')
            validBook = False
        if rating == "select":
            messages.error(request, 'Please provide a rating.')
            validBook = False
        if author_list == "select" and validBook == True:
            if len(author_name) < 1:
                messages.error(request, 'Please choose or create an author.')
                validAuthor = False
                return validAuthor
            if author_name_check:
                messages.error(request, 'That author already exists in the database.')
                validAuthor = False
            else:
                validAuthor = True
                new_author = Author.objects.db_manager('book_review').create(name=author_name)
                author = Author.objects.using('book_review').get(name=author_name)
        if author_list != "select" and validBook == True:
            if len(author_name) > 0:
                messages.error(request, 'Cannot select an existing author and create a new author simultaneously.')
                validAuthor = False
                return validAuthor
            else:
                validAuthor = True
                author = Author.objects.using('book_review').get(name=author_list)
        if validBook == True and validAuthor == True:
                Book.objects.db_manager('book_review').create(title=title, author=author)
                book_add = Book.objects.using('book_review').get(title=title)
                Review.objects.db_manager('book_review').create(review=review, rating=rating, user=user, book=book_add)
                messages.success(request, 'Thank you for your review!')
        return validBook

    def newReview(self, postData, id, request):
        review = postData['review']
        rating = postData['rating']
        title = postData['title']
        validReview = True
        if len(review) == 0 or rating == "select":
            messages.error(request, 'Please provide a review and rating')
            validReview = False
        else:
            user = UserAccount.objects.using('book_review').get(id=request.session['user']['id'])
            book_add = Book.objects.using('book_review').get(title=title)
            Review.objects.db_manager('book_review').create(review=review, rating=rating, user=user, book=book_add)
            messages.success(request, 'Thank you for your review!')
        return validReview

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name="book_author")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BookManager()

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(UserAccount, related_name="review_user")
    book = models.ForeignKey(Book, related_name="review_book")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
