# Generated by Django 4.0.4 on 2022-09-14 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_alter_buy_finalprice_alter_detailbuy_total_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailsale',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Fecha de Venta'),
        ),
    ]