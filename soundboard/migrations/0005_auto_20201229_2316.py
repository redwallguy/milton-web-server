# Generated by Django 3.1.3 on 2020-12-29 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    operations = [
        migrations.AlterField(
            model_name='discorduser',
            name='user_id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]