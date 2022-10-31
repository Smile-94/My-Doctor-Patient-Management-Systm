# Generated by Django 3.2 on 2022-10-27 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctor_app', '0001_initial'),
        ('admin_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlineappointment',
            name='appointment_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='onlineAppointment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='doctorinfo',
            name='specialist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='specialist', to='admin_app.doctorcatagory'),
        ),
        migrations.AddField(
            model_name='doctorinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='appoint_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to=settings.AUTH_USER_MODEL),
        ),
    ]
