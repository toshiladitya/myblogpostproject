# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db.models import Q
from .models import Blog, Comment, Tag
from django.conf import settings
from django.core.paginator import Paginator



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('blog_list')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('blog_list')
    return render(request, 'users/login.html')

@login_required
def blog_list(request):
    tag = request.GET.get('tag')
    tags = Tag.objects.all()
    if tag:
        blogs = Blog.objects.filter(tags__name=tag)
    else:
        blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/blog_list.html', {'page_obj': page_obj, 'tags': tags})

@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = blog.comments.all()
    return render(request, 'blog/blog_detail.html', {'blog': blog, 'comments': comments})

@login_required
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(blog=blog, author=request.user, content=content)
    return redirect('blog_detail', blog_id=blog_id)

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('blog_detail', blog_id=comment.blog.id)

@login_required
def share_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    sent = False
    error = None
    
    if request.method == 'POST':
        recipient_email = request.POST.get('email')
        if recipient_email:
            subject = f"Check out this blog: {blog.title}"
            message = f"Hi there,\n\nCheck out this blog post:\n\n{blog.title}\n\n{blog.content}\n\nBest regards,\nYour Blog Team"
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
                sent = True
            except Exception as e:
                error = str(e)
    
    return render(request, 'blog/share_blog.html', {'blog': blog, 'sent': sent, 'error': error})


@login_required
def search_blog(request):
    query = request.GET.get('q', '')
    results = Blog.objects.filter(
        Q(title__contains=query) | Q(content__contains=query)
    )
    return render(request, 'blog/search_results.html', {'results': results})

def logout_view(request):
    logout(request)
    return redirect('login')
