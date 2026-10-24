from django.contrib import admin
from django.urls import path

from core.views import index, book_list, add_book, book_page, login, logout, mrsign

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book-list/', book_list),
    path('add-book/', add_book),
    path('book/<int:id>/', book_page),
    path('login/', login),
    path('logout/', logout, name='logout'),
    path('signup/', mrsign),
    path('', index),
]
