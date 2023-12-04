from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from courses.models import Course, CourseClass


class CourseClassListTest(APITestCase):
    """Test for CourseClassList view."""

    def setUp(self):
        self.client = APIClient()
        self.author_user = User.objects.create_user(username='author',
                                                    password='testpass123')
        self.course = Course.objects.create(title='Test Course',
                                            slug='test-course')
        self.course.authors.set([self.author_user])
        self.client.force_authenticate(user=self.author_user)
        self.url = reverse('course:course_class_list',
                           kwargs={'course': self.course.slug})

    def test_list_course_classes(self):
        """Test listing course classes."""
        CourseClass.objects.create(title='Test Class', course=self.course)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_course_class(self):
        """Test creating a new course class."""
        payload = {
            'title': 'New Class',
            'slug': 'new-class',
            'course': self.course.slug
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CourseClass.objects.count(), 1)
        self.assertEqual(CourseClass.objects.get().title, 'New Class')

    def test_list_course_classes_unauthorized_user(self):
        """Test listing course classes with an unauthorized user."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_course_class_unauthorized_user(self):
        """Test creating a course class with an unauthorized user."""
        self.client.force_authenticate(user=None)
        payload = {'title': 'New Class', 'course': self.course.id}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_course_class_non_owner_user(self):
        """Test creating a course class with a user who is not an owner."""
        non_author_user = User.objects.create_user(username='nonauthor',
                                                   password='testpass123')
        self.client.force_authenticate(user=non_author_user)
        payload = {'title': 'New Class', 'course': self.course.id}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
