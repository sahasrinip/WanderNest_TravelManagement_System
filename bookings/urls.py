from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account, name='account'),
    path('profile/', views.profile, name='profile'),
    path('list_travel/', views.list_travel_options, name='list_travel_options'),
    path('book_travel/<int:travel_id>/', views.book_travel, name='book_travel'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
