from django.contrib import admin
from .models import Produto, CategoriaProduto, Restaurante, Cliente, Comanda

# --- Cadastros Simples ---
admin.site.register(Restaurante)
# admin.site.register(CategoriaProduto) # Vou melhorar esse também abaixo
admin.site.register(Cliente)
admin.site.register(Comanda)

# --- Cadastros "Pro" (Com busca e filtros) ---

@admin.register(CategoriaProduto)
class CategoriaProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem_exibicao') # Mostra colunas
    ordering = ('ordem_exibicao',) # Ordena por ordem de exibição

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_atual', 'ativo', 'eh_popular') # Colunas na tabela
    list_filter = ('categoria', 'ativo', 'eh_popular') # Filtros laterais (ajuda muito!)
    search_fields = ('nome', 'descricao') # Barra de busca
    list_editable = ('preco_atual', 'ativo', 'eh_popular') # Edita direto na lista (muito rápido)