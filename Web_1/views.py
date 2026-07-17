from .models import Customer, Course, News
from .forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    return render(request, 'index.html', {'courses': Course.objects.all()[:3]})

def courses(request):
    return render(request, 'courses.html', {'courses': Course.objects.all()})

def course(request, name_url):
    course = get_object_or_404(Course, name_url=name_url, is_active=True)
    return render(request, 'course.html', {'course': course})

def about(request):
    return render(request, 'about.html')

def contact_us(request):
    customer = Customer()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_message(form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['phone'], form.cleaned_data['text'],)
            customer.name = request.POST.get('name')
            customer.email = request.POST.get('email')
            customer.phone = request.POST.get('phone')
            customer.message = request.POST.get('text')
            customer.save()
            return HttpResponseRedirect("/contact-us/")
    return render(request, 'contact-us.html', {"form": ContactForm()})

def send_message(name, email, text, phone):
    text_send = get_template('message.html')
    html = get_template('message.html')
    context = {'name': name, 'email': email, 'text': text, 'phone': phone}
    theme = 'Повідомлення із сайту'
    from_email = 'support@kodim.ua'
    text_content = text_send.render(context)
    html_content = text_send.render(context)

    msg = EmailMultiAlternatives(theme, text_content, from_email, ['kodim.pervomaisk@gmail.com'])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
def news_list(request):
    news_qs = News.objects.filter(is_active=True)
    paginator = Paginator(news_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news.html', {'page_obj': page_obj})


def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, is_active=True)
    related_news = News.objects.filter(is_active=True).exclude(pk=news.pk)[:3]
    return render(request, 'news_detail.html', {
        'news': news,
        'related_news': related_news,
    })
