# Generated by Django 4.2.9 on 2024-02-06 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0004_alter_customuser_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='nickname',
            field=models.CharField(max_length=50, verbose_name='닉네임'),
        ),
    ]
