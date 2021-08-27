# Generated by Django 3.2.5 on 2021-07-28 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            ],
            options={
                'verbose_name': 'Продукт для корзины',
                'verbose_name_plural': 'Продукты для корзины',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Discounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Тип скидки',
                'verbose_name_plural': 'Типы скидок',
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
                ('cart', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.cart', verbose_name='Корзина')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('title', models.CharField(max_length=150, verbose_name='Ресторан')),
                ('cooking_time', models.CharField(max_length=100, verbose_name='Среднее время приготовления')),
                ('min_price', models.PositiveIntegerField(default=5, help_text='указывать сумму в рублях', verbose_name='Минимальная цена')),
                ('address', models.TextField(default='', max_length=100, verbose_name='Адресс')),
                ('email', models.EmailField(default='', max_length=254, verbose_name='Email')),
                ('draft', models.BooleanField(default=False, verbose_name='Черновик')),
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='Id')),
                ('category', models.ManyToManyField(to='delivery.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Ресторан',
                'verbose_name_plural': 'Рестораны',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('name', models.CharField(max_length=100, verbose_name='Статус заказа')),
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='Id')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
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
                ('cart_product', models.ManyToManyField(blank=True, to='delivery.CartProduct', verbose_name='Еда')),
                ('delivery', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Delivery', to='delivery.users', verbose_name='Доставщик')),
                ('restaurant', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.restaurant', verbose_name='Рестораны')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.status', verbose_name='Статус')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='User', to='delivery.users', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Раздробленный заказ',
                'verbose_name_plural': 'Раздробленные заказы',
            },
        ),
        migrations.AddField(
            model_name='restaurant',
            name='restaurant_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.users', verbose_name='Пользователь'),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('comment', models.TextField(default='', max_length=5000, verbose_name='Коментарий')),
                ('order', models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='delivery.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Жалоба',
                'verbose_name_plural': 'Жалобы',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='restaurants',
            field=models.ManyToManyField(blank=True, to='delivery.Restaurant', verbose_name='Рестораны'),
        ),
        migrations.AddField(
            model_name='order',
            name='small_order',
            field=models.ManyToManyField(blank=True, default=1, to='delivery.Small_order', verbose_name='Раздробленные заказы'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.users', verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='order',
            name='view_cart',
            field=models.ManyToManyField(blank=True, to='delivery.CartProduct', verbose_name='Еда'),
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Еда')),
                ('description', models.TextField(default='', verbose_name='Описание')),
                ('price', models.FloatField(default=5, help_text='указывать сумму в рублях, без скидки', verbose_name='Цена')),
                ('percent', models.PositiveIntegerField(default=0, help_text="работает тольки при типе скидке : 'Скидка'", verbose_name='Процент скидки')),
                ('discounted_price', models.FloatField(default=5, help_text='Вписать любую, потом изменится', verbose_name='Конечная цена')),
                ('restaurant', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.restaurant', verbose_name='Ресторан')),
                ('type_discount', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.discounts', verbose_name='Тип скидки')),
            ],
            options={
                'verbose_name': 'Еда',
                'verbose_name_plural': 'Еда',
            },
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='food',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.food', verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.restaurant', verbose_name='Ресторан'),
        ),
        migrations.AddField(
            model_name='cart',
            name='food',
            field=models.ManyToManyField(blank=True, related_name='related_cart', to='delivery.CartProduct', verbose_name='Еда'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='delivery.users', verbose_name='Пользователь'),
        ),
    ]