# Generated by Django 4.2.1 on 2023-11-29 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campanha',
            name='imagem',
            field=models.ImageField(upload_to='campanha/images/'),
        ),
    ]
