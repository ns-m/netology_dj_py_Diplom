from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _


class RegistrationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("Пароли не совпадают."),
    }
    first_name = forms.CharField(max_length=100,
                                 label=_("Имя пользователя:"),
                                 widget=forms.TextInput(
                                     attrs={'id': 'inputUsername',
                                            'class': 'form-control first-field',
                                            'placeholder': 'Имя',
                                            'value': '',
                                            'required': '',
                                            'autofocus': '',
                                            'data-cip-id': 'inputUsername'})
                                 )
    username = forms.EmailField(max_length=254,
                                label=_("E-mail пользователя:"),
                                widget=forms.EmailInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Email',
                                           'value': '',
                                           'required': '',
                                           'data-cip-id': 'inputEmail'})
                                )
    password1 = forms.CharField(label=_("Придумайте пароль:"),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Пароль',
                                           'required': '',
                                           'data-cip-id': 'inputPassword1'})
                                )
    password2 = forms.CharField(label=_("Подтвердите пароль:"),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control last-field',
                                           'placeholder': 'Повторите пароль',
                                           'required': '',
                                           'data-cip-id': 'repeatPassword2'}),
                                help_text=_("Введите тот же пароль, что и ранее."))
    field_order = ['first_name', 'username', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.EmailField(max_length=254,
                                label=_("E-mail пользователя:"),
                                widget=forms.EmailInput(
                                    attrs={'class': 'form-control first-field',
                                           'placeholder': 'Email',
                                           'value': '',
                                           'required': '',
                                           'autofocus': '',
                                           'data-cip-id': 'inputEmail'})
                                )
    password = forms.CharField(label=_("Пароль:"),
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control last-field',
                                          'placeholder': 'Пароль',
                                          'required': '',
                                          'data-cip-id': 'inputPassword1'})
                               )
    field_order = ['username', 'password']


CHOICES=[('1', '1'),
         ('2', '2'),
         ('3', '3'),
         ('4', '4'),
         ('5', '5')]


class ReviewForm(forms.Form):
    name = forms.CharField(label=_("Имя:"),
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'aria-describedby': 'nameHelp',
                                      'placeholder': 'Представьтесь',
                                      'required': '',
                                      'data-cip-id': 'name'}),
                           )
    description = forms.CharField(label=_("Содержание"),
                                  widget=forms.Textarea(
                                      attrs={'class': 'form-control',
                                             'placeholder': 'Содержание',
                                             'required': '',
                                             'rows': '',
                                             'cols': ''}),
                                  )
    mark = forms.ChoiceField(choices=CHOICES,
                             widget=forms.RadioSelect(
                                 attrs={'class': 'form-check-input'})
                             )
