# Generated by Django 3.1.8 on 2021-05-12 13:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210430_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('students', models.ManyToManyField(related_name='groups', to='accounts.StudentProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
