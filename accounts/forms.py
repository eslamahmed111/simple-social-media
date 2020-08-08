from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"
        
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None     # To hide help text