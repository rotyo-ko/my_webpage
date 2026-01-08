from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm): 
    username = forms.CharField(
        label="ユーザー名",
        min_length=6,
        # バリデーションで6文字以上の制限にしている。
        help_text="(半角英数6文字以上)",
        error_messages={
            'min_length': "ユーザー名は6文字以上で入力してください。"
        }, 
    )
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        min_length=6,
        help_text="(半角英数6文字以上)",
        error_messages={
            'min_length': "パスワードは6文字以上で入力してください。"
        }
    )
    password2 = forms.CharField(
        label="パスワード（確認用)",
        widget=forms.PasswordInput,
        min_length=6
    )
    # UserCreationFormはModelFormを継承しているので、form.is_valid()のあと、form.save()すると
    # Userインスタンスが生成されusernameと,ハッシュ化されたpassword1
    # がpasswordとしてUserインスタンスに保持される
    class Meta:                                 
        model = User                            
        fields = ("username", "password1", "password2")
        

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "ユーザー名"
        self.fields["password"].label = "パスワード"