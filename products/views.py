# Import DRF's generic views
from rest_framework import viewsets, permissions
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer



# --- Category Viewset ---
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    Provides list, create, retrieve, updata, partial_update, destroy actions automatically
    """
    # queryset: Defines the set of objects this viewset will manage.
    queryset = Category.objects.all().order_by('name') # Get all categories, ordered by name
    # serializer_class: Specifies the serializer to use for this viewset.
    serializer_class = CategorySerializer
    # permission_classes: Define who can access this viewset.
    # IsAuthenticatedOrReadOnly allows anyone to view (GET, HEAD, OPTIONS)
    # but only authenticated users to perform write actions (POST, PUT, PATCH, DELETE).
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    Provides list, create, retrieve, update, partial_update, destroy actions automatically.
    """
    # We only manage products that are marked as 'available'.
    # Note: This applies to list, retrieve, update, delete. Consider if you want
    # admins to manage unavailable products - might need custom queryset logic later.
    queryset = Product.objects.filter(available=True).order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # We can add custom actions, filtering, pagination etc. here later.
# Note: We are currently only creating read-only views (List and Retrieve).
# We will use other generic views (Create, Update, Destroy) or ViewSets later
# to handle creating, updating, and deleting products/categories via the API.