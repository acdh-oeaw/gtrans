# Generated by Django 2.1.7 on 2019-10-26 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NetVisCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=250)),
                ('model_name', models.CharField(blank=True, max_length=250)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('graph_data', models.TextField(blank=True)),
                ('graph_data_preview', models.TextField(blank=True)),
            ],
        ),
    ]
