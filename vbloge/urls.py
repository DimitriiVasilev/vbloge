from django.urls import path
from django.conf.urls import include
from . import views


# app_name = 'vbloge'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:slug>/', views.show_category, name='show_category'),
    path('category/<slug:category_slug>/add_article', views.add_article, name='add_article'),
    path('category/<slug:category_slug>/<slug:article_slug>', views.show_article, name='show_article'),
    path('comment/<slug:category_slug>/<slug:article_slug>', views.add_comment, name='add_comment'),
    path('profile/', views.show_profile, name='profile'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]
