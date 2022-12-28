from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Language, Genre
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available
    }
    return render(request, 'catalog/index.html', context=context)

class BookCreate(LoginRequiredMixin, CreateView): # model_form.html

    model = Book
    fields = '__all__'
    success_url = reverse_lazy('catalog:index')

class BookDetail(DetailView):
    model = Book

@login_required
def my_view(request):
    return render(request, 'catalog/my_view.html')


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'catalog/signup.html'

class CheckedOutBooksByUsersView(LoginRequiredMixin, ListView):
    model = BookInstance
    context_object_name = 'bookinstance'
    template_name = 'catalog/profile.html'
    paginate_by = 5 # mostramos cuantos elementos por pagina mostraremos

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)