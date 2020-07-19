# Generated by Django 3.0.4 on 2020-03-11 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='书号')),
                ('name', models.CharField(max_length=50, verbose_name='书名')),
                ('author', models.CharField(max_length=30, verbose_name='作者')),
                ('publisher', models.CharField(max_length=40, verbose_name='出版社')),
            ],
            options={
                'verbose_name': '书目表',
                'verbose_name_plural': '书目表',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('borrow_date', models.DateTimeField(auto_now_add=True)),
                ('return_ddl', models.DateTimeField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mylibrary.Book')),
            ],
            options={
                'verbose_name': '借阅表',
                'verbose_name_plural': '借阅表',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='学号')),
                ('name', models.CharField(max_length=30, verbose_name='姓名')),
                ('password', models.CharField(max_length=30, verbose_name='密码')),
                ('borrowed_books', models.ManyToManyField(through='mylibrary.Borrow', to='mylibrary.Book', verbose_name='借阅书籍')),
            ],
            options={
                'verbose_name': '学生表',
                'verbose_name_plural': '学生表',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='borrow',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mylibrary.Student'),
        ),
    ]
