from django import forms
from .models import Ingrediente_itens

class Ingrediente_itensForm(forms.ModelForm):

    class Meta:
        model = Ingrediente_itens
        fields = "__all__"