# Generated by Django 2.0.5 on 2018-05-26 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autofalante', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='musica',
            name='executing',
            field=models.BooleanField(default=0, verbose_name='Na fila de execução'),
            preserve_default=False,
        ),
    ]
