from django.db.models import Count
from django.shortcuts import render

from courses.models import Course, CourseClass


# Create your views here.
def home(request):
    context = {
        'title': 'Welcome to the best Django Tutorials'
    }
    return render(request, 'pages/home.html', context)


# Create your views here.
def about_us(request):
    context = {
        'title': 'About Us'
    }
    return render(request, 'pages/about_us.html', context)


def courses(request):
    """Display a list of published courses

    :param request:
    :return:
    """
    context = {
        'courses': Course.objects.prefetch_related('classes', 'subscriptions').all()
    }

    return render(request, 'pages/courses.html', context)


def classes(request):
    """Display a list of classes

    :param request:
    :return:
    """
    context = {
        'classes': CourseClass.objects.select_related('course').all()
    }

    return render(request, 'pages/classes.html', context)


def show_course(request, slug):
    """Display individual course

    :param request:
    :param slug:
    :return:
    """
    course = Course.objects.filter(slug=slug).get()
    context = {
        'course': course,
        'is_subscribed': course.has_subscription(request.user),
        'is_author': course.is_author(request.user)
    }

    return render(request, 'pages/course.html', context)
