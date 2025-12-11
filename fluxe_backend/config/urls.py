from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from cardapio.views import CategoriaProdutoViewSet, adicionar_carrinho, ver_carrinho, remover_carrinho, limpar_carrinho

router = routers.DefaultRouter()
router.register(r'categorias', CategoriaProdutoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # --- ROTAS DO CARRINHO ---
    path('carrinho/', ver_carrinho, name='ver_carrinho'),
    path('carrinho/add/<str:produto_id>/', adicionar_carrinho, name='add_carrinho'),
    path('carrinho/remove/<str:produto_id>/', remover_carrinho, name='remove_carrinho'),
    path('carrinho/limpar/', limpar_carrinho, name='limpar_carrinho'),
]