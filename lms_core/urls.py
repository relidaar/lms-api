from rest_framework.routers import DefaultRouter

from lms_core.views import (
    CourseViewSet, RequestViewSet, ResponseViewSet, StudentGroupViewSet,
    TimetableViewSet, EventTypeViewSet, EventViewSet,
)

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('student-groups', StudentGroupViewSet,
                basename='student-group')
router.register('timetables', TimetableViewSet, basename='timetable')
router.register('events', EventViewSet, basename='event')
router.register('event-types', EventTypeViewSet, basename='event-type')
router.register('requests', RequestViewSet, basename='request')
router.register('responses', ResponseViewSet, basename='response')

urlpatterns = [
] + router.urls
