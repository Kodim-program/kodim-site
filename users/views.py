from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import authenticate, login
from users.forms import UserRegisterForm
from learning.models import Enrollment, MaterialProgress

from django.http import JsonResponse
from django.contrib.auth.views import LoginView

from django.middleware.csrf import get_token
from django.urls import reverse


def _is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def _auth_ok(request, redirect_url='/'):
    """JSON-відповідь після успішного входу/реєстрації."""
    return JsonResponse({
        'ok': True,
        'redirect': redirect_url,
        'profile_url': reverse('users:profile'),
        'csrf': get_token(request),   # Django міняє CSRF-токен після входу
    })

class AjaxLoginView(LoginView):
    """Звичайний LoginView, але для AJAX повертає JSON замість редіректу/HTML."""

    def form_valid(self, form):
        response = super().form_valid(form)
        if _is_ajax(self.request):
            return _auth_ok(self.request, redirect_url=self.get_success_url())
        return response

    def form_invalid(self, form):
        if _is_ajax(self.request):
            return JsonResponse(
                {'ok': False, 'errors': ['Невірний логін або пароль. Спробуйте ще раз.']},
                status=400,
            )
        return super().form_invalid(form)

@login_required
def profile(request):
    enrollments = (
        Enrollment.objects.filter(user=request.user)
        .select_related('course')
        .prefetch_related('course__materials')
    )

    # Перший курс, де є що продовжити
    continue_item = None
    for enrollment in enrollments:
        material = enrollment.next_material()
        if material:
            continue_item = {'enrollment': enrollment, 'material': material}
            break

    # Останні прочитані матеріали — аналог "нещодавніх статей"
    recent_progress = (
        MaterialProgress.objects.filter(user=request.user, is_read=True)
        .select_related('material', 'material__course')
        .order_by('-read_at')[:5]
    )

    context = {
        'enrollments': enrollments,
        'continue_item': continue_item,
        'recent_progress': recent_progress,
    }
    return render(request, 'registration/profile.html', context)


class Register(View):
    template_name = 'registration/registration.html'

    def get(self, request):
        context = {
            'form': UserRegisterForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            if _is_ajax(request):
                return _auth_ok(request, '/')
            return redirect('/')

        if _is_ajax(request):
            errors = [e for errs in form.errors.values() for e in errs]
            return JsonResponse({'ok': False, 'errors': errors}, status=400)
        return render(request, self.template_name, {'form': form})