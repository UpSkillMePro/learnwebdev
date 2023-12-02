from django.urls import path
from courses import views

app_name = 'course'

urlpatterns = [
    path('courses/',
         views.CourseList.as_view(),
         name='course_list'),
    path('courses/<slug:slug>/',
         views.CourseDetail.as_view(),
         name='course_detail'),
    path('courses/<slug:course>/classes/',
         views.CourseClassList.as_view(),
         name='course_class_list'),
    path('classes/<slug:slug>/',
         views.CourseClassDetail.as_view(),
         name='course_class_detail'),
]
