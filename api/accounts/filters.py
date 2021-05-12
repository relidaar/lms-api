from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from django.db.models import Q

from accounts.models import InstructorProfile, StudentProfile, StudentGroup


class UserProfileFilter(filters.FilterSet):
    user = filters.ModelChoiceFilter(
        label='User',
        field_name='uuid',
        to_field_name='uuid',
        queryset=get_user_model().objects.all(),
    )

    class Meta:
        abstract = True
        fields = ('user', 'user__full_name', 'user__email',)


class StudentProfileFilter(UserProfileFilter):
    class Meta:
        model = StudentProfile
        fields = UserProfileFilter.Meta.fields + ()


class InstructorProfileFilter(UserProfileFilter):
    class Meta:
        model = InstructorProfile
        fields = UserProfileFilter.Meta.fields + ()


class StudentGroupFilter(filters.FilterSet):
    students = filters.ModelMultipleChoiceFilter(
        label='Students',
        field_name='uuid',
        to_field_name='uuid',
        queryset=StudentProfile.objects.all(),
    )

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)

        students = StudentProfile.objects.filter(user=user)

        if not students:
            return parent

        student = students.first()
        return parent.filter(students=student)

    class Meta:
        model = StudentGroup
        fields = ('code', 'students',)
