from django.contrib import admin

from lms_core.models import Course, StudentGroup, Timetable, PeriodicEvent, NonPeriodicEvent, EventType


class RequestAdmin(admin.ModelAdmin):
    list_display = ('status', 'created_date', 'modified_date',
                    'created_by', 'modified_by', 'uuid',)
    search_fields = ('status', 'uuid',)
    ordering = ('status')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'uuid',)
    search_fields = ('code', 'title', 'uuid',)
    ordering = ('code',)


@admin.register(StudentGroup)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'uuid',)
    search_fields = ('code', 'uuid',)
    ordering = ('code',)


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'get_course_code', 'uuid',)
    search_fields = ('code', 'title', 'get_course_code', 'uuid',)

    def get_course_code(self, obj):
        return obj.course.code
    get_course_code.short_description = 'Course'
    get_course_code.admin_filter_field = 'code'


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'get_course_code',
                    'get_instructor', 'uuid',)
    search_fields = ('title', 'event_type', 'get_course_code',
                     'get_instructor', 'uuid',)
    list_filter = ('event_type',)

    def get_course_code(self, obj):
        return obj.timetable.course.code
    get_course_code.short_description = 'Course'
    get_course_code.admin_filter_field = 'code'

    def get_instructor(self, obj):
        return obj.instructor.user.full_name
    get_instructor.short_description = 'Instructor'
    get_instructor.admin_filter_field = 'full_name'


@admin.register(PeriodicEvent)
class PeriodicEventAdmin(EventAdmin):
    pass


@admin.register(NonPeriodicEvent)
class NonPeriodicEventAdmin(EventAdmin):
    pass


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'uuid',)
    search_fields = ('title', 'uuid',)
    ordering = ('title',)
