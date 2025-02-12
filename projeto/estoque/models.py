from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from projeto.core.models import TimeStampedModel
from projeto.produto.models import Produto
from .managers import EstoqueEntradaManager, EstoqueSaidaManager
from django.conf import settings

MOVIMENTO = (
    ('e', 'entrada'),
    ('s', 'saida'),
)

class Estoque(TimeStampedModel):
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    nf = models.PositiveBigIntegerField('nota fiscal', null=True, blank=True)
    movimento = models.CharField(max_length=1, choices=MOVIMENTO)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.created.strftime('%d/%m/%Y')} - {self.funcionario.username}"

    def nf_formated(self):
        return str(self.nf).zfill(3)

class EstoqueItens(models.Model):
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='estoques')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return f'{self.produto.produto} - Quantidade: {self.quantidade} - Saldo: {self.saldo}'

    def atualizar_estoque(self):
        if self.saldo >= self.quantidade:
            self.saldo -= self.quantidade
            self.save()
        else:
            raise ValueError(f"Estoque insuficiente para o produto {self.produto.produto}!")

    def atualizar_estoque_ingredientes(self):
        for ingrediente in self.produto.ingredientes.all():
            produto_ingrediente = self.produto.produtoingrediente_set.get(ingrediente=ingrediente)
            quantidade_necessaria = produto_ingrediente.quantidade * self.quantidade

            if ingrediente.estoque < quantidade_necessaria:
                raise ValueError(f"Estoque insuficiente para o ingrediente {ingrediente.nome}!")
            
            ingrediente.estoque -= quantidade_necessaria
            ingrediente.save()

class EstoqueEntrada(Estoque):
    objects = EstoqueEntradaManager()

    class Meta:
        proxy = True
        verbose_name = 'estoque entrada'
        verbose_name_plural = 'estoque entrada'

    def get_absolute_url(self):
        return reverse_lazy('estoque:estoque_entrada_detail', kwargs={'pk': self.pk})

class EstoqueSaida(Estoque):
    objects = EstoqueSaidaManager()

    class Meta:
        proxy = True
        verbose_name = 'estoque saída'
        verbose_name_plural = 'estoque saída'

    def get_absolute_url(self):
        return reverse_lazy('estoque:estoque_saida_detail', kwargs={'pk': self.pk})
