from rest_framework import serializers
from .models import Category, Product
import decimal # Import the decimal module for validation


class CategorySerializer(serializers.ModelSerializer):
    """"
    Serializer for the Category model.
    Includes read-only representation of child categories
    """
    # Display primary keys of children categories in the response.
    # 'many=True' because a category can have multiple children.
    # 'read_only=True' because we typically manage childe relationships via the 'parent' field pn the child.
    children = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


    class Meta:
        model = Category
        # Specify the fields from the Category model to include in the serialization.
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'parent',       # Still expects parent ID on input
            'children',     # Read-only list of child IDs on output
            'created_at',
            'updated_at',
        ]
        # Optional: Mark fields as read-only if they shouldn't be directly set via API input
        read_only_fields = ['slug']



class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    Includes nested Category details (read-only) and validation.
    """
    # Nest the CategorySerializer for read operations.
    # 'read_only=True' means for GET requests, the full category object (as defined
    # by CategorySerializer) will be nested. For POST/PUT/PATCH requests, DRF will
    # still expect a simple primary key (ID) for the category field in the input data.
    # This avoids complex handling of nested writes for now.
    category= CategorySerializer(read_only=True)

    # Add a write-only field that accepts the category ID during create/update
    # 'source' links this field to the actual 'category' model field for saving.
    # 'queryset' is needed for validation when using PrimaryKeyRelatedField for writes.
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )


    class Meta:
        model = Product
        # Specify the fields from the Product model to include.
        fields = [
            'id',           # Primary key
            'category',     # Read-only nested representation
            'category_id',  # Write-only ID input
            'name',
            'slug',
            'description',
            'price',
            'stock',
            'available',
            'created_at',
            'updated_at',
            # 'image' field would be added here later
        ]
        
        read_only_fields = ['slug', 'category']

    # --- Custom Validation Methods ---

    def validate_price(self, value):
        """
        Ensures the price is not negative
        """
        if value < decimal.Decimal(0):
            raise serializers.ValidationError("Price cannot be negative")
        return value
    
    def validate_stock(self, value):
        """
        Ensure the stock is not negative
        """
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    # Example of object-level validation (runs after field-level validation)
    # def validate(self, data):
    #     """
    #     Check complex conditions across multiple fields.
    #     Example: Ensure stock is 0 if available is False.
    #     """
    #     if not data.get('available', True) and data.get('stock', 0) > 0:
    #         raise serializers.ValidationError("If product is not available, stock must be 0.")
    #     return data