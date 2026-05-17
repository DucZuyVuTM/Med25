import time
import random
import string
from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Administrator, Employee, Position


User = get_user_model()


def rand_str(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


FUZZ_STRINGS = [
    '', 'a' * 1000, '<script>alert(1)</script>',
    "'; DROP TABLE documents_document; --",
]

# Create your tests here.
class DocumentAdminFuzzTest(TestCase):
    """Fuzz tests for Document admin."""
    
    @classmethod
    def setUpTestData(cls):
        # Create superuser (general)
        cls.superuser = User.objects.create_superuser(
            username='superadmin',
            password='superpassword123',
        )
        
        # Create default position (general)
        cls.position = Position.objects.create(
            title='Admin Position',
            salary=Decimal('10000000'),
            access_category='Full',
        )
    
    def setUp(self):
        # Login before each test
        self.client.login(username='superadmin', password='superpassword123')
        
        # Create fresh administrator for each test (unique to avoid conflicts)
        unique_username = f'test_admin_{int(time.time()*1000)}_{rand_str(5)}'
        
        self.admin_user = User.objects.create_user(
            username=unique_username,
            password='pass123',
            role='administrator'
        )
        
        # Use get_or_create to avoid signal conflicts
        self.employee, _ = Employee.objects.get_or_create(
            user=self.admin_user,
            defaults={
                'position': self.position,
                'employment_date': date.today(),
                'contract_end_date': date.today(),
            }
        )
        
        self.administrator, _ = Administrator.objects.get_or_create(
            employee=self.employee,
            defaults={
                'system_access_rights': 'Full',
            }
        )
    
    def test_create_document_fuzz_content(self):
        url = reverse('admin:documents_document_add')
        for fuzz in FUZZ_STRINGS:
            with self.subTest(fuzz=repr(fuzz)):
                response = self.client.post(url, {
                    'administrator': self.administrator.pk,
                    'content': fuzz,
                    'formation_date': date.today().isoformat(),
                })
                self.assertNotEqual(response.status_code, 500, 
                                   f'Server error with fuzz: {fuzz}')
    
    def test_create_document_fuzz_date(self):
        url = reverse('admin:documents_document_add')
        date_cases = ['', 'not-a-date', '9999-99-99', '2000-01-01', 
                      '2024-13-45', '2024-02-30']
        for date_value in date_cases:
            with self.subTest(date=date_value):
                response = self.client.post(url, {
                    'administrator': self.administrator.pk,
                    'content': 'Test content',
                    'formation_date': date_value,
                })
                self.assertNotEqual(response.status_code, 500,
                                   f'Server error with date: {date_value}')
    
    def test_create_document_fuzz_long_content(self):
        """Test with extremely long content."""
        url = reverse('admin:documents_document_add')
        long_content = 'A' * 10000  # 10,000 characters
        
        response = self.client.post(url, {
            'administrator': self.administrator.pk,
            'content': long_content,
            'formation_date': date.today().isoformat(),
        })
        self.assertNotEqual(response.status_code, 500)
    
    def test_create_document_empty_content(self):
        """Test with empty content."""
        url = reverse('admin:documents_document_add')
        response = self.client.post(url, {
            'administrator': self.administrator.pk,
            'content': '',
            'formation_date': date.today().isoformat(),
        })
        # Should return 200 (form error) or 302, not 500
        self.assertNotEqual(response.status_code, 500)
