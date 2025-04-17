from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Default Django admin site URL
    path('admin/', admin.site.urls),

    # --- API V1 URLS

    path(
        'api/v1/', # Prefix remains the same
        include('products.urls') # Just include the module path
    ),

    # --- JWT Authentication URLs ---
    # Endpoint to obtain token pair (access and refresh) by posting username/password
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint to obtain a new access token by posting a valid refresh token
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # We can add URLs for other apps (like users, orders) here later
    # path('api/v1/users/', include('users.urls')), # Example for later
]


# Add configurations for serving media files during development later if needed
# from django.conf import settings
# from django.conf.urls.static import static
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
