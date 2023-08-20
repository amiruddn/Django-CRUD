# Generated by Django 4.2.4 on 2023-08-19 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='created_date',
            new_name='Created_date',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Product',
            new_name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='Note',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='Gender',
            field=models.CharField(choices=[('M', 'M'), ('F', 'F'), ('U', 'U')], max_length=1, null=True),
        ),
    ]
