from django.db import models
from django.utils.text import slugify
# Import the User model correctly using settings.AUTH_USER_MODEL if needed later
# from django.conf import settings


class Category(models.Model):
    """
    Model representing a product category.
    Allows for nested categories.
    """
    name = models.CharField(max_length=255, unique=True, help_text="Name of the category")
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text='URL-friendly slug (auto-generated)')
    description = models.TextField(blank=True, null=True, help_text="Optional description of the category")
    # Allow nesting categories (e.g., 'Men's Clothing' under 'Clothing')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE, # If a parent category is deleted, delete its children too
        null=True,
        blank=True,
        related_name='children', # How to refer to children from the parent
        help_text="Optional parent category for nesting"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # optional: Ensures category names are ordered alphabetically by default
        ordering = ('name',)
        # Optional: Sets the plural name used in the Django admin
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        '''
        Auto generates slug from name is not provided
        '''
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        '''
        String representation for the model instance
        '''
        return self.name
    

class Product(models.Model):
    """
    Model representing a product in the store.
    """
    category = models.ForeignKey(
        Category,
        related_name='products', # How to refer to products from the category
        on_delete=models.PROTECT, # Prevent deleting category if products are associated
        help_text="Category that this product belongs to"
    )
    name = models.CharField(max_length=255, help_text='Name of the product')
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text="URL-friendly slug (auto-generated)")
    description = models.TextField(blank=True, null=True, help_text="Detailed description of the product")
    # Use DecimalField for price to avoid floating-point inaccuracies
    price = models.DecimalField(
        max_digits=10,       # Max number of digits including decimal places
        decimal_places=2,    # Number of decimal places
        help_text="Price of the product"
    )
    stock = models.PositiveIntegerField(default=0, help_text="Number of items currently in stock")
    
    available = models.BooleanField(default=True, help_text="Is the product available for purchase?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # --- Add ImageField ---
    # 'upload_to' specifies a subdirectory of MEDIA_ROOT to store uploaded images.
    # '%Y/%m/%d/' will create subdirectories based on the upload date.
    # 'blank=True, null=True' makes the image optional.
    image = models.ImageField(
        upload_to='products/images/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Optional image for the product"
    )

    class Meta:
        # Optional: Default ordering for products
        ordering = ('-created_at',) # Show newest products first by default
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        # String representation for the model instance
        return self.name




