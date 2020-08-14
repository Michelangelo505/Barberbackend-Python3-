from django.forms import *
from .models import *


class Registration(Form):
    size = 20
    username = CharField(label='Имя пользвователя',widget= widgets.TextInput)
    password1 = CharField(label='Пароль',widget= widgets.PasswordInput)
    password2 = CharField(label='Повторить',widget= widgets.PasswordInput)
    phone = CharField(
        label='Номер телефона',
        widget= widgets.TextInput(
            attrs={'size':size}
        )
    )
    def clean(self):
        errors = {}

        if not self.cleaned_data['password1'] == self.cleaned_data['password2']:
            errors['password2'] = ValidationError(
                'Введенные пароли не совпадают'
            )
        if len(self.cleaned_data['phone']) > self.size:
            errors['phone'] = ValidationError(
                'Неверный номер телефона'
            )
        if errors:
            raise ValidationError(errors)

class BNewsForm(ModelForm):
    class Meta:
        model = BarberNews
        fields = (
            "bTitleNews",
            "bTextNews",
            "bNewsImage",
        )
        labels = {
            'bTitleNews':'Заголовок',
            'bTextNews':'Описание',
            'bNewsImage':'Изображение',
        }


