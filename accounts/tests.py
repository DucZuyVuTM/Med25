import random
import string
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Administrator, Doctor, Employee, Position


User = get_user_model()


def rand_str(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def rand_phone():
    return '+84' + ''.join(random.choices(string.digits, k=9))


FUZZ_STRINGS = [
    '', 'a' * 1000, '<script>alert(1)</script>',
    "'; DROP TABLE accounts_employee; --", '\x00\x01\x02',
    '../../../etc/passwd', '%s %s %s', '\n\r\t', '0', '-1',
    '99999999999999999999',
]

# Create your tests here.
class AdminFuzzBase(TestCase):
    """Base class with common setup for all admin fuzz tests."""

    @classmethod
    def setUpTestData(cls):
        # Clean up existing test data
        Doctor.objects.all().delete()
        Administrator.objects.all().delete()
        Employee.objects.all().delete()
        User.objects.filter(username__startswith='test').delete()
        User.objects.filter(username='superadmin').delete()

        # Create superuser
        cls.superuser = User.objects.create_superuser(
            username='superadmin',
            password='superpassword123',
            email='super@med25.com',
        )
        
        # Create default position
        cls.position = Position.objects.create(
            title='Test Position',
            salary=Decimal('5000000'),
            access_category='Basic',
        )

    def setUp(self):
        """Login before each test."""
        self.client.login(username='superadmin', password='superpassword123')

    def assertNoServerError(self, response, url=''):
        self.assertNotEqual(response.status_code, 500, f'Server error at {url}')


class PositionAdminFuzzTest(AdminFuzzBase):
    """Fuzz tests for Position admin."""

    def test_create_position_valid(self):
        url = reverse('admin:accounts_position_add')
        response = self.client.post(url, {
            'title': 'Pediatrician',
            'salary': '8000000',
            'access_category': 'Level 2',
        })
        self.assertIn(response.status_code, [200, 302])

    def test_create_position_fuzz_title(self):
        url = reverse('admin:accounts_position_add')
        for fuzz in FUZZ_STRINGS:
            with self.subTest(fuzz=repr(fuzz)):
                response = self.client.post(url, {
                    'title': fuzz,
                    'salary': '5000000',
                    'access_category': 'Basic',
                })
                self.assertNoServerError(response, url)

    def test_create_position_fuzz_salary(self):
        url = reverse('admin:accounts_position_add')
        salary_cases = ['0', '-1', '99999999999', 'abc', '', '1.5']
        for salary in salary_cases:
            with self.subTest(salary=salary):
                response = self.client.post(url, {
                    'title': rand_str(),
                    'salary': salary or '0',
                    'access_category': 'Basic',
                })
                self.assertNoServerError(response, url)


class EmployeeAdminFuzzTest(AdminFuzzBase):
    """Fuzz tests for Employee admin."""

    def test_create_employee_valid(self):
        url = reverse('admin:accounts_employee_add')
        new_user = User.objects.create_user(
            username=rand_str(), 
            password='pass123', 
            role='doctor'
        )
        response = self.client.post(url, {
            'user': new_user.pk,
            'position': self.position.pk,
            'employment_date': date.today().isoformat(),
            'contract_end_date': (date.today() + timedelta(days=365)).isoformat(),
        })
        self.assertNoServerError(response, url)

    def test_create_employee_fuzz_dates(self):
        url = reverse('admin:accounts_employee_add')
        date_cases = ['2099-01-01', '1900-01-01', 'not-a-date', '', '2024-13-45']
        for date_value in date_cases:
            with self.subTest(date=date_value):
                new_user = User.objects.create_user(
                    username=rand_str(), 
                    password='pass123'
                )
                response = self.client.post(url, {
                    'user': new_user.pk,
                    'position': self.position.pk,
                    'employment_date': date_value,
                    'contract_end_date': date_value,
                })
                self.assertNoServerError(response, url)


class DoctorAdminFuzzTest(AdminFuzzBase):
    """Fuzz tests for Doctor admin."""

    def setUp(self):
        super().setUp()
        # Create fresh doctor data for each test
        self.doctor_user = User.objects.create_user(
            username=rand_str(),  # Unique username each time
            password='pass123',
            role='doctor'
        )
        
        # Use get_or_create to avoid signal conflicts
        self.doctor_employee, _ = Employee.objects.get_or_create(
            user=self.doctor_user,
            defaults={
                'position': self.position,
                'employment_date': date.today(),
                'contract_end_date': date.today() + timedelta(days=365),
            }
        )
        
        self.doctor, _ = Doctor.objects.get_or_create(
            employee=self.doctor_employee,
            defaults={
                'speciality': 'General',
                'work_experience': '5 years',
            }
        )

    def test_edit_doctor_fuzz_speciality(self):
        url = reverse('admin:accounts_doctor_change', args=[self.doctor.pk])
        for fuzz in FUZZ_STRINGS:
            with self.subTest(fuzz=repr(fuzz)):
                response = self.client.post(url, {
                    'employee': self.doctor_employee.pk,
                    'speciality': fuzz,
                    'work_experience': 'Updated',
                })
                self.assertNoServerError(response, url)

    def test_edit_doctor_fuzz_experience(self):
        url = reverse('admin:accounts_doctor_change', args=[self.doctor.pk])
        for fuzz in FUZZ_STRINGS:
            with self.subTest(fuzz=repr(fuzz)):
                response = self.client.post(url, {
                    'employee': self.doctor_employee.pk,
                    'speciality': 'Cardiology',
                    'work_experience': fuzz,
                })
                self.assertNoServerError(response, url)


class AdministratorAdminFuzzTest(AdminFuzzBase):
    """Fuzz tests for Administrator admin."""

    def setUp(self):
        super().setUp()
        # Create fresh administrator data for each test
        self.admin_user = User.objects.create_user(
            username=rand_str(),
            password='pass123',
            role='administrator'
        )
        
        self.admin_employee, _ = Employee.objects.get_or_create(
            user=self.admin_user,
            defaults={
                'position': self.position,
                'employment_date': date.today(),
                'contract_end_date': date.today() + timedelta(days=365),
            }
        )
        
        self.administrator, _ = Administrator.objects.get_or_create(
            employee=self.admin_employee,
            defaults={
                'system_access_rights': 'Full',
            }
        )

    def test_edit_administrator_fuzz_access_rights(self):
        url = reverse('admin:accounts_administrator_change', args=[self.administrator.pk])
        for fuzz in FUZZ_STRINGS:
            with self.subTest(fuzz=repr(fuzz)):
                response = self.client.post(url, {
                    'employee': self.admin_employee.pk,
                    'system_access_rights': fuzz,
                })
                self.assertNoServerError(response, url)
