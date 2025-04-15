from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """"
    Serializer for the Category model.
    Converts Category model instances to JSON and validates incoming data
    """
    class Meta:
        model = Category
        # Specify the fields from the Category model to include in the serialization.
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'parent',       # Foreign key to parent category (will be represented by its ID)
            'created_at',
            'updated_at',
        ]
        # Optional: Mark fields as read-only if they shouldn't be directly set via API input
        # read_only_fields = ['slug', 'created_at', 'updated_at']



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # Specify the fields from the Product model to include.
        fields = [
            'id',           # Primary key
            'category',     # Foreign key to Category (will be represented by its ID)
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
        # Optional: Mark fields as read-only
        # read_only_fields = ['slug', 'created_at', 'updated_at']