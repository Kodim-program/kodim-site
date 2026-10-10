from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.AjaxLoginView.as_view(), name='login'),

    # --- Скидання пароля (свої шаблони, namespace users:) ---
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name='users/password_reset_email.txt',
        html_email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',
        success_url=reverse_lazy('users:password_reset_done'),
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html',
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete'),
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html',
    ), name='password_reset_complete'),

    path('', include('django.contrib.auth.urls')),
    path('registration/', views.Register.as_view(), name='registration'),
    path('profile/', views.profile, name='profile'),
]