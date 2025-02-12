from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from .models import Produto, ProdutoIngrediente
from projeto.ingrediente.models import Ingrediente_itens
from .forms import ProdutoForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from decimal import Decimal

def produto_list(request):
    template_name = 'produto_list.html'
    objects = Produto.objects.all()
    context = {'object_list': objects}
    return render(request, template_name, context)

@login_required 
def produto_detail(request, pk):
    template_name = 'produto_detail.html'
    object = Produto.objects.get(pk=pk)
    context = {'object': object}
    return render(request, template_name, context)

@login_required 
def produto_add(request):
    template_name = 'produto_form.html'
    return render(request, template_name)

class ProdutoCreate(LoginRequiredMixin, CreateView):  
    model = Produto
    template_name = 'produto_form.html'
    form_class = ProdutoForm
    login_url = '/user/signin/'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredientes'] = Ingrediente_itens.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        ingredientes_data = self.request.POST.get('ingredientes_data', None)
        if ingredientes_data:
            try:
                ingredientes_list = json.loads(ingredientes_data)
                for item in ingredientes_list:
                    ingrediente_id = item.get('id')
                    quantidade = item.get('quantidade')
                    if quantidade and float(quantidade) > 0:
                        quantidade_decimal = Decimal(str(quantidade))
                        ingrediente = Ingrediente_itens.objects.get(id=ingrediente_id)
                        ingrediente.estoque -= quantidade_decimal
                        ingrediente.save()
                        ProdutoIngrediente.objects.create(
                            produto=self.object,
                            ingrediente=ingrediente,
                            quantidade=quantidade_decimal
                        )
                        ingrediente.estoque -= quantidade_decimal
                        ingrediente.save()
                    else:
                        raise ValueError(f"Estoque insuficiente para o ingrediente: {ingrediente.nome}")
            except Exception as e:
                print("Erro ao processar ingredientes:", e)
        return response

class ProdutoUpdate(LoginRequiredMixin, UpdateView): 
    model = Produto
    template_name = 'produto_form.html'
    form_class = ProdutoForm
    login_url = '/user/signin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredientes'] = Ingrediente_itens.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        ingredientes_data = self.request.POST.get('ingredientes_data', None)
        
        ProdutoIngrediente.objects.filter(produto=self.object).update(quantidade=0)
        
        if ingredientes_data:
            try:
                ingredientes_list = json.loads(ingredientes_data)
                for item in ingredientes_list:
                    ingrediente_id = item.get('id')
                    quantidade = item.get('quantidade')
                    if quantidade and float(quantidade) > 0:
                        ingrediente = Ingrediente_itens.objects.get(id=ingrediente_id)
                        if ingrediente.estoque >= float(quantidade):
                            ProdutoIngrediente.objects.update_or_create(
                                produto=self.object,
                                ingrediente=ingrediente,
                                defaults={'quantidade': quantidade}
                            )
                            ingrediente.estoque -= float(quantidade)
                            ingrediente.save()
                        else:
                            raise ValueError(f"Estoque insuficiente para o ingrediente: {ingrediente.nome}")
            except Exception as e:
                print("Erro ao processar ingredientes:", e)
        return response

@login_required 
def produto_json(request, pk):
    try:
        produto = Produto.objects.get(pk=pk)
        
        fornecedor_data = {
            'id': produto.fornecedor.id,
            'nome': produto.fornecedor.nome, 
        }

        data = {
            'id': produto.id,
            'produto': produto.produto,
            'preco': produto.preco,
            'estoque': produto.estoque,
            'fornecedor': fornecedor_data,
        }

        return JsonResponse({'data': data})
    
    except Produto.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': f'Erro inesperado: {str(e)}'}, status=500)

    

def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)  
    produto.delete() 
    return redirect('produto:produto_list') 
