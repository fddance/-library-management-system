# Generated by Django 3.0.4 on 2020-03-12 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mylibrary', '0003_auto_20200312_1531'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrow',
            old_name='student',
            new_name='student_id',
        ),
    ]
