from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Event, Photo
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


class EventCreate(CreateView):
    model = Event
    fields = ['title', 'date', 'time', 'location',
            'attendees', 'infolink', 'category', 'description']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def events_index(request):
    #   events = Event.objects.filter()
    #   events = request.user.event_set.all()
    events = Event.objects.all()
    return render(request, 'events/index.html', {'events': events})

def category_index(request, event_category):
    events = Event.objects.filter(category=event_category)
    return render(request, 'events/index.html', {'events': events})

def events_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    # Instantiate FeedingForm to be rendered in the template
    post_form = PostForm()
    return render(request, 'events/detail.html', {
        # Pass the cat and feeding_form as context
        'event': event,
    })

def upload_photo(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'main_app/event_upload_photo.html', {
        # Pass the cat and feeding_form as context
        'event': event
    })


def landing(request):
    return render(request, 'index.html', {'arr': ['Outdoors', 'Entertainment', 'Food', 'Tech', 'Education', 'Health']})


def user(request):
<<<<<<< HEAD

    events = Event.objects.all()
    return render(request, 'user/profile.html', {'contact_name': request.user.first_name, 'events': events})
=======
    
    return render(request, 'user/profile.html', {'contact_name': request.user.first_name})
>>>>>>> parent of 056832f... fix comments showing on detail view, and passing events to profile screen


def events(request):
    return render(request, 'events/index.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid Sign up - Try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
