from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth import get_user_model
from registration.forms import RegistrationForm

User = get_user_model()


class UserRegistrationForm(RegistrationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'country', 'phone', 'captcha']
