from django import forms
from django.contrib.auth import get_user_model
from .models import UserAddress,AddressType
User = get_user_model()
class UserCheckoutForm(forms.Form):
    # TODO: Define form fields here
    email = forms.EmailField()
    email2 = forms.EmailField(label = "Verify email")
    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email == email2:
            count = User.objects.filter(email=email2).count()
            if count == 1:
                raise  forms.ValidationError("This User alridy exist. Please login instead")
            return email2
        else:
            raise forms.ValidationError("Please confirm email are same.")
class AddressForm(forms.Form):
    shipping = AddressType.objects.get(id=2)
    bilding = AddressType.objects.get(id=1)
    shipping_address = forms.ModelChoiceField(
                    queryset = UserAddress.objects.filter(type=shipping),
                    widget = forms.Select(),
                    empty_label = None,
    )
    billing_address = forms.ModelChoiceField(
                    queryset = UserAddress.objects.filter(type=bilding),
                    widget = forms.Select(),
                    empty_label = None,
    )
class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['type','street','city','state','zipcode']
