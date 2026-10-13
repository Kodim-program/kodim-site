from django.contrib import admin

from .models import (
    ModelCategory,
    Model3D,
    OrderRequest,
    Technology,
    ServiceCategory,
    Service,
    ServicePackage,
    ServiceOrder,
)


# ---------- Спільне ----------
@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "kind")
    list_filter = ("kind",)
    prepopulated_fields = {"slug": ("name",)}


# ---------- Розділ «Моделі» ----------
@admin.register(ModelCategory)
class ModelCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Model3D)
class Model3DAdmin(admin.ModelAdmin):
    list_display = (
        "title", "category", "source_type", "license_type",
        "material", "delivery_days", "print_price", "is_active",
    )
    list_filter = ("source_type", "license_type", "category", "material", "is_active")
    search_fields = ("title", "author_name")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_active",)


@admin.register(OrderRequest)
class OrderRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "model3d", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "phone", "email")
    readonly_fields = ("model3d", "name", "phone", "email", "comment", "created_at")


# ---------- Розділ «Послуги» ----------
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ServicePackageInline(admin.TabularInline):
    model = ServicePackage
    extra = 3


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "category", "is_active")
    list_filter = ("kind", "category", "is_active")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    inlines = [ServicePackageInline]


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "package", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "phone", "email")
    readonly_fields = ("package", "name", "phone", "email", "comment", "created_at")