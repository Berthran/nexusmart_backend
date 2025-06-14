from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, RangeFilter

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


# --- Custom FilterSet for Products ---
# We define a custome FilterSet to enable more advanced filetering optins, like ranges.
class ProductFilter(FilterSet):
    price = RangeFilter()
    class Meta:
        model = Product
        fields = ['category', 'available', 'price']


# --- Category Viewset ---
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    Provides list, create, retrieve, updata, partial_update, destroy actions automatically
    """
    queryset = Category.objects.all().order_by('name') # Get all categories, ordered by name
    serializer_class = CategorySerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filter_backends = [DjangoFilterBackend]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    Provides list, create, retrieve, update, partial_update, destroy actions automatically.
    """
    # queryset = Product.objects.filter(available=True).order_by('-created_at') # The old line
    # --- OPTIMIZED QUERYSET ---
    # Use .select_related('category') to perform a JOIN and fetch related category
    # data in a single database query, solving the N+1 problem.
    queryset = Product.objects.select_related('category').filter(available=True).order_by('-created_at')

    serializer_class = ProductSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    # --- Apply Caching ---
    # Apply the cache_page decorator to the 'list' method of this viewset.
    # The cache will last for 60 seconds * 2 (i.e., 2 minutes).
    # @method_decorator(cache_page(60*2), name="list")
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # --- Custom Action ---
    # The @action decorator routes this method.
    # detail=False means this action operates on the list of products (e.g., /api/v1/products/recent/),
    # not on a specific product detail (e.g., /api/v1/products/{pk}/recent/).
    # methods=['get'] specifies that this action only responds to GET requests.
    @action(detail=False, methods=['get'], url_path='recent', url_name='recent-products')
    def recent_products(self, request):
        """
        Custom action to retrieve the 5 most recently added available products.
        """
        # Get the last 5 available products based on creation date
        recent_products = Product.objects.filter(available=True).order_by('-created_at')[:5]
        # Serialize the queryset
        serializer = self.get_serializer(recent_products, many=True)
        # Return the serialized data in a standard DRF Response
        return Response(serializer.data, status=status.HTTP_200_OK)

    


  