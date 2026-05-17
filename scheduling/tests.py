import time
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Position, Employee, Administrator


User = get_user_model()


FUZZ_STRINGS = [
    '', 'a' * 1000, '<script>alert(1)</script>',
    "'; DROP TABLE scheduling_schedule; --", '\x00\x01\x02',
    '../../../etc/passwd', '%s %s %s', '\n\r\t', '0', '-1',
    '99999999999999999999',
]

# Create your tests here.
class ScheduleAdminFuzzTest(TestCase):

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
            username='test_admin',
            password='pass123',
            role='administrator'
        )

        cls.employee, _ = Employee.objects.get_or_create(
            user=cls.admin_user,
            defaults={
                'position': cls.position,
                'employment_date': date.today(),
                'contract_end_date': date.today() + timedelta(days=365),
            }
        )

        cls.administrator, _ = Administrator.objects.get_or_create(
            employee=cls.employee,
            defaults={
                'system_access_rights': 'Full',
            }
        )

    def setUp(self):
        self.client.login(username='superadmin', password='superpassword123')

    def test_create_schedule_fuzz_place(self):
        url = reverse('admin:scheduling_schedule_add')
        inline_fields = {
            'receptions-TOTAL_FORMS': '0',
            'receptions-INITIAL_FORMS': '0',
            'receptions-MIN_NUM_FORMS': '0',
            'receptions-MAX_NUM_FORMS': '1000',
        }

        for fuzz in FUZZ_STRINGS:
            with self.subTest(fuzz=repr(fuzz)):
                response = self.client.post(url, {
                    'administrator': self.administrator.pk,
                    'reception_start_time': '2026-06-01 08:00:00',
                    'reception_end_time': '2026-06-01 12:00:00',
                    'reception_place': fuzz,
                    **inline_fields,
                })
                self.assertNotEqual(response.status_code, 500)

    def test_create_schedule_end_before_start(self):
        url = reverse('admin:scheduling_schedule_add')
        inline_fields = {
            'receptions-TOTAL_FORMS': '0',
            'receptions-INITIAL_FORMS': '0',
            'receptions-MIN_NUM_FORMS': '0',
            'receptions-MAX_NUM_FORMS': '1000',
        }

        response = self.client.post(url, {
            'administrator': self.administrator.pk,
            'reception_start_time': '2026-06-01 12:00:00',
            'reception_end_time': '2026-06-01 08:00:00',
            'reception_place': 'Room 1',
            **inline_fields,
        })
        self.assertNotEqual(response.status_code, 500)


class ScheduleAdminFuzzTestAlternative(TestCase):

    def setUp(self):
        super().setUp()

        self.superuser = User.objects.create_superuser(
            username='superadmin',
            password='superpassword123',
        )
        self.client.login(username='superadmin', password='superpassword123')

        self.position = Position.objects.create(
            title='Admin Position',
            salary=Decimal('10000000'),
            access_category='Full',
        )

        unique_username = f'test_admin_{int(time.time()*1000)}'
        
        self.admin_user = User.objects.create_user(
            username=unique_username,
            password='pass123',
            role='administrator'
        )

        self.employee, _ = Employee.objects.get_or_create(
            user=self.admin_user,
            defaults={
                'position': self.position,
                'employment_date': date.today(),
                'contract_end_date': date.today() + timedelta(days=365),
            }
        )
        
        self.administrator, _ = Administrator.objects.get_or_create(
            employee=self.employee,
            defaults={
                'system_access_rights': 'Full',
            }
        )
    
    def test_create_schedule_fuzz_place(self):
        url = reverse('admin:scheduling_schedule_add')
        inline_fields = {
            'receptions-TOTAL_FORMS': '0',
            'receptions-INITIAL_FORMS': '0',
            'receptions-MIN_NUM_FORMS': '0',
            'receptions-MAX_NUM_FORMS': '1000',
        }
        
        for fuzz in FUZZ_STRINGS:
            with self.subTest(fuzz=repr(fuzz)):
                response = self.client.post(url, {
                    'administrator': self.administrator.pk,
                    'reception_start_time': '2026-06-01 08:00:00',
                    'reception_end_time': '2026-06-01 12:00:00',
                    'reception_place': fuzz,
                    **inline_fields,
                })
                self.assertNotEqual(response.status_code, 500)
