from django import forms
from .models import Booking, TravelOption

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats']  # Include fields that the user will fill out

    # def __init__(self, *args, **kwargs):
    #     self.travel_option_id = kwargs.pop('travel_option_id', None)
    #     super().__init__(*args, **kwargs)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     number_of_seats = cleaned_data.get('number_of_seats')

    #     if self.travel_option_id:
    #         try:
    #             travel_option = TravelOption.objects.get(travel_id=self.travel_option_id)
    #             if number_of_seats > travel_option.available_seats:
    #                 raise forms.ValidationError('Not enough available seats.')
    #         except TravelOption.DoesNotExist:
    #             raise forms.ValidationError('Travel option does not exist.')
    #     else:
    #         raise forms.ValidationError('Travel option ID is missing.')

    #     return cleaned_data