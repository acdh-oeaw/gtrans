# Generated by Django 2.1.7 on 2019-10-25 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netviz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='netviscache',
            name='graph_data',
            field=models.TextField(blank=True),
        ),
    ]
