# Generated by Django 3.2.5 on 2021-07-28 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_alter_status_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
