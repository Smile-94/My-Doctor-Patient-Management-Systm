# Generated by Django 3.2 on 2022-10-27 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('age', models.IntegerField(default=0)),
                ('village', models.CharField(blank=True, max_length=50)),
                ('post_office', models.CharField(blank=True, max_length=50)),
                ('police_station', models.CharField(blank=True, max_length=50)),
                ('district', models.CharField(blank=True, max_length=50)),
                ('post_code', models.IntegerField(blank=True, default=0)),
                ('marital_status', models.CharField(choices=[('Married', 'Married'), ('Unmarrid', 'Unmarrid')], default='No', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
