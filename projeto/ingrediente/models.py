from django.db import models

class Ingrediente_itens(models.Model):
    nome = models.CharField('ingrediente', max_length=100)
    estoque = models.DecimalField('estoque', max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"

    def __str__(self):
        return self.nome
