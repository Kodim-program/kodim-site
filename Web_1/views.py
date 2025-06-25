from .models import Customer, Course
from .forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import get_template

# Create your views here.
def index(request):
    return render(request, 'index.html', {'courses': Course.objects.all()[:3]})

def courses(request):
    return render(request, 'courses.html', {'courses': Course.objects.all()})

def course(request, id):
    return render(request, 'course.html', {'course': Course.objects.get(id=id)})

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
