from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.db.models import Q
from mylibrary.models import User, Book, Borrow, Log, BorrowReview
from mylibrary.forms import LoginForm, RegisterForm, SearchForm, BookForm
from datetime import datetime, timedelta
import hashlib


class IndexView(View):
    """
    主页
    """

    def get(self, request):
        return redirect('/login/')


class LoginView(View):
    """
    登录
    """

    def get(self, request):
        if request.session.get('is_login', None):
            if (request.session.get('is_admin', False)):
                return redirect('/book_manage/')
            else:
                return redirect('/home/')
        login_form = LoginForm()
        return render(request, 'login.html', locals())

    def post(self, request):
        login_form = LoginForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            user_id = login_form.cleaned_data['user_id']
            password = login_form.cleaned_data['password']
            user = User.objects.filter(id=user_id).first()
            if user and user.password == hashcode(password, user_id):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['is_admin'] = user.is_admin
                Log.objects.create(user_id=user_id, action='登录')
                if (user.is_admin):
                    return redirect('/book_manage/')
                else:
                    return redirect('/home/')
            else:
                message = '用户名或密码错误！'
        return render(request, 'login.html', locals())


class LogoutView(View):
    """
    登出
    """

    def get(self, request):
        if request.session.get('is_login', None):
            Log.objects.create(user_id=request.session['user_id'], action='登出')
            request.session.flush()
            messages.success(request, '登出成功！')
        return redirect('/login/')


class RegisterView(View):
    """
    注册
    """

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        register_form = RegisterForm(request.POST)
        message = '请检查填写的内容！'
        if register_form.is_valid():
            user_name = register_form.cleaned_data['user_name']
            user_id = register_form.cleaned_data['user_id']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            major = register_form.cleaned_data['major']
            research_direction = register_form.cleaned_data['research_direction']
            tag_list = register_form.cleaned_data['tag_list']
            if password1 == password2:
                same_id_users = User.objects.filter(id=user_id)
                if same_id_users:
                    message = '该学号已被注册！'
                else:
                    User.objects.create(id=user_id, name=user_name, password=hashcode(password1, user_id), major=major,
                                        research_direction=research_direction, tag_list=tag_list)
                    Log.objects.create(user_id=user_id, action='注册')
                    messages.success(request, '注册成功！')
                    return redirect('/login/')
            else:
                message = '两次输入的密码不一致！'
        return render(request, 'register.html', locals())


class HomeView(View):
    """
    个人中心
    """

    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')

        user_id = request.session['user_id']
        borrow_entries = Borrow.objects.filter(user_id=user_id)
        return render(request, 'home.html', locals())


class SearchView(View):
    """
    借书
    """

    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')

        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            keyword = search_form.cleaned_data['keyword']
            books = Book.objects.filter(
                Q(name__icontains=keyword) | Q(author__icontains=keyword) | Q(publisher__icontains=keyword))
            if not books:
                message = '未查询到相关书籍！'
        else:
            books = Book.objects.all()
        return render(request, "search.html", locals())


class BorrowView(View):
    """
    借书操作
    """

    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')

        user_id = request.session['user_id']
        book_id = request.GET.get('book_id')
        books = Book.objects.filter(id=book_id, is_available=True)
        if books:
            book = books.first()
            borrow_time = datetime.now()
            return_ddl = borrow_time + timedelta(days=90)
            Borrow.objects.create(user_id=user_id, book_id=book_id, borrow_time=borrow_time, return_ddl=return_ddl)
            BorrowReview.objects.create(user_id=user_id, book_id=book_id, star=0)
            book.is_available = False
            book.save()
            Log.objects.create(user_id=user_id, book_id=book_id, action='借书')
            messages.success(request, '借书成功！')
        else:
            messages.error(request, '借书失败：此书不存在或已借出！')
        return redirect('/search/')


class ReturnView(View):
    """
    还书操作
    """

    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')

        user_id = request.session['user_id']
        book_id = request.GET.get('book_id')
        borrow_entries = Borrow.objects.filter(user_id=user_id, book_id=book_id)
        if borrow_entries:
            borrow_entry = borrow_entries.first()
            delta = -(borrow_entry.borrow_time - datetime.now())  # 负天数不足一天算一天
            exceed_days = delta.days - 90
            if exceed_days > 0:
                fine = exceed_days * 0.5
                messages.warning(request, '已逾期 {} 天，需缴纳罚金 {} 元！'.format(exceed_days, fine))
            borrow_entry.delete()
            book = Book.objects.get(id=book_id)
            book.is_available = True
            book.save()
            Log.objects.create(user_id=user_id, book_id=book_id, action='还书')
            messages.success(request, '还书成功！')
        else:
            messages.error(request, '还书失败：您未借过此书！')
        return redirect('/home/')


class StarView(View):
    """
    自己借阅过书籍进行评分操作
    """

    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')
        user_id = request.session['user_id']
        borrow_entries = BorrowReview.objects.filter(user_id=user_id).order_by("-id")
        return render(request, 'star.html', locals())

    def post(self, request):
        id = request.GET.get('id')
        star = request.form.get('star')
        print(id, '的星级为', star)


class BookStarView(View):
    """
    自己借阅过书籍进行评分操作
    """

    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')
        user_id = request.session['user_id']
        id = request.GET.get('id')
        star = int(request.GET.get('star'))
        if star > 5 | star < 1:
            messages.error(request, '评分最小为1最大为5,请检查！')
            return redirect('/star/')
        br = BorrowReview.objects.filter(id=id).first()
        br.star = star
        br.save()
        print(id, '的星级为', star)
        return redirect('/star/')


class TestView(View):
    """
    for test
    """

    def get(self, request):
        search_form = SearchForm()
        return render(request, 'test.html', locals())


class AdminHomeView(View):
    """
    管理员个人中心页面
    """

    def get(self, request):
        search_form = SearchForm()
        return render(request, 'home_admin.html', locals())


class BookManageView(View):
    """
    管理图书信息界面
    """

    def get(self, request):
        return redirect('/book_search/')


class BookSearchView(View):
    """
    图书管理时查询
    """

    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')

        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            keyword = search_form.cleaned_data['keyword']
            books = Book.objects.filter(
                Q(name__icontains=keyword) | Q(author__icontains=keyword) | Q(publisher__icontains=keyword))
            if not books:
                message = '未查询到相关书籍！'
        else:
            books = Book.objects.all()
        return render(request, "book_manage.html", locals())


class BookAddView(View):
    """
    新增书籍
    """

    def get(self, request):
        book_form = BookForm()
        return render(request, 'book_add.html', locals())

    def post(self, request):
        book_form = BookForm(request.POST)

        if book_form.is_valid():
            book_name = book_form.cleaned_data['book_name']
            author = book_form.cleaned_data['author']
            publisher = book_form.cleaned_data['publisher']
            category = book_form.cleaned_data['category']
            tag_list = book_form.cleaned_data['tag_list']
            Book.objects.create(name=book_name, author=author, publisher=publisher, category=category,
                                tag_list=tag_list)
            # Log.objects.create(book_name=book_name, action='新增')
            messages.success(request, '新增书籍成功！')
        return redirect('/book_manage/')


class BookDelView(View):
    """
    删除图书信息
    """

    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')

        book_id = request.GET.get('book_id')
        books = Book.objects.filter(id=book_id, is_available=True)
        if books:
            book = books.first()
            book.delete()
            messages.success(request, '删除成功！')
        else:
            messages.error(request, '删除失败：此书不存在或已借出！')
        return redirect('/book_manage/')


class UserManageView(View):
    """
    管理读者信息界面
    """

    def get(self, request):
        search_form = SearchForm()
        return redirect('/user_search/')


class UserSearchView(View):
    """
    用户管理时查询
    """

    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')

        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            keyword = search_form.cleaned_data['keyword']
            users = User.objects.filter(
                Q(name__icontains=keyword) | Q(id__icontains=keyword) | Q(major__icontains=keyword) | Q(research_direction__icontains=keyword))
            if not users:
                message = '未查询到相关用户！'
        else:
            users = User.objects.filter(is_admin=False)
        return render(request, "user_manage.html", locals())


def hashcode(s, salt='17373252'):
    s += salt
    h = hashlib.sha256()
    h.update(s.encode())
    return h.hexdigest()
