from django.urls import path
from . import views

#  Define an app name for namespacing. This helps avoid URL name collisions 
#  betweenn different apps in the project. It allows us to refer to these URLs 
#  like 'products:product-list'.
app_name = 'products'

urlpatterns = [
    # --- Category URLS ---
    # URL for listing all categories
    path(
        'categories/', # The URL path fragment
        views.CategoryListAPIView.as_view(), # The view calss to handle requests (use .as_view() for CBVs)
        name='category-list' # A unique name to refer to this URL pattern later (e.g., in templates or tests)
    ),
    # URL for retrieving a single category bu its primary key (pk)
    path(
        'categories/<int:pk>/', # <int:pk> captures an integer from the URL and passes it as 'pk' to the view
        views.CategoryDetailAPIView.as_view(),
        name='category-detail'
    ),

    # --- Product URLs ---
    # URL for listing all available products
    path(
        'products/',
        views.ProductListAPIView.as_view(),
        name='product-list'
    ),
    # URL for retrieving a single available product by its primary key (pk)
    path(
        'products/<int:pk>/',
        views.ProductDetailAPIView.as_view(),
        name='product-detail'
    ),
]