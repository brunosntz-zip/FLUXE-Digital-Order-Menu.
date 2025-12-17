from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from cardapio.views import (
    CategoriaProdutoViewSet, 
    ProdutoViewSet,
    ProdutoPopularViewSet,
    adicionar_carrinho, 
    ver_carrinho, 
    remover_carrinho, 
    limpar_carrinho,
    home,      
    detalhes   
)

# Configuração da API
router = routers.DefaultRouter()
router.register(r'categorias', CategoriaProdutoViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'populares', ProdutoPopularViewSet, basename='produto-popular')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include(router.urls)),
    
    # PAGINAS HTML
    path('', home, name='home'),
    
    # 👇 AQUI ESTAVA O ERRO! Adicionei <str:produto_id> pra ele aceitar o código do produto
    path('detalhes/<str:produto_id>/', detalhes, name='detalhes'),

    # CARRINHO
    path('carrinho/', ver_carrinho, name='ver_carrinho'),
    path('carrinho/add/<str:produto_id>/', adicionar_carrinho, name='add_carrinho'),
    path('carrinho/remove/<str:produto_id>/', remover_carrinho, name='remove_carrinho'),
    path('carrinho/limpar/', limpar_carrinho, name='limpar_carrinho'),
]