from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "이메일"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"}))

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 다릅니다"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("가입된 이메일이 아닙니다"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("email", "nickname", "nationality")
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "이메일"}),
            "nickname": forms.TextInput(attrs={"placeholder": "닉네임"}),
        }
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인"}))

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("두 비밀번호가 다릅니다")
        else:
            return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("이미 가입된 이메일입니다")
        except models.User.DoesNotExist:
            return email

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")
        try:
            models.User.objects.get(nickname=nickname)
            raise forms.ValidationError("이미 가입된 닉네임입니다")
        except models.User.DoesNotExist:
            return nickname

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()