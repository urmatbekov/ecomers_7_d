from django import  forms
from newlater.models import SignUp

class SignUpForm(forms.ModelForm):
    # TODO: Define other fields here
    class Meta:
        model = SignUp
        fields = ('full_name','email')
    def clean_email(self):
        email=self.cleaned_data.get('email')
        email_base,provider = email.split('@')
        domain,extension = provider.split('.')
        if not domain == 'gmail':
            raise forms.ValidationError('Please use gmail acount')
        if not extension == 'com':
            raise forms.ValidationError('Please use .COM')
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        return full_name
class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()
    def clean_email(self):
        email=self.cleaned_data.get('email')
        email_base,provider = email.split('@')
        domain,extension = provider.split('.')
        if not domain == 'gmail':
            raise forms.ValidationError('Please use gmail acount')
        if not extension == 'com':
            raise forms.ValidationError('Please use .COM')
        return email
