from django import forms
from django.contrib.auth.models import User

from .models import Account

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = Account
        fields = ['first_name','email','level', 'roll_number']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['required'] = True
        self.fields['level'].widget.attrs['class'] = 'form-control'
        self.fields['level'].widget.attrs['required'] = True
        self.fields['roll_number'].widget.attrs['class'] = 'form-control'
        self.fields['roll_number'].widget.attrs['required'] = True


    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data['password']
        confim_password = cleaned_data['confirm_password']

        if password != confim_password:
            raise forms.ValidationError('Password doesnot match')
        