from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class book_renew_form(forms.Form):
    renew_date=forms.DateField(help_text='Max No of Days to Renew is 3 Week(21 days)')


    def renew_data(self):
        data=self.cleaned_data['renew_date']

        if data < datetime.date.today():
            raise ValidationError( _('Invalid date - renewal in past'))

        if data > datetime.date.today()+ datetime.timedelta(week=4):
            raise ValidationError( _('Invalid date - renewal more than 4 weeks ahead'))

        return data
