# Generated by Django 3.2.7 on 2021-10-05 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_room_host'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
    ]