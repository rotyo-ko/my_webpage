from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Comment

class CommentForm(forms.ModelForm):  
    class Meta:                      
        model = Comment
        fields = ("message",)  # 名前はフォームに表示させない
        labels = {"message": "メッセージ"}

class CustomUserCreationForm(UserCreationForm): 
    username = forms.CharField(
        label="ユーザー名",
        min_length=5,
        help_text="(半角英数5文字以上)"
    )
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        min_length=5,
        help_text="(半角英数5文字以上)"
    )
    password2 = forms.CharField(
        label="パスワード（確認用)",
        widget=forms.PasswordInput,
        min_length=5
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