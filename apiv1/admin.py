from django.contrib import admin
from .models import Company, Category, Product
from .models import Company, Category, Product, Cart, CartItem


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)



class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'price', 'category', 'company', 'uploaded_at', 'updated_at',)
    list_display_links = ('id', 'name',)
    readonly_fields = ('thumbnail_preview',)
    list_editable = ('is_active', 'category', 'company',)
    list_filter = ('category', 'company', 'is_active',)
    list_per_page = 25
    search_fields = ('name', 'price')  # this will create a text input for filtering title and price
    actions = ['make_active', 'make_not_active']


    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # You need to define a character for splitting your range, in this example I'll use a hyphen (-)
        try:
            # This will get me the range values if there's only 1 hyphen
            min_price, max_price = search_term.split('-')
        except ValueError:
            # Otherwise it will do nothing
            pass
        else:
            # If the try was successful, it will proceed to do the range filtering
            queryset |= self.model.objects.filter(price__gte=min_price, price__lte=max_price)
        return queryset, use_distinct

    @admin.action(description='Mark selected stories as active')
    def make_active(modeladmin, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Mark selected stories as not active')
    def make_not_active(modeladmin, request, queryset):
        queryset.update(is_active=False)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail'
    thumbnail_preview.allow_tags = True


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total')
    list_display_links = ('id', 'user', 'total')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'price', 'quantity')
    list_display_links = ('id', 'price', 'cart', 'product', 'quantity')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
