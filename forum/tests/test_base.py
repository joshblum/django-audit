from django.utils import unittest
from django.test import Client
from django.contrib.auth.models import User

class TestBase(unittest.TestCase):
    def setUp(self):
        try:
            self.user = User.objects.get(id=1) # user is already created.
        except:
            self.user = User.objects.create_user(username='john', email='lennon@thebeatles.com', password='1234')
            self.user.is_superuser = True
            self.user.is_staff = True
            self.user.save()

        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.client.login(username='john', password='1234')

    def assertAuditCreation(self, obj_type, obj_count, audit_count):
        """
            Assert that the object type was created and that audit logs were created
        """
        self.assertEqual(obj_type.objects.all().count(), obj_count)
        self.assertEqual(obj_type.audit_log.all().count(), audit_count)
        self.assertAuditDetails(obj_type)

    def assertAuditDetails(self, obj_type):
        """
            Assert that audit log details, user information and ip information are created
        """
        for i in obj_type.audit_log.all():
            self.assertEqual(i.action_user.username, "john")
            self.assertEqual(i.action_ip, "127.0.0.1")