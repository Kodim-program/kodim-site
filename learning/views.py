from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Enrollment, Material, MaterialProgress, Test, TestResult
from .forms import TestAttemptForm


@login_required
def my_courses(request):
    """Список курсів, призначених учню, з прогрес-баром по кожному."""
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    return render(request, 'learning/my_courses.html', {'enrollments': enrollments})


def _get_enrollment_or_403(request, course_id):
    return get_object_or_404(Enrollment, user=request.user, course_id=course_id)


@login_required
def course_materials(request, course_id):
    """Список матеріалів курсу зі статусами прочитано/заблоковано + прогрес-бар."""
    enrollment = _get_enrollment_or_403(request, course_id)
    materials_status = enrollment.materials_with_status()
    test = Test.objects.filter(course=enrollment.course).first()

    return render(request, 'learning/course_materials.html', {
        'enrollment': enrollment,
        'materials_status': materials_status,
        'test': test,
    })


@login_required
def material_detail(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    enrollment = _get_enrollment_or_403(request, material.course_id)

    if not material.is_unlocked_for(request.user):
        messages.warning(request, 'Спочатку пройдіть попередній матеріал.')
        return redirect('learning:course_materials', course_id=material.course_id)

    is_read = MaterialProgress.objects.filter(
        user=request.user, material=material, is_read=True
    ).exists()

    if request.method == 'POST':
        MaterialProgress.objects.update_or_create(
            user=request.user, material=material,
            defaults={'is_read': True, 'read_at': timezone.now()},
        )
        messages.success(request, f'Матеріал «{material.title}» позначено як прочитаний.')
        return redirect('learning:course_materials', course_id=material.course_id)

    return render(request, 'learning/material_detail.html', {
        'material': material,
        'enrollment': enrollment,
        'is_read': is_read,
    })


@login_required
def take_test(request, course_id):
    enrollment = _get_enrollment_or_403(request, course_id)
    test = get_object_or_404(Test, course_id=course_id)

    if not enrollment.all_materials_read():
        messages.warning(request, 'Спершу прочитайте всі матеріали курсу.')
        return redirect('learning:course_materials', course_id=course_id)

    if test.attempts_left(request.user) <= 0:
        messages.error(request, 'Ви вичерпали кількість спроб для цього тесту.')
        return redirect('learning:course_materials', course_id=course_id)

    if request.method == 'POST':
        form = TestAttemptForm(request.POST, test=test)
        if form.is_valid():
            score, passed = form.score()
            TestResult.objects.create(
                user=request.user, test=test, score=score, passed=passed,
            )
            return redirect('learning:test_result', course_id=course_id)
    else:
        form = TestAttemptForm(test=test)

    return render(request, 'learning/test.html', {
        'test': test,
        'form': form,
        'enrollment': enrollment,
        'attempts_left': test.attempts_left(request.user),
    })


@login_required
def test_result(request, course_id):
    enrollment = _get_enrollment_or_403(request, course_id)
    test = get_object_or_404(Test, course_id=course_id)
    last_result = TestResult.objects.filter(user=request.user, test=test).first()

    return render(request, 'learning/test_result.html', {
        'enrollment': enrollment,
        'test': test,
        'result': last_result,
        'attempts_left': test.attempts_left(request.user),
    })
