# Generated by Django 5.0.2 on 2024-03-01 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quarterback_simulation', '0002_delete_quarterbacksearch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quarterback',
            name='coach',
        ),
        migrations.RemoveField(
            model_name='quarterback',
            name='skillset',
        ),
        migrations.RemoveField(
            model_name='quarterback',
            name='team',
        ),
        migrations.RemoveField(
            model_name='halloffame',
            name='quarterback',
        ),
        migrations.RemoveField(
            model_name='quarterback',
            name='age',
        ),
        migrations.RemoveField(
            model_name='quarterback',
            name='experience',
        ),
        migrations.DeleteModel(
            name='Coach',
        ),
        migrations.DeleteModel(
            name='Skillset',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]