# Generated by Django 3.1.7 on 2021-03-14 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210313_2019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='uid',
            new_name='uuid',
        ),
    ]
