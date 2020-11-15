# Generated by Django 2.2.15 on 2020-11-14 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userextensions', '0004_serviceaccount_serviceaccounttokenhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceaccount',
            name='admin_enabled',
            field=models.BooleanField(default=True, help_text='admin enable/disable state of service account'),
        ),
        migrations.AlterField(
            model_name='serviceaccount',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='serviceaccount',
            name='enabled',
            field=models.BooleanField(default=True, help_text='owner enable/disable state of service account'),
        ),
        migrations.AlterField(
            model_name='serviceaccount',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='theme',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='theme',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userfavorite',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userfavorite',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userrecent',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userrecent',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
