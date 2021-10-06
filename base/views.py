from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Message, Room , Topic
from .forms import RoomForm
# Create your views here.

def appLogin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if(request.method=='POST'):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # try:
        #     user = User.objects.get(username=username)
        # except:
        #     messages.error(request,'User does not exist!')
        
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Incorrect username or password or both, please check your credentials and try again')

    page = 'login'
    context = {'page':page}

    return render(request,'base/login-register.html',context)

def appLogout(request):
    logout(request)
    return redirect('home')
        
def appRegisterUser(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during user registration')

    form = UserCreationForm()
    context = {'form':form}
    return render(request,'base/login-register.html',context)

def home(request):
    q =  request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.all()
    activities = Message.objects.all()[:10]
    rooms = Room.objects.filter(
                Q(topic__name__icontains = q) |
                Q(name__icontains = q) |
                Q(description__icontains = q) 
            )

    room_count = rooms.count()
    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'activities':activities}
    return render(request,'base/index.html',context)

def room(request,slug):
    room = Room.objects.get(id=slug)
    
    if request.method == 'POST':
        comment = Message.objects.create(user = request.user , room = room , body = request.POST.get('body'))
        room.message_set.add(comment)
        #request.method = 'GET'
        room.participants.add(request.user)
        return redirect('room',slug=room.id)
    
    participants = room.participants.all()
    comments = room.message_set.all() #.order_by('-updated')
    context = {'room':room,'comments':comments,'participants':participants}

    return render(request,'base/room.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    context = {'form':form}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
        else:
            messages.error(form.errors)

    return render(request,'base/room-form.html',context)

@login_required(login_url='login')
def updateRoom(request,slug):
    room =  Room.objects.get(id=slug)

    if request.user != room.host :
        return HttpResponse('You are not authorized, Access denied')

    form = RoomForm(instance=room)

    if request.method=='POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request,'base/room-form.html',context)

@login_required(login_url='login')
def deleteRoom(request,slug):
    room = Room.objects.get(id=slug)

    if request.user != room.host :
        return HttpResponse('You are not authorized, Access denied')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'item':room}
    return render(request,'delete-item.html',context)

@login_required(login_url='login')
def deleteMessage(request,slug):
    message = Message.objects.get(id=slug)

    if request.user != message.user:
        return HttpResponse('You are not authorized')
    
    if request.method == 'POST':
        message.delete()
        return redirect('room',slug=message.room.id)
    
    context = {'item':message}

    return render(request,'delete-item.html',context)

def userProfile(request,user_id):
    user = User.objects.get(id=user_id)
    rooms = user.room_set.all()
    activities = user.message_set.all()[:10]
    topics = Topic.objects.all()
    context = {
        'user':user,
        'rooms':rooms,
        'activities':activities,
        'topics':topics
    }

    return render(request,'base/user-profile.html',context)

