from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Item, Day
from .forms import ItemCreateForm
from datetime import datetime, date

class DayItemListView(LoginRequiredMixin, ListView):
    model = Item
    context_object_name = 'context'
    template_name = 'tracker/home.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        today = str(datetime.now())[:10]
        day, created = Day.objects.get_or_create(tracker=user, date=today)
        items = Item.objects.filter(day=day)

        # Populate context data
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        context['items'] = items
        context['day'] = day 
        return context

class DayItemDetailView(LoginRequiredMixin, DetailView):
    model = Day 
    template_name = 'tracker/home.html'
    context_object_name = 'context'

    def get_context_data(self, **kwargs):
        user = self.request.user
        today = date.today()

        # Retrieve Day object
        day = self.object

        # Populate context data
        context = super().get_context_data(**kwargs)
        context['today'] = today
        context['day'] = day
        context['items'] = Item.objects.filter(day=day)
        return context

    def get_object(self, queryset=None):
        user = self.request.user
        pk = self.kwargs.get('pk')
        return get_object_or_404(Day, pk=pk, tracker=user)

class DayItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemCreateForm
    context_object_name = 'context' 

    def form_valid(self, form):
        tracker = self.request.user
        date = self.kwargs.get('date') 
        date_param = datetime.strptime(date, "%Y-%m-%d").date()
        day, created = Day.objects.get_or_create(tracker=tracker, date=date_param)
        form.instance.day = day
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.kwargs.get('date')
        context['day'] = Day.objects.get_or_create(tracker=self.request.user, date=date)[0]
        return context
    
    def get_success_url(self):
        # Retrieve the pk of the day object
        pk = self.object.day.pk if self.object else self.request.POST.get('pk')
        # Construct the success URL using the day's pk
        return reverse_lazy('detail-day', kwargs={'pk': pk})
    
class DayItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item

    def get_success_url(self):
        item = self.get_object()
        pk = item.day.pk if item else self.request.POST.get('pk')
        return reverse_lazy('detail-day', kwargs={'pk': pk})

    def test_func(self):
        item = self.get_object()
        return item.day.tracker == self.request.user

class DayListView(LoginRequiredMixin, ListView):
    model = Day
    template_name = 'tracker/list-days.html'
    context_object_name = 'context'

    def get_context_data(self):
        user = self.request.user

        # Populate context data
        context = {}
        context['today'] = date.today()
        context['days'] = Day.objects.filter(tracker=user)
        context['tracker'] = user
        return context
