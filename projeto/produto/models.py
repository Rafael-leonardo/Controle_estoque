from django.db import models
from django.urls import reverse_lazy
from projeto.fornecedores.models import Fornecedores_loja
from projeto.ingrediente.models import Ingrediente_itens

class Produto(models.Model):
    ncm = models.CharField('NCM', max_length=8)
    produto = models.CharField(max_length=100, unique=True)
    preco = models.DecimalField('preço', max_digits=7, decimal_places=2)
    estoque = models.DecimalField('estoque atual', max_digits=10, decimal_places=2)
    fornecedor = models.ForeignKey(
        Fornecedores_loja,
        related_name='fornecedores',
        on_delete=models.CASCADE,
    )
    ingredientes = models.ManyToManyField(Ingrediente_itens, related_name='produtos', through='ProdutoIngrediente')

    class Meta:
        ordering = ('produto',)

    def __str__(self):
        return self.produto

    def get_absolute_url(self):
        return reverse_lazy('produto:produto_detail', kwargs={'pk': self.pk})

    def to_dict_json(self):
        return {
            'pk': self.pk,
            'produto': self.produto,
            'estoque': self.estoque,
            'fornecedor': self.fornecedor.nome,
        }

class ProdutoIngrediente(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente_itens, on_delete=models.CASCADE)
    quantidade = models.DecimalField('quantidade por produto', max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produto.produto} - {self.ingrediente.nome} ({self.quantidade} unidades)"
