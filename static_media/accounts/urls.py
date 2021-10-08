from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path('confirm', views.confirm, name='confirm'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('forgot_password', views.forgotPassword, name="forgot_password"),
    path('resetPasswordValidation/<uidb64>/<token>',
         views.resetPasswordValidation, name="resetPasswordValidation"),
    path('reset_password', views.resetPassword, name="resetPassword"),
    path('my_orders/', views.my_orders, name="my_orders"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('order_details/<int:order_id>',
         views.order_details, name="order_details"),
]
