from rest_framework import generics

from .models import Course, CourseClass
from .serializers import CourseSerializer, CourseClassSerializer


# Create your views here.
class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'


class CourseClassList(generics.ListCreateAPIView):
    serializer_class = CourseClassSerializer

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
