# nexusmart_backend/products/tests.py

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Product

User = get_user_model()

class ProductAPITests(APITestCase):
    """
    Tests for the Product API endpoints (ViewSet).
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')
        # Create a staff user for testing write operations
        cls.staff_user = User.objects.create_user(
            username='staffuser', password='password123', is_staff=True
        )

        cls.category = Category.objects.create(name='Test Category', slug='test-category')
        cls.category2 = Category.objects.create(name='Another Category', slug='another-category')


        cls.product1 = Product.objects.create(
            category=cls.category, name='Available Product 1', slug='available-product-1',
            price=10.00, stock=5, available=True
        )
        cls.product2 = Product.objects.create(
            category=cls.category, name='Available Product 2', slug='available-product-2',
            price=20.00, stock=10, available=True
        )
        cls.product3 = Product.objects.create(
            category=cls.category, name='Unavailable Product', slug='unavailable-product',
            price=30.00, stock=0, available=False
        )

        cls.list_url = reverse('product-list')
        # Helper function to get detail URL for a specific product
        cls.detail_url_for_product = lambda pk: reverse('product-detail', kwargs={'pk': pk})

    # --- List and Retrieve Tests (from previous step, ensure they still pass) ---
    def test_list_products_anonymous(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        product_names = {p['name'] for p in response.data['results']}
        self.assertIn(self.product1.name, product_names)
        self.assertNotIn(self.product3.name, product_names)

    def test_retrieve_available_product_detail(self):
        response = self.client.get(self.detail_url_for_product(self.product1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product1.name)

    def test_retrieve_unavailable_product_detail(self):
        response = self.client.get(self.detail_url_for_product(self.product3.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- Create (POST) Product Tests ---

    def test_create_product_anonymous_fails(self):
        new_product_data = {'category_id': self.category.pk, 'name': 'New Anon Product', 'price': '1.00', 'stock': 1}
        response = self.client.post(self.list_url, new_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Corrected from 403

    def test_create_product_authenticated_non_staff_fails(self):
        self.client.force_authenticate(user=self.user)
        new_product_data = {'category_id': self.category.pk, 'name': 'New User Product', 'price': '2.00', 'stock': 2}
        response = self.client.post(self.list_url, new_product_data, format='json')
        # DjangoModelPermissionsOrAnonReadOnly requires model permissions for POST,
        # which a regular authenticated user doesn't have by default.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_staff_user_succeeds(self):
        self.client.force_authenticate(user=self.staff_user)
        initial_product_count = Product.objects.count()
        new_product_data = {
            'category_id': self.category.pk,
            'name': 'New Staff Product',
            'price': '3.00',
            'stock': 3,
            'available': True
        }
        response = self.client.post(self.list_url, new_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), initial_product_count + 1)
        self.assertEqual(response.data['name'], new_product_data['name'])
        # Check if nested category is present in response
        self.assertIn('category', response.data)
        self.assertEqual(response.data['category']['id'], self.category.pk)


    def test_create_product_staff_user_invalid_data_fails(self):
        self.client.force_authenticate(user=self.staff_user)
        # Missing 'name' and negative price
        invalid_product_data = {'category_id': self.category.pk, 'price': '-5.00', 'stock': 1}
        response = self.client.post(self.list_url, invalid_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data) # Check for 'name' field error
        self.assertIn('price', response.data) # Check for 'price' field error

    # --- Update (PUT/PATCH) Product Tests ---

    def test_update_product_staff_user_succeeds(self):
        self.client.force_authenticate(user=self.staff_user)
        updated_data = {'name': 'Updated Product 1 Name', 'price': '12.00'}
        response = self.client.patch(self.detail_url_for_product(self.product1.pk), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, updated_data['name'])
        self.assertEqual(float(self.product1.price), float(updated_data['price']))

    def test_update_product_non_staff_user_fails(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url_for_product(self.product1.pk), {'name': 'Attempted Update'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_anonymous_fails(self):
        response = self.client.patch(self.detail_url_for_product(self.product1.pk), {'name': 'Attempted Update Anon'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # --- Delete (DELETE) Product Tests ---

    def test_delete_product_staff_user_succeeds(self):
        self.client.force_authenticate(user=self.staff_user)
        initial_product_count = Product.objects.count()
        response = self.client.delete(self.detail_url_for_product(self.product1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), initial_product_count - 1)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=self.product1.pk)

    def test_delete_product_non_staff_user_fails(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url_for_product(self.product1.pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_anonymous_fails(self):
        response = self.client.delete(self.detail_url_for_product(self.product1.pk))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

