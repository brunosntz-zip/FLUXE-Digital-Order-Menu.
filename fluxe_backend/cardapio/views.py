from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import CategoriaProduto, Produto
from .serializers import CategoriaProdutoSerializer, ProdutoSerializer

# --- API REST ---

class CategoriaProdutoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProduto.objects.all().order_by('ordem_exibicao')
    serializer_class = CategoriaProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class ProdutoPopularViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Produto.objects.filter(ativo=True, eh_popular=True)
    serializer_class = ProdutoSerializer

# --- FUNÇÃO AUXILIAR (Conta quantos itens tem no carrinho) ---
def get_qtd_carrinho(session):
    carrinho = session.get('carrinho', {})
    # Soma todas as quantidades (ex: 2 cervejas + 1 espetinho = 3)
    return sum(carrinho.values())

# --- VIEWS (Páginas HTML) ---

def home(request):
    # Calcula a quantidade para mostrar na bolinha vermelha
    qtd = get_qtd_carrinho(request.session)
    return render(request, 'home.html', {'qtd_carrinho': qtd})

def detalhes(request):
    # Também passamos a qtd aqui, caso você queira mostrar a bolinha na tela de detalhes
    qtd = get_qtd_carrinho(request.session)
    return render(request, 'detalhes.html', {'qtd_carrinho': qtd})

def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens_carrinho = []
    total_geral = 0
    
    if carrinho:
        produtos_db = Produto.objects.filter(id__in=carrinho.keys())
        for produto in produtos_db:
            # Converte ID para string para garantir que acha no dicionário
            qtd = carrinho.get(str(produto.id))
            if qtd:
                subtotal = produto.preco_atual * qtd
                total_geral += subtotal
                itens_carrinho.append({
                    'produto': produto,
                    'quantidade': qtd,
                    'subtotal': subtotal
                })
    
    context = {
        'itens': itens_carrinho, 
        'total': total_geral,
        'qtd_carrinho': get_qtd_carrinho(request.session)
    }
    return render(request, 'carrinho.html', context)

def adicionar_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto_id = str(produto_id) # garante q a chave é STRING
    
    if produto_id in carrinho:
        carrinho[produto_id] += 1
    else:
        carrinho[produto_id] = 1
        
    request.session['carrinho'] = carrinho
    request.session.modified = True
    return redirect('ver_carrinho')

def remover_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto_id = str(produto_id)
    
    if produto_id in carrinho:
        carrinho[produto_id] -= 1
        if carrinho[produto_id] <= 0:
            del carrinho[produto_id]
            
    request.session['carrinho'] = carrinho
    request.session.modified = True
    return redirect('ver_carrinho')

def limpar_carrinho(request):
    if 'carrinho' in request.session:
        del request.session['carrinho']
        request.session.modified = True
    return redirect('ver_carrinho')