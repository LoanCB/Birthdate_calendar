from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label="Nom d'utilisateur")
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="Mot de passe")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        classes = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5'
        self.fields['username'].widget.attrs['class'] = classes
        self.fields['password'].widget.attrs['class'] = classes
