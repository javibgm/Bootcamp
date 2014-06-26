# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from models import Photo
from django.conf import settings

# Permite que BADWORDS se pueda sobrescribir desde el settings.py
BADWORDS = getattr(settings, 'BADWORDS', ())


class UserSerializer(serializers.Serializer):

    id = serializers.Field()  # Es importante definir un campo id para poder acceder al detalle de un
                    # usuario ya que los campos que definamos aquí son los que van a aparecer en nuestra API
                    # Es un campo de solo lectura, no podemos cambiarlo con esta API
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def restore_object(self, attrs, instance=None):
        """
        Devuelve un objeto User en funcion de attrs
        :param attrs: diccionario con datos
        :param instance: objeto User a actualizar
        :return: objeto User
        """
        if not instance:
            instance = User()
        instance.first_name = attrs.get('first_name')
        instance.last_name = attrs.get('last_name')
        instance.username = attrs.get('username')
        instance.email = attrs.get('email')
        new_password = make_password(attrs.get('password'))
        instance.password = new_password

        return instance


class UserPostSerializer(UserSerializer):
    """
    Serializer específico para la validacion del metodo POST para indicar que no se puede crear un usuario existente
    """
    def validate(self, attrs):
        existent_users = User.objects.filter(username=attrs.get('username'))
        if len(existent_users) > 0:
            raise serializers.ValidationError(u'Ya existe ese usuario')
        return attrs  # todo ha ido OK

class PhotoSerializer(serializers.ModelSerializer):
    """
    clase serializadora de un modelo photo
    """
    class Meta:
        model = Photo
        read_only_fields = ('owner',)  # Impedimos que el propietario cambie al actualizar una foto

    """
    def validate_description(self, attrs, source):
    # Validamos solo la descripcion para que no tengan tacos
        description = attrs.get(source, '')
        for badword in BADWORDS:
            if badword.lower() in description.lower():
                raise serializers.ValidationError(badword + u"no está permitido")
        return attrs  # todo ha ido OK
    """


class PhotoListSerializer(PhotoSerializer):

    class Meta(PhotoSerializer.Meta):
        fields = ('id', 'owner', 'name')