from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories", views.categories, name='categories'),
    path("watchlist", views.watchlist, name='watchlist'),
    path('category/<slug:cat_slug>', views.show_category, name='show_category'),
]
