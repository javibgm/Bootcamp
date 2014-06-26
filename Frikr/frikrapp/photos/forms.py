# -*- coding: utf-8 -*-
from models import Photo
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


BADWORDS = (u'aparcabicis', u'bocachancla', u'abollao', u'limiatubos', u'mascachapas', u'diseñata')


class PhotoForm(forms.ModelForm):
    """
    Pinta un formulario de una foto
    """
    class Meta:
        model = Photo  # Se basa en el modelo photo
        fields = ['name', 'url', 'description', 'license', 'visibility']

    """
    def clean(self):
    # Validacion del formulario (esta comentado porque se esta haciendo la validacion en el clean del model)
        cleaned_data = super(PhotoForm, self).clean()
        description = cleaned_data.get('description', '')
        for badword in BADWORDS:
            if badword in description:
                raise forms.ValidationError(badword + u' no está permitido')
        return cleaned_data
    """