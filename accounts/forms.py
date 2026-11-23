from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Налаштування полів для сумісності з кастомною моделлю
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({'placeholder': 'Введіть ім`я користувача'})
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({'placeholder': 'Введіть ваш email'})