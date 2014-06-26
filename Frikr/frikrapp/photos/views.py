# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http.response import HttpResponseNotFound
from models import Photo, VISIBILITY_PUBLIC
from django.contrib.auth import authenticate, login, logout
from forms import LoginForm, PhotoForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic import ListView
# Create your views here.


class HomeView(View):
    """
    Pagina de inicio
    """
    def get(self, request):
        photo_list = Photo.objects.filter(visibility=VISIBILITY_PUBLIC).order_by("-created_at")[:3]
        context = {
            "photos": photo_list
        }
        return render(request, "main.html", context)


class PhotoDetailView(View):
    """
    Muestra el detalle de una foto
    """
    def get(self, request, pk):
        possible_photos = Photo.objects.filter(pk=pk)
        if request.user.is_authenticated():
            possible_photos = possible_photos.filter(Q(owner=request.user) | Q(visibility=VISIBILITY_PUBLIC))
        else:
            possible_photos = possible_photos.filter(visibility=VISIBILITY_PUBLIC)
        if len(possible_photos) == 0:
            return HttpResponseNotFound('No existe la foto seleccionada')
        else:
            context = {
                "photo": possible_photos[0]
            }
            return render(request, "photo_detail.html", context)


class UserLoginView(View):
    """
    Loguea un usuario
    """
    def get(self, request):
        login_form = LoginForm()
        context = {
            'form': login_form
        }
        return render(request, "login.html", context)

    def post(self, request):
        error_messages = []
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is None:
                error_messages.append('Nombre de usuario o contraseña incorrecta')
            else:
                if user.is_active:
                    login(request, user)  # crea la sesion de usuario
                    next_url = request.GET.get('next', '/')
                    return redirect(next_url)
                else:
                    error_messages.append('El usuario no esta activo')
        context = {
            "form": login_form,
            "error_messages": error_messages
        }
        return render(request, "login.html", context)


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class UserProfileView(View):
    """
    Devuelve las fotos de un usuario registrado
    """
    @method_decorator(login_required())  # forzamos a que el usuario esté autenticado
    def get(self, request):
        context = {
            'photos': request.user.photo_set.all()
        }
        return render(request, "profile.html", context)


@login_required()
def create_photo(request):
    """
    Gestiona la creacion de fotos
    :param request: objeto request
    :return:
    """
    new_photo = None
    if request.method == "POST":
        photo_with_user = Photo(owner=request.user)
        form = PhotoForm(request.POST, instance=photo_with_user)
        if form.is_valid():
            new_photo = form.save()
            form = PhotoForm()
    else:
        form = PhotoForm()
    context = {
        'photo': new_photo,
        'form': form
    }
    return render(request, 'create_photo.html', context)


class PhotoListView(ListView):
    model = Photo
    template_name = 'photo_list.html'

    def get_queryset(self):
        return Photo.objects.filter(visibility=VISIBILITY_PUBLIC)