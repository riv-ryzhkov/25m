from lib2to3.fixes.fix_input import context

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView

from .models import Book
from .forms import BookForm


class IndexTab(ListView):
    paginate_by = 5
    model = Book
    template_name = 'main/index_tab.html'
    context_object_name = 'books'
    extra_context = {'numbers': 'is ' + str(len(Book.objects.all()))}
    allow_empty = False



def index(request):
    # books = Book.objects.all()
    books = Book.objects.order_by('-id')
    # books = Book.objects.order_by('-id')[:2]
    # books = Book.objects.filter(author='Шевченко Т.Г.')
    # books = Book.objects.filter(id__gt=10)
    # books = Book.objects.filter(id__lt=2)
    return render(request, 'main/index.html', {'title': 'головна сторінка', 'books': books})

def index_tab(request):
    books = Book.objects.order_by('-id')
    return render(request, 'main/index_tab.html', {'title': 'Книги', 'books': books})


def book_view(request, id=1):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        raise Http404
    return render(request, 'main/book_view.html', {'title': 'Книги', 'book': book})


def book_delete(request, id=0):
    try:
        book = Book.objects.get(id=id)
        book.delete()
    except Book.DoesNotExist:
        raise Http404
    books = Book.objects.order_by('-id')
    return render(request, 'main/index_tab.html', {'title': 'Книги', 'books': books})



def about(request):

    context_list = Book.objects.all()
    paginator = Paginator(context_list, 5)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, 'main/about.html', {'title': 'About us', 'books_page': page_obj})

def index_start(request):
    return render(request, 'main/start.html')


def create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = BookForm(initial={'author': 'Невідомий автор'})
    context = {
        'form': form
    }
    return render(request, 'main/create.html', context)

def book_edit(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = BookForm()
        else:
            book = Book.objects.get(id=id)
            form = BookForm(instance=book)
        return render(request, 'main/book_edit.html', {'form': form})
    else:
        if id == 0:
            form = BookForm(request.POST)
        else:
            book = Book.objects.get(id=id)
            form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
        return redirect('main')
