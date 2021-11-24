from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from .models import Todo
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import UserCreationForm
#from django.http import HttpResponse



class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasklist')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasklist')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasklist')
        return super(RegisterPage, self).get(*args, **kwargs)

# Create your views here.
class Tasklist(LoginRequiredMixin, ListView):
    context_object_name = 'tasks'
    model = Todo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Makes sure the user can only see what he created in the tasks
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(completed=False).count()

        search_input = self.request.GET.get('search-area') or '' # Get the search input from the url
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context
    

class Taskdetail(LoginRequiredMixin, DetailView):
    model = Todo
    context_object_name = 'tasksdetail'

class Taskcreate(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasklist')
    def form_valid(self, form):                  #make sure the user is creating a task that only belongs to him
        form.instance.user = self.request.user
        return super(Taskcreate, self).form_valid(form)

class Taskupdate(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasklist')

class Taskdelete(LoginRequiredMixin, DeleteView):
    model = Todo
    context_object_name = 'task'
    success_url = reverse_lazy('tasklist')



