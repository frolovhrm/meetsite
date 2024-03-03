# Generated by Django 4.2.4 on 2024-02-21 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetplan', '0006_alter_meeting_options_remove_meeting_planned_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateplan', models.DateTimeField(verbose_name='Дата')),
                ('listplan', models.JSONField(null=True, verbose_name='Список запланированных встреч')),
            ],
            options={
                'verbose_name': 'Дата',
                'verbose_name_plural': 'Даты',
                'ordering': ['dateplan'],
            },
        ),
        migrations.RemoveField(
            model_name='param',
            name='numofroom',
        ),
        migrations.RemoveField(
            model_name='param',
            name='roomlist',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='plan',
        ),
    ]