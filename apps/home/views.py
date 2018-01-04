from django.shortcuts import render, redirect, HttpResponse

def index(request):
    return render(request, 'home/index.html')

def home(request):
    return redirect('/')

def about(request):
    return render(request, 'home/about.html')

def projects(request):
    return render(request, 'home/projects.html')

def blog(request):
    return render(request, 'home/blog.html')
