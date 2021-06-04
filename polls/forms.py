from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField()
    last_name = forms.CharField()


class EditAccountForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    bio = forms.CharField(required=False)


class CreatePollForm(forms.Form):
    question = forms.CharField(required=True)
    choice1 = forms.CharField(required=True)
    choice2 = forms.CharField(required=True)
    choice3 = forms.CharField(required=False)
    choice4 = forms.CharField(required=False)
    choice5 = forms.CharField(required=False)
