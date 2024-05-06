from django.shortcuts import render, redirect
from .models import Quote, Author, Tag
from .forms import RegistrationForm, LoginForm, AddQuoteForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

def quote_detail(request, quote_id):
    quote = Quote.objects.get(pk=quote_id)
    
    return render(request, 'quotes/quote_detail.html', {'quote': quote})

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Генерувати та надіслати новий пароль на вказану адресу електронної пошти
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()
            subject = 'Password Reset'
            message = f'Your new password is: {new_password}'
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]
            send_mail(subject, message, from_email, to_email)
            return HttpResponse('An email with the new password has been sent.')
        except User.DoesNotExist:
            return HttpResponse('User with this email does not exist.')
    else:
        return render(request, 'reset_password.html')

def add_quote(request):
    if request.method == 'POST':
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data['author_name']
            quote_text = form.cleaned_data['quote_text']
            tag_names = form.cleaned_data['tags']

            author_instance, created = Author.objects.get_or_create(name=author_name)

            new_quote = Quote.objects.create(author=author_instance, text=quote_text)

            if tag_names:
                tag_names_list = [tag.strip() for tag in tag_names.split(',')]
                for tag_name in tag_names_list:
                    tag_instance, created = Tag.objects.get_or_create(name=tag_name)
                    new_quote.tags.add(tag_instance)

            return redirect('index')  
    else:
        form = AddQuoteForm()

    return render(request, 'quotes/add_quote.html', {'form': form})

def index(request):
    quotes = Quote.objects.all()    
    return render(request, 'quotes/index.html', {'quotes': quotes})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)  
    return redirect('index') 