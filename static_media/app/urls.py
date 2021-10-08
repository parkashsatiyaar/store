from django.views.generic import RedirectView
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('products/', views.products, name='products'),
    path('products/<name>', views.singleProduct, name='product'),
    path('contact-us/', views.contact, name='contact'),
    path('about-us/', views.about, name='about'),
    path('category/<category>', views.category, name='categories'),
    path('category', views.category, name='categories'),
]
