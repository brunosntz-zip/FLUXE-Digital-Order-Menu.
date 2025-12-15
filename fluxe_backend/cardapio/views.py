from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import CategoriaProduto, Produto
from .serializers import CategoriaProdutoSerializer, ProdutoSerializer

# API REST

class CategoriaProdutoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProduto.objects.all().order_by('ordem_exibicao')
    serializer_class = CategoriaProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class ProdutoPopularViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Produto.objects.filter(ativo=True)
    serializer_class = ProdutoSerializer

def home(request):
    return render(request, 'home.html')

def detalhes(request):
    return render(request, 'detalhes.html')

def ver_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens_carrinho = []
    total_geral = 0
    
    if carrinho:
        produtos_db = Produto.objects.filter(id__in=carrinho.keys())
        for produto in produtos_db:
            qtd = carrinho.get(str(produto.id))
            if qtd:
                subtotal = produto.preco_atual * qtd
                total_geral += subtotal
                itens_carrinho.append({
                    'produto': produto,
                    'quantidade': qtd,
                    'subtotal': subtotal
                })
    
    context = {'itens': itens_carrinho, 'total': total_geral}
    return render(request, 'carrinho.html', context)

def adicionar_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    if produto_id in carrinho:
        carrinho[produto_id] += 1
    else:
        carrinho[produto_id] = 1
    request.session['carrinho'] = carrinho
    return redirect('ver_carrinho')

def remover_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    if produto_id in carrinho:
        carrinho[produto_id] -= 1
        if carrinho[produto_id] <= 0:
            del carrinho[produto_id]
    request.session['carrinho'] = carrinho
    return redirect('ver_carrinho')

def limpar_carrinho(request):
    if 'carrinho' in request.session:
        del request.session['carrinho']
    return redirect('ver_carrinho')