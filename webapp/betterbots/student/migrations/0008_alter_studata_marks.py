# Generated by Django 4.0.6 on 2022-08-18 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_studata_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studata',
            name='marks',
            field=models.TextField(default='', max_length=3, verbose_name='marks'),
        ),
    ]
