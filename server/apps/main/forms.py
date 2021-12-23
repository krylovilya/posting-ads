from django import forms
from django.forms import ModelForm, inlineformset_factory

from apps.main.models import Ad, Picture, Seller, User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class SellerForm(ModelForm):
    sms_code_widget = forms.NumberInput(attrs={'size': 4, 'hidden': True, 'maxlength': "4", 'pattern': "[0-9]{4}"})
    sms_code = forms.IntegerField(widget=sms_code_widget, label='Код из смс')

    def validate_phone(self):
        """Проверка кода из смс"""
        seller = self.instance
        sms_log = seller.smslog
        entered_sms_code = int(self.data.get('sms_code', None))
        entered_phone = self.data.get('phone')
        if entered_phone != sms_log.sent_phone:
            self.add_error('phone', 'Полученный телефон не совпадает с подтверждённым')
        elif entered_sms_code and sms_log.code != entered_sms_code:
            self.add_error('phone', 'Введён неверный код')
        else:
            sms_log.confirmed = True
            sms_log.save()

    def clean(self):
        self.validate_phone()
        return super().clean()

    class Meta:
        model = Seller
        fields = ('itn', 'phone', 'sms_code')


ImageFormset = inlineformset_factory(parent_model=Ad, model=Picture, fields=('image',))
