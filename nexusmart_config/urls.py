"""
URL configuration for nexusmart_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Default Django admin site URL
    path('admin/', admin.site.urls),

    # Include the URLs from the 'products' app under the 'api/v1' prefix
    # All URLs defined in products.urls will now be accessible starting with /api/v1/
    # e.g., /api/v1/products, /api/v1/categories/
    path(
        'api/v1/',  # The prefix for all URLs included from products.urls
        include('products.urls', namespace='products') # Include URLs from products/urls.py
        # The 'namespace' argument should match the 'app_name' defined in products.urls
        # It helps in uniquely identifying URL names, e.g., 'products:product-list'
    ),

    # We can add URLs for other apps (like users, orders) here later
    # path('api/v1/users/', include('users.urls', namespace='users')),
]

# Add configurations for serving media files during development later if needed
# from django.conf import settings
# from django.conf.urls.static import static
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
