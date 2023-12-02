from django.contrib import admin

from courses.models import CourseClass, Course, CourseSubscription


class CourseSubscriptionsInline(admin.TabularInline):
    model = CourseSubscription
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    def num_of_classes(self, obj):
        return obj.classes.all().count()

    list_display = ('title', 'short_desc', 'price', 'num_of_classes')

    fieldsets = [
        ("Basic", {
            "fields": ['title', 'slug', 'price', 'status', 'thumbnail',
                       'video']
        }),
        ("Description", {
            "fields": ['short_desc', 'desc']
        }),
        ("Authors", {
            "fields": ['authors']
        })
    ]

    inlines = [
        CourseSubscriptionsInline
    ]


@admin.register(CourseClass)
class CourseClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'short_desc')

    fieldsets = [
        ("Basic", {
            "fields": ['title', 'slug', 'course', 'is_free']
        }),
        ("Description", {
            "fields": ['short_desc', 'desc']
        }),
    ]
