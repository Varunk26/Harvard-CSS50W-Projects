from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("listingpage/<int:listing_id>", views.listingpage, name="listingpage"),
    path("addwatchlist/<int:listing_id>", views.addwatchlist, name="addwatchlist"),
    path("removewatchlist/<int:listing_id>", views.removewatchlist, name="removewatchlist"),
    path("placebid/<int:listing_id>", views.placebid, name="placebid"),
    path("closeauction/<int:listing_id>", views.closeauction, name="closeauction") 
]

