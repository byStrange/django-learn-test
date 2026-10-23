from django.contrib.auth.models import User
from django.contrib.auth import login as django_login
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.utils.translation.trans_real import re
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from main.models import Book

def check_auth(request):
    if request.user.is_authenticated == False:
        return redirect("/login/")


@csrf_exempt
def book_list(request: HttpRequest):
    if request.user.is_authenticated == False:
        return redirect("/login/")

    user_id = request.user.id
    # buyerdagi books bu constga o'xshagan o'zgarvuchi xolos
    books = Book.objects.filter(user_id=user_id).order_by("-id")

    if request.method == "GET":
        return render(request,"books-list.html", {"books": books})


@csrf_exempt
def add_book(request: HttpRequest):
    if request.user.is_authenticated == False:
            return redirect("/login/")

    if request.method == "GET":
        return render(request, "add_book.html")

    elif request.method == "POST":
        name1 = request.POST.get("name")
        muallif = request.POST.get("muallif")
        try:
            b1 = Book(name=name1, muallif=muallif, user_id=request.user.id)
            b1.save()
        except Exception as err:
            print(err)
            return HttpResponse('nimadir xato ketti bor konsolni tekshir qovun xato qilorasami!')

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

@csrf_exempt
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
        
            

    
