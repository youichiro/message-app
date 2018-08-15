## Djangoのインストール

```sh
pip install django
```

## プロジェクトの作成

```sh
mkdir message-app-with-django
cd message-app-with-django
django-admin startproject message_app .
python manage.py startapp message
```

## データベースの設定ファイルの作成
**message_app/config.py**

```python
db = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'message_app',
    'USER': 'root',
    'PASSWORD': '', # ここにデータベースのパスワードを入力する
    'HOST': '',
    'PORT': '3306',
}
```

## settingsの変更
**message_app/settings.py**

```python
import os
import pymysql
from .config import db

...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'message',  # 追加
]

...

# ここを変更
pymysql.install_as_MySQLdb()
DATABASES = {
    'default': db
}

...

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
```

## message_app/urls.pyの変更
**message_app/urls.py**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('message.urls')),
]
```

## モデルの作成
**message/models.py**

```python
from django.db import models


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'messages'
```

## マイグレーション

```sh
python manage.py makemigrations
python manage.py migrate
```

## ビューの作成
**message/views.py**

```python
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Message


class MessageListView(ListView):
    model = Message
    template_name = 'message/message_list.html'


class MessageCreateView(CreateView):
    model = Message
    template_name = 'message/message_form.html'
    fields = ['text']
    success_url = reverse_lazy('message_list')
```

## テンプレートの作成
**message/templates/message/base.html**

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>メッセージアプリ</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

**message/templates/message/message_list.html**

```html
{% extends 'message/base.html' %}

{% block content %}
    <h3>メッセージリスト</h3>
    <a href="{% url 'message_form' %}">作成</a>
    {% for message in message_list %}
        <p>
            ID: {{ message.id }}
            <b>{{ message.text }}</b>
            作成: {{ message.created_at|date:"Y-m-d h:m" }}
            更新: {{ message.updated_at|date:"Y-m-d h:m" }}
        </p>
    {% endfor %}
{% endblock %}
```

**message/templates/message/message_form.html**

```html
{% extends 'message/base.html' %}

{% block content %}
    <h3>メッセージフォーム</h3>
    <form method="post">{% csrf_token %}
        <table>
            {{ form.as_table }}
        </table>
        <button type="submit">送信</button>
    </form>
{% endblock %}
```

## URLの設定
**message/urls.py**

```python
from django.urls import path
from . import views


urlpatterns = [
    path('view/', views.MessageListView.as_view(), name='message_list'),
    path('form/', views.MessageCreateView.as_view(), name='message_form'),
]
```

## 起動

```sh
python manage.py runserver
```

