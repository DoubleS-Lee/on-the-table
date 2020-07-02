from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins
from django.contrib import messages


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"환영합니다 {user.nickname}님")
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, f"다음에 다시 만나요~")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class UserProfileView(DetailView):

    model = models.User
    #마이페이지 설정시 다른 유저가 나의 페이지를 볼수있는등 혼란스러운 상황을 막아주는 코드
    context_object_name = "user_obj"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.User
    template_name = "users/update_profile.html"
    fields = (
        "nickname",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "nationality",
    )

    success_message = "Profile Updated"

    #수정하길 원하는 객체를 반환함
    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["nickname"].widget.attrs = {"placeholder": "Nickname"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "ex)2020-05-04"}
        return form


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):
    template_name = "users/update_password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form

    #비번 바꾸면 처리해주는 함수
    def get_success_url(self):
        return self.request.user.get_absolute_url()


def follow(request, user_id):
    people = get_object_or_404(get_user_model(), id=user_id)
    if request.user in people.followers.all():
        # people을 unfollow 하기
        people.followers.remove(request.user)
    else:
        # 1. people을 follow 하기
        people.followers.add(request.user)
    
    return redirect('users:profile', user_id)