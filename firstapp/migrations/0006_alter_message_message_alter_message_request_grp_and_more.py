# Generated by Django 4.2 on 2024-07-03 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0005_message_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='request_grp',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='room_name',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='username',
            field=models.CharField(max_length=400, null=True),
        ),
    ]