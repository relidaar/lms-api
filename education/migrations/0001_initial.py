# Generated by Django 3.1.8 on 2021-05-12 13:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0009_studentgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('syllabus', models.TextField(blank=True)),
                ('instructors', models.ManyToManyField(related_name='instructed_courses', to='accounts.InstructorProfile')),
                ('student_groups', models.ManyToManyField(related_name='joined_courses', to='accounts.StudentGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('start_date', models.DateField(verbose_name='Course start date')),
                ('end_date', models.DateField(verbose_name='Course end date')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetables', to='education.course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PeriodicEventDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('start_time', models.TimeField(verbose_name='Event start time')),
                ('end_time', models.TimeField(verbose_name='Event end time')),
                ('weekday', models.CharField(choices=[('MO', 'Monday'), ('TU', 'Tuesday'), ('WE', 'Wednesday'), ('TH', 'Thursday'), ('FR', 'Friday'), ('SA', 'Saturday'), ('SU', 'Sunday')], default='MO', max_length=2)),
                ('repeat_type', models.CharField(choices=[('W', 'Weekly'), ('E', 'Even'), ('O', 'Odd')], default='W', max_length=1)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_event_details', to='education.event')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.instructorprofile')),
                ('students', models.ManyToManyField(to='accounts.StudentProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NonPeriodicEventDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('start_time', models.TimeField(verbose_name='Event start time')),
                ('end_time', models.TimeField(verbose_name='Event end time')),
                ('date', models.DateTimeField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='non_periodic_event_details', to='education.event')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.instructorprofile')),
                ('students', models.ManyToManyField(to='accounts.StudentProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.eventtype'),
        ),
        migrations.AddField(
            model_name='event',
            name='timetable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.timetable'),
        ),
    ]