from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import CategoriaProduto, Produto, Restaurante, Cliente, Comanda
from .serializers import CategoriaProdutoSerializer, ProdutoSerializer
from django.http import JsonResponse
import json

# API REST 

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
        'restaurante': restaurante, # AGORA SIM ESTAMOS MANDANDO PRO HTML
        'cliente_logado': request.session.get('cpf_cliente', None) # Manda pro front saber se já tá logado
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
        'qtd_carrinho': get_qtd_carrinho(request.session),
        'cliente_logado': request.session.get('cpf_cliente', None)
    }
    return render(request, 'carrinho.html', context)

@require_http_methods(["GET", "POST"]) # Aceita tanto clicar no link quanto enviar formulário
def adicionar_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto_id = str(produto_id)
    
    # (Lógica de adicionar mantém igual...)
    if request.method == 'POST':
        quantidade_form = int(request.POST.get('quantidade', 1))
        if produto_id in carrinho:
            carrinho[produto_id] += quantidade_form
        else:
            carrinho[produto_id] = quantidade_form
    else:
        # GET (Link da Home)
        if produto_id in carrinho:
            carrinho[produto_id] += 1
        else:
            carrinho[produto_id] = 1
        
    request.session['carrinho'] = carrinho
    request.session.modified = True
    
    # --- NOVIDADE AQUI 👇 ---
    # Calcula total de itens agora
    qtd_total = sum(carrinho.values())

    # Se o pedido veio com o carimbo "AJAX" (X-Requested-With), responde JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'qtd': qtd_total, 'status': 'sucesso'})
    # ------------------------

    # Fallback pro jeito antigo (para o formulário de detalhes funcionar normal)
    next_url = request.GET.get('next') or request.POST.get('next')
    if next_url:
        return redirect(next_url)
    
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

# --- NOVA API DE IDENTIFICAÇÃO (FLUXE ZIG) ---
@csrf_exempt 
@require_http_methods(["POST"])
def identificar_cliente(request):
    try:
        data = json.loads(request.body)
        cpf = data.get('cpf')
        # Limpa o CPF (remove pontos e traços se vier)
        cpf_limpo = ''.join(filter(str.isdigit, str(cpf)))

        if not cpf_limpo or len(cpf_limpo) != 11:
             return JsonResponse({'status': 'erro', 'mensagem': 'CPF inválido'}, status=400)

        # ID DO RESTAURANTE (Fixo por enquanto, depois pegamos dinâmico)
        ID_RESTAURANTE = 'b5bcffc5-90c7-4e76-bd19-5c56dbf31b3d'
        
        # 1. Busca ou Cria o Cliente
        cliente, created = Cliente.objects.get_or_create(
            cpf=cpf_limpo,
            restaurante_id=ID_RESTAURANTE,
            defaults={'nome': 'Cliente Novo'} 
        )

        # 2. Busca uma comanda ABERTA para este cliente
        comanda = Comanda.objects.filter(
            cliente=cliente,
            restaurante_id=ID_RESTAURANTE,
            status='ABERTA' # Garantir que o enum no banco bate com isso
        ).first()

        # 3. Se não tiver comanda aberta, cria uma nova
        if not comanda:
            comanda = Comanda.objects.create(
                cliente=cliente,
                restaurante_id=ID_RESTAURANTE,
                status='ABERTA'
            )

        # 4. O PULO DO GATO: Salva na Sessão (Cookie)
        request.session['cliente_id'] = str(cliente.id)
        request.session['comanda_id'] = str(comanda.id)
        request.session['cpf_cliente'] = cliente.cpf
        request.session.modified = True

        return JsonResponse({
            'status': 'sucesso', 
            'cliente': cliente.nome,
            'comanda_id': comanda.id
        })

    except Exception as e:
        print(f"Erro ao identificar: {e}")
        return JsonResponse({'status': 'erro', 'mensagem': 'Erro interno'}, status=500)