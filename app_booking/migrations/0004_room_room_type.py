# Generated by Django 5.0.2 on 2024-03-02 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_booking', '0003_booking_seats_booked_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('conference', 'Conference'), ('meeting', 'Meeting'), ('classroom', 'Classroom')], default='conference', max_length=20),
        ),
    ]
