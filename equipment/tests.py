
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from equipment.models import ClinicEquipmentCategory


User = get_user_model()


FUZZ_STRINGS = [
    '', 'a' * 1000, '<script>alert(1)</script>',
    "'; DROP TABLE equipment_clinicequipment; --",
    '../../../etc/passwd',
]

# Create your tests here.
class EquipmentAdminFuzzTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username='superadmin',
            password='superpassword123',
        )
        cls.category = ClinicEquipmentCategory.objects.create(
            description='Test Category'
        )

    def setUp(self):
        self.client.login(username='superadmin', password='superpassword123')


class EquipmentAdminFuzzTest(EquipmentAdminFuzzTest):

    def test_create_equipment_fuzz_name(self):
        url = reverse('admin:equipment_clinicequipment_add')
        for fuzz in FUZZ_STRINGS:
            with self.subTest(fuzz=repr(fuzz)):
                response = self.client.post(url, {
                    'category': self.category.pk,
                    'name': fuzz,
                    'instruction': 'Use carefully',
                    'warranty_period': '2027-01-01 00:00:00',
                    'certificate': 'CERT-001',
                    'price': '5000000',
                })
                self.assertNotEqual(response.status_code, 500)

    def test_create_equipment_fuzz_price(self):
        url = reverse('admin:equipment_clinicequipment_add')
        price_cases = ['0', '-1', '99999999999999', 'abc', '', '1.5']
        for price in price_cases:
            with self.subTest(price=price):
                response = self.client.post(url, {
                    'category': self.category.pk,
                    'name': 'Test Equipment',
                    'instruction': 'Use carefully',
                    'warranty_period': '2027-01-01 00:00:00',
                    'certificate': 'CERT-001',
                    'price': price,
                })
                self.assertNotEqual(response.status_code, 500)
