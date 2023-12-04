from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from courses.models import Course, CourseClass


class CourseClassDetailTest(APITestCase):
    """Test for CourseClassDetail view."""

    def setUp(self):
        self.client = APIClient()
        self.author_user = User.objects.create_user(username='author',
                                                    password='testpass123')
        self.course = Course.objects.create(title='Test Course',
                                            slug='test-course')
        self.course.authors.set([self.author_user])
        self.course_class = CourseClass.objects.create(title='Test Class',
                                                       slug='test-class',
                                                       course=self.course)
        self.client.force_authenticate(user=self.author_user)
        self.url = reverse('course:course_class_detail',
                           kwargs={'slug': self.course_class.slug})

    def test_retrieve_course_class(self):
        """Test retrieving a course class."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.course_class.title)

    def test_update_course_class(self):
        """Test updating a course class."""
        payload = {'title': 'Updated Class'}
        response = self.client.patch(self.url, payload)

        self.course_class.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.course_class.title, 'Updated Class')

    def test_delete_course_class(self):
        """Test deleting a course class."""
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CourseClass.objects.count(), 0)

    def test_retrieve_course_class_unauthorized_user(self):
        """Test retrieving a course class with an unauthorized user."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_course_class_unauthorized_user(self):
        """Test updating a course class with an unauthorized user."""
        self.client.force_authenticate(user=None)
        payload = {'title': 'Updated Class'}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_course_class_unauthorized_user(self):
        """Test deleting a course class with an unauthorized user."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_course_class_non_owner_user(self):
        """Test updating a course class with a user who is not an owner."""
        non_author_user = User.objects.create_user(username='nonauthor',
                                                   password='testpass123')
        self.client.force_authenticate(user=non_author_user)
        payload = {'title': 'Updated Class'}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
