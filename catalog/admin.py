from django.contrib import admin
from django.contrib import messages
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    # Req 12: block deleting a category that has products (extra safety on top of PROTECT)
    def delete_queryset(self, request, queryset):
        blocked = [c.name for c in queryset if c.products.exists()]
        if blocked:
            self.message_user(request, f'Cannot delete: {", ".join(blocked)} has products.', messages.ERROR)
            return
        super().delete_queryset(request, queryset)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    list_editable = ('price', 'stock', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
