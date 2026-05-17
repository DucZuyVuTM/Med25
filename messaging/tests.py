from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Position, Employee, Administrator
from messaging.models import Email

User = get_user_model()

FUZZ_STRINGS = [
    '', 'a' * 1000, '<script>alert(1)</script>',
    "'; DROP TABLE messaging_message; --",
    '\x00\x01\x02',
]

# Create your tests here.
class MessagingAdminFuzzTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username='superadmin',
            password='superpassword123',
        )
        cls.position = Position.objects.create(
            title='Admin Position',
            salary=Decimal('10000000'),
            access_category='Full',
        )
        cls.admin_user = User.objects.create_user(
            username='admin_msg', password='pass123', role='administrator'
        )
        cls.employee, _ = Employee.objects.get_or_create(
            user=cls.admin_user,
            defaults={
                'position': cls.position,
                'surname': 'Admin', 'name': 'Test',
                'phone': '0900000001', 'address': 'Test St',
                'employment_date': date.today(),
                'end_date_of_the_contract': date.today(),
            }
        )
        cls.administrator, _ = Administrator.objects.get_or_create(
            employee=cls.employee,
            defaults={'system_access_rights': 'Full'},
        )
        cls.patient_user = User.objects.create_user(
            username='patient_msg', password='pass123', role='patient'
        )
        cls.email = Email.objects.create(
            administrator=cls.administrator,
            patient=cls.patient_user,
            status='open',
        )

    def setUp(self):
        self.client.login(username='superadmin', password='superpassword123')

    def test_create_message_fuzz_content(self):
        url = reverse('admin:messaging_message_add')
        for fuzz in FUZZ_STRINGS:
            with self.subTest(fuzz=repr(fuzz)):
                response = self.client.post(url, {
                    'email': self.email.pk,
                    'content': fuzz,
                    'send_date': date.today().isoformat(),
                    'send_time': '10:00:00',
                    'sender_type': 'admin',
                })
                self.assertNotEqual(response.status_code, 500)

    def test_create_message_fuzz_sender_type(self):
        url = reverse('admin:messaging_message_add')
        for sender in ['admin', 'patient', '', 'unknown', '<script>', '123']:
            with self.subTest(sender=sender):
                response = self.client.post(url, {
                    'email': self.email.pk,
                    'content': 'Test message',
                    'send_date': date.today().isoformat(),
                    'send_time': '10:00:00',
                    'sender_type': sender,
                })
                self.assertNotEqual(response.status_code, 500)
