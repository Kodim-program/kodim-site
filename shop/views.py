from django.core.mail import EmailMultiAlternatives
from django.db.models import Min
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template

from .forms import OrderForm, ServiceOrderForm
from .models import (Model3D, ModelCategory, OrderRequest, Service, ServiceCategory,
                     ServiceOrder, Technology)

DAYS_OPTIONS = [3, 7, 14, 30]


def _int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _notify(subject, template, context):
    html = get_template(template).render(context)
    msg = EmailMultiAlternatives(subject, html, "support@kodim.ua", ["kodim.pervomaisk@gmail.com"])
    msg.attach_alternative(html, "text/html")
    msg.send()


# ---------- МОДЕЛІ ----------
def catalog(request):
    g = request.GET
    qs = Model3D.objects.filter(is_active=True).select_related("category", "material")

    if g.get("category"):
        qs = qs.filter(category__slug=g["category"])
    if g.get("kind") in ("own", "makerworld"):
        qs = qs.filter(source_type=g["kind"])
    if _int(g.get("price_min")) is not None:
        qs = qs.filter(print_price__gte=_int(g["price_min"]))
    if _int(g.get("price_max")) is not None:
        qs = qs.filter(print_price__lte=_int(g["price_max"]))
    if _int(g.get("days_max")) is not None:
        qs = qs.filter(delivery_days__lte=_int(g["days_max"]))
    techs = g.getlist("tech")
    if techs:
        qs = qs.filter(material__slug__in=techs)

    return render(request, "shop/catalog.html", {
        "models": qs,
        "categories": ModelCategory.objects.all(),
        "kinds": [("own", "Власні моделі"), ("makerworld", "З MakerWorld")],
        "technologies": Technology.objects.filter(kind="material"),
        "tech_title": "Матеріал",
        "days_options": DAYS_OPTIONS,
        "selected_techs": techs,
    })


def model_detail(request, slug):
    model = get_object_or_404(Model3D, slug=slug, is_active=True)
    sent = request.GET.get("sent") == "1"
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            OrderRequest.objects.create(model3d=model, **d)
            _notify(f"Заявка на друк: {model.title}", "shop/order_email.html", {"model": model, **d})
            return redirect(f"{model.get_absolute_url()}?sent=1")
    else:
        form = OrderForm()
    return render(request, "shop/model_detail.html", {"model": model, "form": form, "sent": sent})


# ---------- ПОСЛУГИ ----------
def services_catalog(request):
    g = request.GET
    qs = (Service.objects.filter(is_active=True)
          .select_related("category")
          .annotate(min_price=Min("packages__price"), min_days=Min("packages__delivery_days"))
          .filter(min_price__isnull=False))

    if g.get("category"):
        qs = qs.filter(category__slug=g["category"])
    if g.get("kind") in ("app", "modeling"):
        qs = qs.filter(kind=g["kind"])
    if _int(g.get("price_min")) is not None:
        qs = qs.filter(min_price__gte=_int(g["price_min"]))
    if _int(g.get("price_max")) is not None:
        qs = qs.filter(min_price__lte=_int(g["price_max"]))
    if _int(g.get("days_max")) is not None:
        qs = qs.filter(min_days__lte=_int(g["days_max"]))
    techs = g.getlist("tech")
    if techs:
        ids = Service.objects.filter(technologies__slug__in=techs).values("pk")
        qs = qs.filter(pk__in=ids)

    return render(request, "shop/services_catalog.html", {
        "services": qs,
        "categories": ServiceCategory.objects.all(),
        "kinds": [("app", "Розробка додатків"), ("modeling", "3D-моделювання")],
        "technologies": Technology.objects.filter(kind="service"),
        "tech_title": "Технологія",
        "days_options": [7, 14, 30, 60],
        "selected_techs": techs,
    })


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    sent = request.GET.get("sent") == "1"
    if request.method == "POST":
        form = ServiceOrderForm(request.POST, service=service)
        if form.is_valid():
            d = form.cleaned_data
            ServiceOrder.objects.create(**d)
            _notify(f"Заявка на послугу: {service.title} / {d['package'].name}",
                    "shop/service_order_email.html", {"service": service, **d})
            return redirect(f"{service.get_absolute_url()}?sent=1")
    else:
        form = ServiceOrderForm(service=service)
    return render(request, "shop/service_detail.html",
                  {"service": service, "packages": service.packages.all(), "form": form, "sent": sent})