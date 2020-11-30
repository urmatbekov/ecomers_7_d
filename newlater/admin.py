from django.contrib import admin
from newlater.models import SignUp
from newlater.forms import SignUpForm


# Register your models here.
@admin.register(SignUp)
class SignUpAdmin(admin.ModelAdmin):
    list_display = ('email','full_name','timestamp','updated')
    form = SignUpForm
