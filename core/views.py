from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.utils.translation.trans_real import re
from django.contrib import messages

from main.models import Book

def index(request):
    """Bosh sahifa – loyihaning kirish sahifasi."""
    if request.user.is_authenticated:
        return redirect("/book-list/") 
    return redirect("/login/")

def check_auth(request):
    if request.user.is_authenticated == False:
        return redirect("/login/")

def book_list(request: HttpRequest):
    if request.user.is_authenticated == False:
        return redirect("/login/")

    user_id = request.user.id
    books = Book.objects.filter(user_id=user_id).order_by("-id")

    if request.method == "GET":
        return render(request,"books-list.html", {"books": books})


def add_book(request: HttpRequest):
    if request.user.is_authenticated == False:
            return redirect("/login/")

    if request.method == "GET":
        return render(request, "add_book.html")

    elif request.method == "POST":
        name1 = request.POST.get("name")
        muallif = request.POST.get("muallif")
        url = request.POST.get("url")

        try:
            b1 = Book(name=name1, muallif=muallif, user_id=request.user.id, url=url)
            b1.save()
        except Exception as err:
            print(err)
            return HttpResponse('nimadir xato ketti bor konsolni tekshir qovun miyya xato qilorasami!')

        return redirect("/book-list/")

    return HttpResponse("hozircha ishlamayapti")

def book_page(request, id):
    if request.user.is_authenticated == False:
        return redirect("/login/")

    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse('kitob topilmadi')

    return render(request, "book.html", {"book": book})


def login(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("/book-list/")

    if  request.method == "GET":
        return render(request, "login.html")
        
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Kechirasiz kiritilgan ma'lumotlar xato!")
            return redirect("/login/")
        
        if  user.check_password(password):
            django_login(request, user)
            return redirect('/book-list/')
        else:
            messages.error(request, "Kechirasiz kiritilgan ma'lumotlar xato!")
            return redirect("/login/")

def mrsign(request: HttpRequest):
    if request.user.is_authenticated:
       return redirect("/book-list/")

    if request.method == "GET":
       return render(request, "signup.html")

    if request.method == "POST":
       username = request.POST.get('username')
       password = request.POST.get('password')
       password_confirm = request.POST.get('password_confirm_ui')
       if  password != password_confirm:
            messages.error(request, "Parolllar mos emas!")
            return redirect('/signup/')

       try:
           User.objects.get(username=username)
           messages.error(request, "Bu user allaqachon mavjud!")
           return redirect("/signup/")
       except User.DoesNotExist:
           user = User(username=username)
           user.set_password(password)
           user.save()
           django_login(request, user)
           return redirect('/book-list/')

def logout(request):
    django_logout(request)
    return redirect('/login/')
