# Generated by Django 3.1.3 on 2020-11-29 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0003_auto_20201129_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='hashvalue',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
