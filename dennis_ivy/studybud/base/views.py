from django.db.models import Q, Model
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import Room, Topic, Message
from .forms import RoomForm

# Create your views here.

def login_page(request: HttpRequest) -> HttpResponse:
    page = "login"

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = str(request.POST.get("username")).lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist")
    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")


def register_user(request: HttpRequest) -> HttpResponse:
    page = "register"
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")
    context = {"page": page, "form": form}
    return render(request, "base/login_register.html", context)


def home(request: HttpRequest) -> HttpResponse:
    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {"rooms": rooms, "topics": topics, "room_count": room_count, "room_messages": room_messages}
    return render(request, "base/home.html", context)


def room(request: HttpRequest, pk: str) -> HttpResponse:
    room: Room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        room.participants.add(User(request.user))
        return redirect("room", pk=room.id)
    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, "base/room.html", context)


def user_profile(request: HttpRequest, pk: str) -> HttpResponse:
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user": user, "rooms": rooms, "room_messages": room_messages, "topics": topics}
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def create_room(request: HttpRequest) -> HttpResponse:
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def update_room(request: HttpRequest, pk: str) -> HttpResponse:
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse(b"You are not allowed here")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def delete_room(request: HttpRequest, pk: str) -> HttpResponse:
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})


@login_required(login_url="login")
def delete_message(request: HttpRequest, pk: str) -> HttpResponse:
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": message})


