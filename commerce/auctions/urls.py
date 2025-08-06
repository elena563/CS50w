from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:name>/", views.listing, name="listing"),
    path("create", views.create, name="create"),
    path("comment/<str:name>/", views.comment, name="comment"),
    path("bid/<str:name>/", views.bid, name="bid"),
    path("cancel/<str:name>/", views.cancel, name="cancel"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("wish/<str:name>/", views.wish, name="wish"),
    path("categories", views.categories, name="categories"),
    path('category/<str:cat>/', views.index, name='category'),
]
