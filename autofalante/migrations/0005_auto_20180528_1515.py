# Generated by Django 2.0.5 on 2018-05-28 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autofalante', '0004_auto_20180528_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='musica',
            name='executing',
        ),
        migrations.AddField(
            model_name='musica',
            name='execute',
            field=models.BooleanField(default=0, editable=False, verbose_name='Execução foi pedida'),
            preserve_default=False,
        ),
    ]
