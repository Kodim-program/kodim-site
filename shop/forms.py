from django import forms

from .models import ServicePackage


class OrderForm(forms.Form):
    """Заявка на друк моделі (сторінка model_detail)."""
    name = forms.CharField(
        min_length=2,
        widget=forms.TextInput(attrs={"placeholder": "Ваше ім'я", "class": "form-input"}),
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Телефон", "class": "form-input"}),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "E-mail (необов'язково)", "class": "form-input"}),
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Колір, розмір, кількість — деталі замовлення", "class": "form-input"}
        ),
    )


class ServiceOrderForm(forms.Form):
    """Заявка на послугу з вибором пакета (сторінка service_detail)."""
    package = forms.ModelChoiceField(
        queryset=ServicePackage.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None,
        error_messages={"required": "Оберіть пакет"},
    )
    name = forms.CharField(
        min_length=2,
        widget=forms.TextInput(attrs={"placeholder": "Ваше ім'я", "class": "form-input"}),
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Телефон", "class": "form-input"}),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "E-mail (необов'язково)", "class": "form-input"}),
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"placeholder": "Опишіть задачу коротко", "class": "form-input"}),
    )

    def __init__(self, *args, service=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Дозволяємо обрати лише пакети саме цієї послуги
        if service is not None:
            self.fields["package"].queryset = service.packages.all()