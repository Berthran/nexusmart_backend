from django.contrib import admin
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    """
    # Fields to display in the list view of categories
    list_display = ('name','slug', 'parent', 'created_at')
    # Fields that can be used to filter the list view
    list_filter = ('created_at', 'updated_at', 'parent')
    # Automaticaaly generate the slug field based on the name field
    prepopulated_fields = {'slug': ('name',)}
    # Fields to search by in the admin search bar
    search_fields = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product Model
    """
    # Fields to display in the list view of products
    list_display = ('name', 'slug', 'category', 'price', 'stock', 'available', 'created_at', 'updated_at')
    # Fields that can be used to filter the list view
    list_filter = ('available', 'created_at', 'updated_at', 'category')
     # Fields that can be edited directly in the list view (use with caution)
    list_editable = ('price', 'stock', 'available')
    # Automatically generate the slug field based on the name field
    prepopulated_fields = {'slug': ('name',)}
    # Fields to search by in the admin search bar
    search_fields = ('name', 'description')
    # Improves performance for ForeignKey dropdowns with many items
    row_id_fields = ('category',)
    # Organizes fields in the detail/edit view
    fieldsets = (
        (None, {
            'fields': ('category', 'name',  'price', 'slug', 'stock', 'available')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse', ) # Make description collapsible
        }),

    )