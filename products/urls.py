from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router instance. DefaultRouter includes a default API root view.
router = DefaultRouter()


# Register the viewsets with the router.
# The router automatically generates URLs for standard actions (list, create, retrieve, update, etc.)
# router.register(prefix, viewset, basename)
#   prefix: The URL prefix for this viewset (e.g., 'categories')
#   viewset: The ViewSet class
#   basename: Used to generate URL names. Optional if 'queryset' is set on the viewset,
#             but good practice to include for clarity. DRF will generate names like
#             'category-list', 'category-detail', 'product-list', 'product-detail'.
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')

# The API URLs are now determined automatically by the router.
# We no longer need the app_name definition here as the router handles naming.
urlpatterns = router.urls

# You could also include the router URLs within a list if you had other non-router paths:
# urlpatterns = [
#     path('', include(router.urls)),
#     # path('some-other-path/', views.some_other_view, name='other'),
# ]