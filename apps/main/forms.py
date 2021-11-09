from django.forms import ModelForm, inlineformset_factory

from apps.main.models import Ad, Picture, Seller, User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class SellerForm(ModelForm):
    class Meta:
        model = Seller
        fields = ('itn',)


ImageFormset = inlineformset_factory(parent_model=Ad, model=Picture, fields=('image',))
