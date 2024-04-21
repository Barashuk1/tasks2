from django.shortcuts import render, redirect
from .models import Quote, Author, Tag
from .forms import RegistrationForm, LoginForm, AddQuoteForm
from django.contrib.auth import login, authenticate, logout

def quote_detail(request, quote_id):
    quote = Quote.objects.get(pk=quote_id)
    
    return render(request, 'quotes/quote_detail.html', {'quote': quote})

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