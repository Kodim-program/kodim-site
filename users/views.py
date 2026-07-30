from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth import authenticate, login
from users.forms import UserRegisterForm
from learning.models import Enrollment, MaterialProgress


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
            return redirect('/')
        return render(request, self.template_name, {'form': form})
