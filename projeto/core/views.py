from django.shortcuts import render
from projeto.vendas.models import ItemVenda, Venda
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def index(request):
    produtos = ItemVenda.objects.values('produto__produto').annotate(total_vendido=Sum('quantidade')).order_by('-total_vendido')

    produtos_nomes = [produto['produto__produto'] for produto in produtos]
    produtos_quantidade = [produto['total_vendido'] for produto in produtos]

    cores = ['#FF5733', '#33FF57', '#3357FF', '#F0FF33', '#FF33A1', '#33FFF7']
    
    produtos_data = [
        {
            'produto': nome,
            'quantidade_vendida': qtd,
            'cor': cores[i % len(cores)]
        }
        for i, (nome, qtd) in enumerate(zip(produtos_nomes, produtos_quantidade))
    ]

    context = {
        'produtos_nomes': produtos_nomes,
        'produtos_quantidade': produtos_quantidade,
        'produtos': produtos_data
    }
    return render(request, 'index.html', context)


def list_vendas(request):
    vendas = Venda.objects.prefetch_related('itens').order_by('-id')
    
    for venda in vendas:
        venda.total_calculado = sum(
            item.quantidade * item.preco_unitario for item in venda.itens.all()
        )
    
    return render(request, 'list_vendas.html', {'vendas': vendas})


@login_required
def financas(request):
    produtos = ItemVenda.objects.values('produto__produto') \
        .annotate(
            total_vendido=Sum('quantidade'),
            receita_total=Sum(F('quantidade') * F('preco_unitario'))
        ).order_by('-total_vendido')

    valor_total_vendas = sum(produto['receita_total'] for produto in produtos)

    metodos_pagamento = Venda.objects.values('forma_pagamento') \
        .annotate(total_vendas=Sum('total')) \
        .order_by('-total_vendas')

    vendas_por_usuario = Venda.objects.values('user__nome').annotate(
        total_vendas=Sum('total')
    ).order_by('-total_vendas')

    itens_vendidos = [
        {
            'produto': produto['produto__produto'],
            'quantidade_vendida': produto['total_vendido'],
        }
        for produto in produtos
    ]

    context = {
        'produtos': [
            {
                'produto': produto['produto__produto'],
                'quantidade_vendida': produto['total_vendido'],
                'receita_total': produto['receita_total'],
            }
            for produto in produtos
        ],
        'valor_total_vendas': valor_total_vendas,
        'metodos_pagamento': [
            {
                'metodo': metodo['forma_pagamento'],
                'total_vendas': metodo['total_vendas'],
            }
            for metodo in metodos_pagamento
        ],
        'vendas_por_usuario': vendas_por_usuario,
        'itens_vendidos': itens_vendidos,
    }
    return render(request, 'financa.html', context)

@login_required
def vendas_usuario_detalhes(request, nome):
    vendas = Venda.objects.filter(user__nome=nome).values('forma_pagamento').annotate(
        total_vendido=Sum('total')
    )

    data = [
        {
            'metodo_pagamento': venda['forma_pagamento'],
            'total_vendido': float(venda['total_vendido']),
        }
        for venda in vendas
    ]

    return JsonResponse({'vendas': data})