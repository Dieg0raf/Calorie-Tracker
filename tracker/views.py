from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.models import User
from .models import Item, Day
from .forms import ItemCreateForm
from datetime import datetime

# Create your views here.
def home(request):
    user = request.user
    day = Day.objects.filter(tracker=user).first()
    items = Item.objects.all()
    return render(request, 'tracker/home.html', {'items': items})

class DayItemListView(ListView):
    model = Item
    context_object_name = 'context'
    template_name = 'tracker/home.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        date_today = str(datetime.now())[:10]
        day = Day.objects.get(tracker=user, date=date_today)
        items = Item.objects.filter(day=day)
        context['items'] = items
        context['day'] = day 

        return context

class DayItemCreateView(CreateView):
    model = Item
    form_class = ItemCreateForm

    def form_valid(self, form):
        tracker = self.request.user
        date = self.kwargs.get('date') 
        date_param = datetime.strptime(date, "%Y-%m-%d").date()
        day, created = Day.objects.get_or_create(tracker=tracker, date=date_param)
        form.instance.day = day

        # increment amount of calories in Day
        Day.increment(
            day, 
            calories=form.instance.calories,
            protein=form.instance.protein,
            carbs=form.instance.carbs,
            fats=form.instance.fats,
            )

        return super().form_valid(form)
    
class DayItemDeleteView(DeleteView):
    model = Item
    success_url = '/'

class DayListView(ListView):
    model = Day
    template_name = 'tracker/list-days.html'
    context_object_name = 'days'

    def get_queryset(self):
        user = self.request.user
        return Day.objects.filter(tracker=user)
