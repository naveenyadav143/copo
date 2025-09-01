from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Course, CO, PO, COPOMapping, COAttainment, Student
from django.contrib.auth import get_user_model

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Computer Science',
            user=self.user
        )
        self.co = CO.objects.create(
            course=self.course,
            number='CO1',
            description='Understand basic programming concepts',
            max_score=100
        )
        self.po = PO.objects.create(
            number='PO1',
            description='Apply knowledge of computing and mathematics'
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_add_course_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('add_course'))
        self.assertEqual(response.status_code, 200)

    def test_courses_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)

    def test_add_co_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('add_co'))
        self.assertEqual(response.status_code, 200)

    def test_add_po_view(self):
        response = self.client.get(reverse('add_po'))
        self.assertEqual(response.status_code, 200)

    def test_add_mapping_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('add_mapping'))
        self.assertEqual(response.status_code, 200)

    def test_upload_marks_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('upload_marks'))
        self.assertEqual(response.status_code, 200)

    def test_co_attainment_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('co_attainment'))
        self.assertEqual(response.status_code, 200)

    def test_po_attainment_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('po_attainment'))
        self.assertEqual(response.status_code, 200)

    def test_login_redirect(self):
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_login_success(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)

    def test_url_routing(self):
        # Test all URLs are accessible
        urls = [
            'home',
            'register',
            'login',
            'add_course',
            'courses',
            'add_co',
            'add_po',
            'add_mapping',
            'upload_marks',
            'co_attainment',
            'po_attainment'
        ]
        
        for url_name in urls:
            try:
                response = self.client.get(reverse(url_name))
                self.assertIn(response.status_code, [200, 302])
            except Exception as e:
                self.fail(f"URL {url_name} failed: {e}")
