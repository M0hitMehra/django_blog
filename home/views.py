from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post


def home(request):
    # return HttpResponse("home")
    posts = Post.objects.all()
    pop_post = []
    i = 0
    for post in posts:
        if i > 10:
            break;
        pop_post.append(post)
        i = i+1
    context = {'NewPosts': pop_post}
    return render(request, 'home/home.html' , context)


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    # thanks = False
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        content = request.POST.get('content')
        if len(name) < 2 or len(email) < 2 or len(content) < 4 or len(phone) < 10:
            messages.error(request, 'Please enter valid details')
        else:
            contact = Contact(email=email, phone=phone, name=name, content=content, )
            contact.save()
            messages.success(request, "Form Submitted Successfully")

    return render(request, 'home/contact.html')


def search(request):
    query = request.GET.get('query')
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)

    if len(allPosts) == 0:
        messages.warning(request, "No posts found for your query")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        email = request.POST.get('email')

        # Validating User
        if len(username) > 15:
            messages.error(request, 'Username must be under 15 characters')
            return redirect('home')
        if len(username) <= 3:
            messages.error(request, 'Username must be at least 3 characters')
            return redirect('home')
        if not username.isalnum():
            messages.error(request, 'Username should only contain characters and numbers')
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, 'Confirm password is not same as password')
            return redirect('home')

        myUser = User.objects.create_user(username, email, pass1)
        myUser.first_name = fname
        myUser.last_name = lname
        myUser.save()

        loginUsername = username
        loginPassword = pass1
        user = authenticate(username=loginUsername, password=loginPassword)
        login(request, user)
        messages.success(request, 'Your account has been created successfully')
        return redirect('home')
    else:
        return HttpResponse("404 - Not Found", status=404)


def handleLogin(request):
    if request.method == 'POST':
        loginUsername = request.POST.get('loginusername')
        loginPassword = request.POST.get('loginpass')
        user = authenticate(username=loginUsername, password=loginPassword)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('home')
    return HttpResponse("404 - Page Not Found")


def handleLogout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')
