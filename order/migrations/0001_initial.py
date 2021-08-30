# Generated by Django 3.2.5 on 2021-08-27 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_price', models.FloatField(default=0, verbose_name='Общая цена')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveIntegerField(default=2, verbose_name='Id пользователя')),
                ('qty', models.PositiveIntegerField(default=1, verbose_name='Кол-во')),
                ('final_price', models.FloatField(default=0, verbose_name='Общая цена')),
                ('food', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='food.food', verbose_name='Статус')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Продукт для корзины',
                'verbose_name_plural': 'Продукты для корзины',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Статус заказа')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.CreateModel(
            name='Small_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('fromm', models.TextField(default='', max_length=100, verbose_name='Адресс')),
                ('to', models.TextField(max_length=100, verbose_name='Адрес доставки')),
                ('comment', models.TextField(default='', max_length=5000, verbose_name='Коментарий')),
                ('final_price', models.FloatField(default=0, verbose_name='Общая цена')),
                ('is_active', models.BooleanField(default=False, verbose_name='Доставить')),
                ('is_delivered', models.BooleanField(default=False, verbose_name='Доставлен')),
                ('delivered_at', models.FloatField(default=0, verbose_name='Дата доставки')),
                ('cart_product', models.ManyToManyField(blank=True, to='order.CartProduct', verbose_name='Еда')),
                ('delivery', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Delivery', to='food.users', verbose_name='Доставщик')),
                ('restaurant', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='food.restaurant', verbose_name='Рестораны')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='order.status', verbose_name='Статус')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='User', to='food.users', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Раздробленный заказ',
                'verbose_name_plural': 'Раздробленные заказы',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('to', models.TextField(max_length=100, verbose_name='Адрес доставки')),
                ('comment', models.TextField(default='', max_length=5000, verbose_name='Коментарий')),
                ('final_price', models.FloatField(default=0, verbose_name='Общая цена')),
                ('cart', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='order.cart', verbose_name='Корзина')),
                ('restaurants', models.ManyToManyField(blank=True, to='food.Restaurant', verbose_name='Рестораны')),
                ('small_order', models.ManyToManyField(blank=True, default=1, to='order.Small_order', verbose_name='Раздробленные заказы')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='food.users', verbose_name='Пользователь')),
                ('view_cart', models.ManyToManyField(blank=True, to='order.CartProduct', verbose_name='Еда')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='food',
            field=models.ManyToManyField(blank=True, related_name='related_cart', to='order.CartProduct', verbose_name='Еда'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='food.users', verbose_name='Пользователь'),
        ),
    ]
