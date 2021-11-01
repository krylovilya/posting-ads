from django.forms import ModelForm

from apps.main.models import Seller, User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class SellerForm(ModelForm):
    class Meta:
        model = Seller
        fields = ('itn',)
