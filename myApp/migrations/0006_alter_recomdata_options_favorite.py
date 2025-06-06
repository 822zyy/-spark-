# Generated by Django 5.1.7 on 2025-03-20 07:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0005_alter_recomdata_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recomdata',
            options={'managed': False},
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='myApp.recomdata')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='myApp.user')),
            ],
            options={
                'db_table': 'favorite',
                'unique_together': {('user', 'job')},
            },
        ),
    ]
