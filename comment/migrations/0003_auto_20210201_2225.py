# Generated by Django 3.1.5 on 2021-02-01 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20210201_2218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parant_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='parant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comment.comment'),
        ),
    ]
