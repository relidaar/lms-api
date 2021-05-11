# Generated by Django 3.1.8 on 2021-05-11 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms_core', '0008_auto_20210511_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonperiodiceventdetails',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='non_periodic_event_details', to='lms_core.event'),
        ),
        migrations.AlterField(
            model_name='periodiceventdetails',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_event_details', to='lms_core.event'),
        ),
    ]