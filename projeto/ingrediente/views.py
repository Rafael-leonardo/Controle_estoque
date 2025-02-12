from django.shortcuts import render, redirect
from projeto.ingrediente.models import Ingrediente_itens
from django.http import JsonResponse
from projeto.ingrediente.forms import Ingrediente_itensForm


def ingrediente_list(request):
    ingredientes = Ingrediente_itens.objects.all()

    ingredientes_list = list(ingredientes.values('id', 'nome', 'estoque'))

    return JsonResponse(ingredientes_list, safe=False)

def ingrediente_add(request):
    if request.method == "POST":
        form = Ingrediente_itensForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingrediente:ingrediente_list')
    form = Ingrediente_itensForm()
    
    return render(request, "ingrediente_form.html", {"form":form})
