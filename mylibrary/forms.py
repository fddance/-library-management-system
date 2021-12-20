from django import forms


class LoginForm(forms.Form):
    user_id = forms.CharField(label="用户名", max_length=8, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=64, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    user_name = forms.CharField(label="姓名", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_id = forms.CharField(label="学号", min_length=8, max_length=8,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", min_length=6, max_length=64,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", min_length=6, max_length=64,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    major = forms.CharField(label="专业", min_length=2, max_length=64,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    research_direction = forms.CharField(label="研究方向", min_length=2, max_length=64,
                                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    tag_list = forms.CharField(label="个人标签", min_length=6, max_length=64,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))


class BookForm(forms.Form):
    book_name = forms.CharField(label="书籍名称", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(label="书籍作者", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    publisher = forms.CharField(label="出版社", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.CharField(label="书籍种类", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tag_list = forms.CharField(label="标签集合", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))


class SearchForm(forms.Form):
    keyword = forms.CharField(label="关键词", max_length=60,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入关键词'}))
