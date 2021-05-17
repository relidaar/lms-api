# Generated by Django 3.1.8 on 2021-05-17 11:26

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_studentgroup'),
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_time', models.TimeField(verbose_name='Course event start time')),
                ('end_time', models.TimeField(verbose_name='Course event end time')),
                ('date', models.DateTimeField()),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.instructorprofile')),
                ('students', models.ManyToManyField(to='accounts.StudentProfile')),
                ('timetable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to='education.timetable')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='nonperiodiceventdetails',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.instructorprofile'),
        ),
        migrations.AlterField(
            model_name='periodiceventdetails',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.instructorprofile'),
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='education.assignment')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solutions', to='accounts.studentprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True)),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='grades', to='accounts.instructorprofile')),
                ('solution', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='education.solution')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]