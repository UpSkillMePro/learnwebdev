from rest_framework import serializers
from .models import Course, CourseClass


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'short_desc', 'desc', 'price', 'slug')


class CourseClassSerializer(serializers.HyperlinkedModelSerializer):
    course_slug = serializers.SlugRelatedField(
        read_only=True,
        source='course',
        slug_field='slug'
    )

    course = serializers.HyperlinkedRelatedField(
        view_name='course:course_detail',
        read_only=True,
        lookup_field='slug'
    )

    class Meta:
        model = CourseClass
        fields = ('course_slug', 'title', 'short_desc',
                  'desc', 'slug', 'course')
        read_only_fields = ['course', ]
