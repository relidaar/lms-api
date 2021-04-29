from rest_framework.routers import SimpleRouter

from lms_core.views import CourseViewSet, RequestViewSet, StudentGroupViewSet, TimetableViewSet, PeriodicEventViewSet, \
    NonPeriodicEventViewSet, EventTypeViewSet

router = SimpleRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('student-groups', StudentGroupViewSet,
                basename='student-group')
router.register('timetables', TimetableViewSet, basename='timetable')
router.register('periodic-events', PeriodicEventViewSet,
                basename='periodic-event')
router.register('nonperiodic-events', NonPeriodicEventViewSet,
                basename='nonperiodic-event')
router.register('event-types', EventTypeViewSet, basename='event-type')
router.register('requests', RequestViewSet, basename='request')

urlpatterns = [
] + router.urls
