from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Message, Comment
from apps.log_reg_app.models import User
from datetime import datetime, timedelta
import bcrypt



def show_wall(request):
    if request.method == "GET":
        try:
            my_user_id = request.session['user_id']
        except:
            return redirect("/")
        my_user = User.objects.get(id=my_user_id)
        first_name = my_user.first_name
        last_name = my_user.last_name
        message_posts = []
        for message in Message.objects.all():
            message_posts.append({'first_name': User.objects.get(id=message.user_id).first_name,
                            'last_name': User.objects.get(id=message.user_id).last_name,
                            'created_at': message.created_at, 
                            'message': message.message,
                            'message_id': message.id,
                            'user_id': message.user_id,
                            })
        comment_posts = []
        for comment in Comment.objects.all():
            comment_posts.append({'comment': comment.comment,
                                'message_id':comment.message_id,
                                'user_id': comment.user_id,
                                'created_at': comment.created_at,
                                'first_name': User.objects.get(id=comment.user_id).first_name,
                                'last_name': User.objects.get(id=comment.user_id).last_name,
                                })
        context = {'user_id': my_user_id, 'first_name': first_name, 'last_name': last_name, 'message_posts':message_posts, 'comments':comment_posts} # context provides a way to display it on the html
        return render(request, 'the_wall_app/index.html', context)

def add_message(request):
    if request.method == "POST":
        message_post = request.POST['message']
        user_id = request.session['user_id']
        errors = Message.objects.message_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/wall")
        else:
            my_message = Message.objects.create(user_id=user_id, message=message_post)
            context = {'message': message_post, 'message_id': my_message.id}
            return redirect("/wall", context)
    if request.method == "GET":
        return redirect("/")

def add_comment(request):
    if request.method == "POST":
        comment_post = request.POST['comment']
        user_id = request.session['user_id']
        message_id = request.POST['message_id']
        errors = Comment.objects.comment_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/wall")
        else:
            my_comment = Comment.objects.create(message_id=message_id, user_id=user_id, comment=comment_post)
            context = {'message': comment_post, 'comment_id': my_comment.id}
            return redirect("/wall", context)
    if request.method == "GET":
        return redirect("/")

def delete_post(request, message_id):
    if request.method == "POST":
        message = Message.objects.get(id=message_id)
        given_date = message.created_at
        now = timezone.now()
        delta = now - given_date
        if delta < timedelta(minutes=30):
            message.delete()
            pass
        else:
            messages.error(request, 'You can only delete messages within 30 minutes of creation')
        return redirect("/wall")
    if request.method == "GET":
        return redirect("/")

def log_out(request):
    request.session.clear()
    return redirect("/")