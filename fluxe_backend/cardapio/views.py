from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
# IMPORTS IMPORTANTES AQUI 👇
from .models import CategoriaProduto, Produto, Restaurante 
from .serializers import CategoriaProdutoSerializer, ProdutoSerializer

# --- API REST (Mantém igual) ---

class CategoriaProdutoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProduto.objects.all().order_by('ordem_exibicao')
    serializer_class = CategoriaProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class ProdutoPopularViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Produto.objects.filter(ativo=True, eh_popular=True)
    serializer_class = ProdutoSerializer

# --- FUNÇÃO AUXILIAR ---
def get_qtd_carrinho(session):
    carrinho = session.get('carrinho', {})
    return sum(carrinho.values())

# --- VIEWS (Páginas HTML) ---

def home(request):
    # ID OFICIAL DO BAR (Copiado do seu arquivo de texto)
    ID_OFICIAL = 'b5bcffc5-90c7-4e76-bd19-5c56dbf31b3d'
    
    # 1. Tenta buscar pelo ID exato
    restaurante = Restaurante.objects.filter(id=ID_OFICIAL).first()

    # --- DEBUG NO TERMINAL (Pra gente ver se funcionou) ---
    if not restaurante:
        print(f"\n⚠️ ALERTA: Não achei o restaurante pelo ID {ID_OFICIAL}!")
        print("🔍 Tentando pegar qualquer um ativo como fallback...")
        restaurante = Restaurante.objects.filter(ativo=True).first()
        
        if restaurante:
            print(f"✅ Fallback funcionou! Usando: {restaurante.nome}")
        else:
            print("❌ PERIGO: Nenhum restaurante ativo encontrado no banco!")
    else:
        print(f"\n✅ SUCESSO: Restaurante '{restaurante.nome}' carregado pelo ID!")
    # ------------------------------------------------------

    qtd = get_qtd_carrinho(request.session)
    
    context = {
        'qtd_carrinho': qtd,
        'restaurante': restaurante # AGORA SIM ESTAMOS MANDANDO PRO HTML
    }
    
    return render(request, 'home.html', context)

def detalhes(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    qtd = get_qtd_carrinho(request.session)
    return render(request, 'detalhes.html', {'produto': produto, 'qtd_carrinho': qtd})

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
    
    context = {
        'itens': itens_carrinho, 
        'total': total_geral,
        'qtd_carrinho': get_qtd_carrinho(request.session)
    }
    return render(request, 'carrinho.html', context)

def adicionar_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto_id = str(produto_id)
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