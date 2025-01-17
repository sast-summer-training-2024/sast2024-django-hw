# 选课系统

## 简介

这还是那个简单的选课系统, 只是这次是一个正儿八经的简单后端.

## 如何运行

1. 建议使用 conda 环境, 新建一个 (或者已有的也行) `python>=3.12` 环境
2. 安装依赖: `pip install -r requirements.txt`
3. 初始化数据库: `python manage.py migrate`
4. 使用标准的 Django 启动模式: `python manage.py runserver`

## 功能说明

本作业预期实现一个简单的选课系统后端, 具体功能如下:

1. 用户登录, 仅需要用户名, 自动注册. (这是为了简单起见, 如果你想练练手, 欢迎自己加上密码)
2. 用户登出
3. 列出所有课程
4. 选课
5. 列出已选课程
6. 管理员上传课程列表
7. 管理员下载所有用户的选课情况

框架中已经实现了部分功能和其它功能的部分. 希望你能够按照提示完成这个系统的剩余部分.

## 待完成

你需要完成的功能全都在 `views.py` 里面. 但是:

- 我希望你首先能够理解整个框架的结构, 然后再开始编写代码;
- 尤其是 `api` 这个 Decorator, 你需要理解它的作用.

## 预期

本作业应该不难 (根据 `git log` 可知我就用了 3h 就把框架整个写完了), 希望大家能从中学到
Django 框架的基本结构和写法, 见微知著, 了解前后端分离开发范式, 了解后端的工程性,
了解文档和注释在项目代码中的重要作用.

这个后端将与 React 的前端配合成为一个完整的简单的选课系统.

## 进阶功能

大家可以可选地实现以下进阶功能:

- 课程的增删改查
- 用户密码登录
- 基于 JWT 的认证
- 课程的搜索和排序
- 时间冲突的检测
- 管理员查看每个用户的选课情况
- 课程的课余量检查
- ......