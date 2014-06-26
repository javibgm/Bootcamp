# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from models import Photo
from serializers import UserSerializer, UserPostSerializer, PhotoSerializer, PhotoListSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404  # atajo para crear una vista de un objeto y si no existe devolver un 404
from rest_framework import status  # Modulo de ayuda para los codigos de estado http
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from permissions import UserPermission
from django.db.models import Q
from models import VISIBILITY_PUBLIC


class UserListAPI(APIView):

    permission_classes = (UserPermission,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)  # le indicamos al serializer que le pasamos varios usuarios
                                                    # el serializer nos devuelve una lista de diccionarios con los datos
        return Response(serializer.data)  # la funcion Response se encarga de renderizar los datos
                                          # para mostrarlos en formato HTML

    def post(self, request):
        serializer = UserPostSerializer(data=request.DATA)  # Pasamos los datos del metodo (no diferenciamos entre POST
                                                        # y otros metodos)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class UserDetailAPI(APIView):

    permission_classes = (UserPermission,)

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:  # Para los permisos del usuario, que los usuarios
                                                            # normales no puedan ver el detalle de otro usuario
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        """
        Actualizacion de un usuario
        :param request: objeto request
        :param pk: clave primaria del usuario a actualizar
        :return: oobjeto response
        """
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:  # Para los permisos del usuario, que los usuarios
                                                            # normales no puedan modificar el detalle de otro usuario
            serializer = UserSerializer(user, data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=202)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user.is_superuser or request.user == user:  # Para los permisos del usuario, que los usuarios
                                                            # normales no puedan modificar el detalle de otro usuario
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PhotoAPIQueryset:

    def get_queryset(self):
        """
        Devuelve un queryset en funcion de varios criterios
        """
        if self.request.user.is_superuser:
            return Photo.objects.all()
        elif self.request.user.is_authenticated():
            return Photo.objects.filter(Q(visibility=VISIBILITY_PUBLIC) | Q(owner=self.request.user))
        else:
            return Photo.objects.filter(visibility=VISIBILITY_PUBLIC)


class PhotoListAPI(PhotoAPIQueryset, ListCreateAPIView):
    """
    clase que genera automaticamente el listado (GET) y creacion (POST) de objetos con el serializar indicado
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return PhotoSerializer if self.request.method == "POST" else self.serializer_class
        # Devolvemos el serializador completo si es un post para poder hacer fotos con todos los campos

    def pre_save(self, obj):
        """
        Asigna la autoria de la foto al usuario autenticado al crearla
        """
        obj.owner = self.request.user


class PhotoDetailAPI(PhotoAPIQueryset, RetrieveUpdateDestroyAPIView):
    """
    Implementa la API de detalle (GET),
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)