# Generated by Django 4.0.5 on 2022-07-19 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctorapp', '0008_alter_user_reg_cdate_alter_user_reg_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_reg',
            name='phone',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
