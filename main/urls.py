from django.urls import path

from .views import home, about_us, courses, classes

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('about-us', about_us, name='about_us'),
    path('courses/', courses, name='courses'),
    path('classes/', classes, name='classes'),
]
