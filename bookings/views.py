from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import TravelOption, Booking
from django.contrib import messages
from .forms import BookingForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def account(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Your profile has been updated!')
        return redirect('profile')

    return render(request, 'acc.html', {'user': request.user})

@login_required
def view_bookings(request):
    search_query = request.GET.get('search', '')
    
    # Filter bookings for the logged-in user
    if search_query:
        bookings = Booking.objects.filter(
            user=request.user,  # Ensure the bookings belong to the logged-in user
            booking_id__icontains=search_query
        )
    else:
        bookings = Booking.objects.filter(user=request.user)
    
    return render(request, 'view_bookings.html', {'bookings': bookings})
    
@login_required
def cancel_booking(request, booking_id):
    # Fetch the booking or return 404 if not found
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    # Check if the booking is already cancelled or not
    if booking.status == 'Cancelled':
        messages.warning(request, 'This booking is already cancelled.')
    else:
        # Update the status to 'Cancelled'
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled successfully.')
    
    # Redirect to the bookings page
    return redirect('view_bookings')

@login_required
def list_travel_options(request):
    travel_options = TravelOption.objects.all()
    return render(request, 'list_travel_options.html', {'travel_options': travel_options})

@login_required
def book_travel(request, travel_id):
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            number_of_seats = form.cleaned_data['number_of_seats']

            if number_of_seats > travel_option.available_seats:
                form.add_error('number_of_seats', 'Not enough seats available.')
            else:
                # Save the booking
                booking_instance = Booking(
                    user=request.user,
                    travel_option=travel_option,
                    number_of_seats=number_of_seats,
                    total_price=number_of_seats * travel_option.price,
                    status='Pending'
                )
                booking_instance.save()

                # Update the travel option's available seats
                travel_option.available_seats -= number_of_seats
                travel_option.save()

                messages.success(request, 'Your travel has been successfully booked!')

                return redirect('list_travel_options')  # Redirect after saving
        else:
            messages.error(request, 'There was an error with your booking.')
    else:
        form = BookingForm(initial={'travel_option': travel_option})

    return render(request, 'book_travel.html', {'form': form, 'travel_option': travel_option})