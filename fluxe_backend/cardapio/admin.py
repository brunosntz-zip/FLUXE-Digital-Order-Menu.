from django.contrib import admin
from .models import Produto, CategoriaProduto, Restaurante, Cliente, Comanda

admin.site.register(Restaurante)
admin.site.register(CategoriaProduto)
admin.site.register(Produto)
admin.site.register(Cliente)
admin.site.register(Comanda)