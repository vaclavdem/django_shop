# Generated by Django 3.2.5 on 2021-08-27 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('comment', models.TextField(default='', max_length=5000, verbose_name='Коментарий')),
                ('order', models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='order.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Жалоба',
                'verbose_name_plural': 'Жалобы',
            },
        ),
    ]
