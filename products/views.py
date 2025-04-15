from rest_framework import generics # Import DRF's generic views
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer



# --- Category Views ---

class CategoryListAPIView(generics.ListAPIView):
    """
    API view to list all categories.
    User ListAPIView for read-only endpoint listing a quesryset
    """
    # queryset: Defines the initial set of objects this view will work with.
    # Here, we get all Category objects.
    queryset = Category.objects.all()
    # serializer_class: specifies the serializer to use for converting the
    # queryset objects into the response data format (JSON).
    serializer_class = CategorySerializer
    # Permission can be added later, e.g.:
    # permission_classes = [permissions.AllowAny] # Default


class CategoryDetailAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve a single category by its ID (pk)
    Uses RetrieveAPIView for read-only endpoint for a single model instance.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # DRF's RetrieveAPIView automatically hadles lookup by primary key ('pk')
    # based on the URL configuration  (which we'll set up next).


# --- Product Views ---
class ProductListAPIView(generics.ListAPIView):
    """
    API view to list all available products.
    """
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve a single available product by its ID (pk).
    """
    # Ensure we only retrieve products that are available.
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    # Like CategoryDetailAPIView, lookup by 'pk' is handled automatically.

# Note: We are currently only creating read-only views (List and Retrieve).
# We will use other generic views (Create, Update, Destroy) or ViewSets later
# to handle creating, updating, and deleting products/categories via the API.