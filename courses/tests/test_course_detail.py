from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from courses.models import Course


class CourseDetailTest(APITestCase):
    """Test for CourseDetail view."""

    def setUp(self):
        self.client = APIClient()
        self.author_user = User.objects.create_user(username='author',
                                                    password='testpass123')
        self.course = Course.objects.create(title='Test Course',
                                            slug='test-course')
        self.course.authors.set([self.author_user])
        self.client.force_authenticate(user=self.author_user)
        self.url = reverse('course:course_detail',
                           kwargs={'slug': self.course.slug})

    def test_retrieve_course(self):
        """Test retrieving a course."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.course.title)

    def test_update_course(self):
        """Test updating a course."""
        payload = {'title': 'Updated Course'}
        response = self.client.patch(self.url, payload)

        self.course.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.course.title, 'Updated Course')

    def test_delete_course(self):
        """Test deleting a course."""
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)

    def test_retrieve_course_unauthorized_user(self):
        """Test retrieving a course with an unauthorized user."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_course_unauthorized_user(self):
        """Test updating a course with an unauthorized user."""
        self.client.force_authenticate(user=None)
        payload = {'title': 'Updated Course'}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_course_unauthorized_user(self):
        """Test deleting a course with an unauthorized user."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_course_non_owner_user(self):
        """Test updating a course with a user who is not an owner of
        the course."""
        non_author_user = User.objects.create_user(username='nonauthor',
                                                   password='testpass123')
        self.client.force_authenticate(user=non_author_user)
        payload = {'title': 'Updated Course'}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
