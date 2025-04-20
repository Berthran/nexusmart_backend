from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, RangeFilter
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


# --- Custom FilterSet for Products ---
# We define a custome FilterSet to enable more advanced filetering optins, like ranges.
class ProductFilter(FilterSet):
    # Define a filter for the 'price' field that allows range queries
    # e.g., ?price_min=10.00&price_max=50.00
    price = RangeFilter()

    class Meta:
        model = Product
        # Specify the fields available for filtering
        # 'price' uses the RangeFilter defined above.
        # 'category' and 'available' will use default exact match lookups.
        fields = ['category', 'available', 'price']

# --- Category Viewset ---
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    Provides list, create, retrieve, updata, partial_update, destroy actions automatically
    """
    queryset = Category.objects.all().order_by('name') # Get all categories, ordered by name
    serializer_class = CategorySerializer
    # permission_classes: Define who can access this viewset.
    # IsAuthenticatedOrReadOnly allows anyone to view (GET, HEAD, OPTIONS)
    # but only authenticated users to perform write actions (POST, PUT, PATCH, DELETE).
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    # filter_backends = [DjangoFilterBackend]


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
    # Use DjangoModelPermissionsOrAnonReadOnly for standard model permission checks
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
 

   # --- Filtering & Search Configuration ---
    # Specify the filter backends to use for this viewset.
    # We add SearchFilter alongside DjangoFilterBackend.
    filter_backends = [DjangoFilterBackend, SearchFilter]

    # Use our custom FilterSet class for django-filter backend
    filterset_class = ProductFilter
    # Remove filterset_fields as filterset_class handles field definitions

    # Specify the fields for the SearchFilter backend.
    # Allows requests like /api/v1/products/?search=laptop
    # It will search case-insensitively across name and description.
    search_fields = [
        'name',
        'description',
        # Can also search related fields like category name:
        # 'category__name',
    ]

    


  