from rest_framework.routers import DefaultRouter

from api.accounts.views import (
    UserViewSet,
    GroupViewSet,
    PermissionViewSet,
    StudentProfileViewSet,
    InstructorProfileViewSet,
    StudentGroupViewSet,
)
from api.education.views import (
    AssignmentViewSet,
    CourseViewSet,
    GradeViewSet,
    SolutionViewSet,
    TimetableViewSet,
    EventTypeViewSet,
    EventViewSet,
)
from api.management.views import RequestViewSet, ResponseViewSet

router = DefaultRouter()
router.get_api_root_view().cls.__name__ = 'Api v1'
router.get_api_root_view().cls.__doc__ = ''

router.register('users', UserViewSet, basename='user')
router.register('groups', GroupViewSet, basename='group')
router.register('permissions', PermissionViewSet, basename='permission')
router.register('students', StudentProfileViewSet, basename='student')
router.register('instructors', InstructorProfileViewSet, basename='instructor')
router.register('student-groups', StudentGroupViewSet,
                basename='student-group')

router.register('courses', CourseViewSet, basename='course')
router.register('timetables', TimetableViewSet, basename='timetable')
router.register('assignments', AssignmentViewSet, basename='assignment')
router.register('solutions', SolutionViewSet, basename='solution')
router.register('grades', GradeViewSet, basename='grade')

router.register('events', EventViewSet, basename='event')
router.register('event-types', EventTypeViewSet, basename='event-type')

router.register('requests', RequestViewSet, basename='request')
router.register('responses', ResponseViewSet, basename='response')
