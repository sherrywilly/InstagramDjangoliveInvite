  
from django import forms

from core.models import IgUser, SlaveUser
from flatpickr import  TimePickerInput

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
class SlaveForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    class Meta:
        model = SlaveUser
        fields = ['username', 'password']
class IgUpdateForm(forms.ModelForm):
    class Meta:
        model = IgUser
        fields = ['ftime', 'ttime','slave','proxy',]
        widgets = {
            'ftime': TimePickerInput(),
            'ttime': TimePickerInput()
        }

    def __init__(self, user, *args, **kwargs):
        super(IgUpdateForm, self).__init__(*args, **kwargs)
        self.fields['slave'].queryset = SlaveUser.objects.filter(
            created_by=user.username)



