from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from courses.models import Course


class CourseListTest(APITestCase):
    """Test for CourseList view."""

    def setUp(self):
        self.client = APIClient()
        self.author_user = User.objects.create_user(username='author',
                                                    password='testpass123')
        author_group, _ = Group.objects.get_or_create(name='Author')
        self.author_user.groups.add(author_group)
        self.client.force_authenticate(user=self.author_user)
        self.url = reverse('course:course_list')

    def test_list_courses(self):
        """Test listing courses for an author."""
        course = Course.objects.create(title='Test Course')
        course.authors.set([self.author_user])

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_course(self):
        """Test creating a new course."""
        payload = {
            'title': 'New Course',
            'authors': [self.author_user.id]
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().title, 'New Course')

    def test_list_courses_unauthorized_user(self):
        """Test listing courses with an unauthorized user."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_course_unauthorized_user(self):
        """Test creating a course with an unauthorized user."""
        self.client.force_authenticate(user=None)
        payload = {'title': 'New Course', 'authors': [self.author_user.id]}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_course_non_author_user(self):
        """Test creating a course with a user who is not an author."""
        non_author_user = User.objects.create_user(username='nonauthor',
                                                   password='testpass123')
        self.client.force_authenticate(user=non_author_user)
        payload = {'title': 'New Course', 'authors': [self.author_user.id]}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
