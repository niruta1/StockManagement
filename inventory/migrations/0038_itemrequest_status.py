# Generated by Django 4.0.4 on 2022-07-06 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0037_rename_date_of_purchase_itemrequest_date_of_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemrequest',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
