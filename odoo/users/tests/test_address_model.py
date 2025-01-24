from django.test  import TestCase
from ..models import AddressModel
from ..serializers.user_serializers import AddressSerializer

def create_address_object():
    return AddressModel.objects.create(
        address1="New colony",
        state="Uttar pradesh",
        country="India"
    )

class TestAddressModel(TestCase):
    def test_new_instace(self):
        instance = create_address_object()
        self.assertEqual(instance.address1, "New colony")
        self.assertEqual(instance.address2, None)
        self.assertEqual(instance.state, "Uttar pradesh")
        self.assertEqual(instance.country, "India")
        self.assertEqual(len(AddressModel.objects.all()), 1)

class TestAddressSerializer(TestCase):
    def test_new_serializer_instance(self):
        instance = create_address_object()
        serializer = AddressSerializer(instance)
        self.assertEqual(serializer.data.get("address1"), "New colony")
        self.assertEqual(serializer.data.get("address2"), None)
        self.assertEqual(serializer.data.get("state"), "Uttar pradesh")
        self.assertEqual(serializer.data.get("country"), "India")