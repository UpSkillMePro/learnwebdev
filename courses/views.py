from rest_framework import generics, authentication, permissions

from .models import Course, CourseClass
from .serializers import CourseSerializer, CourseClassSerializer


class IsCourseOwnedBy(permissions.BasePermission):
    message = {'detail': 'You must be the owner of this course.'}

    def has_object_permission(self, request, view, obj):
        return request.user in obj.authors.all()


class IsClassCourseOwnedBy(permissions.BasePermission):
    message = {'detail': 'You must be the owner of this course.'}

    def has_permission(self, request, view):
        course_slug = view.kwargs['course']

        try:
            course = Course.objects.get(slug=course_slug)
        except Course.DoesNotExist:
            return False

        return request.user in course.authors.all()


class IsClassOwnedBy(permissions.BasePermission):
    message = {'detail': 'You must be the owner of this course.'}

    def has_object_permission(self, request, view, obj):
        return request.user in obj.course.authors.all()


class IsAuthor(permissions.BasePermission):
    message = {'detail': 'You must be a author to do this.'}

    def has_permission(self, request, view):
        group_name = "Author"  # Set your group name here
        return request.user.groups.filter(name=group_name).exists()


# Create your views here.
class CourseList(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def get_queryset(self):
        author = self.request.user
        return author.courses.all()


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsCourseOwnedBy]


# 1277631c31e7f2a809ce2ed8c95160289ff6439c

class CourseClassList(generics.ListCreateAPIView):
    serializer_class = CourseClassSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsClassCourseOwnedBy]

    def get_queryset(self):
        course = self.kwargs['course']
        return CourseClass.objects.filter(course__slug=course)

    def perform_create(self, serializer):
        course = Course.objects.get(slug=self.kwargs['course'])
        serializer.save(course=course)


class CourseClassDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseClass.objects.all()
    serializer_class = CourseClassSerializer
    lookup_field = 'slug'
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsClassOwnedBy]
