from django.contrib import admin
# Importando tudo pra garantir que nada fique de fora
from .models import Produto, CategoriaProduto, Restaurante, Cliente, Comanda, Mesa, Pedido, Usuario

# --- Cadastros Simples ---
admin.site.register(Restaurante)
admin.site.register(Cliente)
admin.site.register(Comanda)
admin.site.register(Mesa)     # Adicionei pra garantir
admin.site.register(Pedido)   # Adicionei pra garantir
admin.site.register(Usuario)

# --- Cadastros "Pro" (Com busca e filtros) ---

@admin.register(CategoriaProduto)
class CategoriaProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem_exibicao', 'ativo') 
    ordering = ('ordem_exibicao',)
    list_editable = ('ordem_exibicao', 'ativo') # Pra editar rápido a ordem

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_atual', 'ativo', 'eh_popular') # Colunas na tabela
    list_filter = ('categoria', 'ativo', 'eh_popular') # Filtros laterais
    search_fields = ('nome', 'descricao') # Barra de busca
    list_editable = ('preco_atual', 'ativo', 'eh_popular') # Edita direto na lista (Rápido demais!)
    
    # 🔥 O SEGREDO DO CROSS-SELLING 🔥
    # Cria a interface de duas caixas para escolher os adicionais
    filter_horizontal = ('sugestoes',)