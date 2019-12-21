from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Event, Photo, User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import uuid
import boto3

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
    return render(request, 'events/index.html', {'events': events, 'category': event_category})

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
    
    return render(request, 'user/profile.html', {'contact_name': request.user.first_name})


def events(request):
    return render(request, 'events/index.html', )


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



class EventUpdate(UpdateView):
  model = Event
  fields = ['title', 'date', 'time', 'location', 'description', 'attendees', 'infolink', 'category']

class EventDelete(DeleteView):
  model = Event
  success_url = '/events/'

def add_photo(request, event_id):
    event = Event.objects.get(id=event_id)
    S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
    BUCKET = 'dog-sitter'
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, event_id=event_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('events_detail', event_id=event_id)
