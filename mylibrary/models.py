from django.db import models
from datetime import datetime


class User(models.Model):
    """
    用户表
    """
    id = models.CharField(verbose_name='用户名', max_length=8, primary_key=True)
    name = models.CharField(verbose_name='姓名', max_length=30)
    password = models.CharField(verbose_name='密码', max_length=64)
    major = models.CharField(verbose_name='专业', max_length=80, default='null')
    research_direction = models.CharField(verbose_name='研究方向', max_length=80, default='计算机')
    tag_list = models.JSONField(verbose_name='标签集合', max_length=80, default='[]')
    is_admin = models.BooleanField(verbose_name='是否为管理员', max_length=80, default=False)
    borrowed_books = models.ManyToManyField('Book', verbose_name='借阅书籍', through='Borrow')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.id) + " " + self.name


class Book(models.Model):
    """
    书目表
    """
    id = models.AutoField(verbose_name='书号', primary_key=True)
    name = models.CharField(verbose_name='书名', max_length=60)
    author = models.CharField(verbose_name='作者', max_length=60)
    publisher = models.CharField(verbose_name='出版社', max_length=60)
    category = models.CharField(verbose_name='图书种类', max_length=60, default='计算机')
    tag_list = models.JSONField(verbose_name='标签集合', max_length=3000, default='[]')
    is_available = models.BooleanField(verbose_name='是否可借', default=True)

    class Meta:
        verbose_name = '书目'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.id) + " " + self.name


class Borrow(models.Model):
    """
    借阅关系表
    """
    id = models.AutoField(verbose_name='序号', primary_key=True)
    user = models.ForeignKey(User, verbose_name='借阅者', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='所借书籍', on_delete=models.CASCADE)
    borrow_time = models.DateTimeField(verbose_name='借出时间', default=datetime.now())
    return_ddl = models.DateTimeField(verbose_name='归还期限', default=datetime.now())

    class Meta:
        verbose_name = '借阅关系'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return '{} borrowed {} at {}'.format(self.user, self.book, self.borrow_time)


class BorrowReview(models.Model):
    """
    借阅后评分
    """
    id = models.AutoField(verbose_name='序号', primary_key=True)
    user = models.ForeignKey(User, verbose_name='借阅者', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='所借书籍', on_delete=models.CASCADE)
    star = models.IntegerField(verbose_name='书籍评分', default=0)

    class Meta:
        verbose_name = '借阅书籍评分'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return '{} review {} at {}'.format(self.user, self.book, self.star)


class Log(models.Model):
    """
    日志表
    """
    id = models.AutoField(verbose_name='序号', primary_key=True)
    time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='相关书籍', on_delete=models.CASCADE, null=True)
    action = models.CharField(verbose_name='操作', max_length=30)

    class Meta:
        verbose_name = '日志'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return '[{}] {} {} {}'.format(self.time, self.user, self.action, self.book)
