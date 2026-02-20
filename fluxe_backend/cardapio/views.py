from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Agora importamos todos os models necessários para o pedido
from .models import CategoriaProduto, Produto, Restaurante, Cliente, Comanda, Mesa, Pedido, ItemPedido
from .serializers import CategoriaProdutoSerializer, ProdutoSerializer

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

# --- FUNÇÕES AUXILIARES ---
def get_qtd_carrinho(session):
    carrinho = session.get('carrinho', {})
    return sum(carrinho.values())

def excluir_item_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto_id = str(produto_id)

    if produto_id in carrinho:
        del carrinho[produto_id]

    request.session['carrinho'] = carrinho
    request.session.modified = True
    return redirect('ver_carrinho')


# --- VIEWS (Páginas HTML) ---
def home(request):
    ID_OFICIAL = 'b5bcffc5-90c7-4e76-bd19-5c56dbf31b3d'
    restaurante = Restaurante.objects.filter(id=ID_OFICIAL).first()

    if not restaurante:
        restaurante = Restaurante.objects.filter(ativo=True).first()

    qtd = get_qtd_carrinho(request.session)
    
    context = {
        'qtd_carrinho': qtd,
        'restaurante': restaurante, 
        'cliente_logado': request.session.get('cpf_cliente', None)
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

@require_http_methods(["GET", "POST"])
def adicionar_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    produto_id = str(produto_id)
    
    if request.method == 'POST':
        quantidade_form = int(request.POST.get('quantidade', 1))
        if produto_id in carrinho:
            carrinho[produto_id] += quantidade_form
        else:
            carrinho[produto_id] = quantidade_form
    else:
        if produto_id in carrinho:
            carrinho[produto_id] += 1
        else:
            carrinho[produto_id] = 1
        
    request.session['carrinho'] = carrinho
    request.session.modified = True
    
    qtd_total = sum(carrinho.values())

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'qtd': qtd_total, 'status': 'sucesso'})

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

# --- APIS DE NEGÓCIO (FLUXE ZIG) ---

@csrf_exempt 
@require_http_methods(["POST"])
def identificar_cliente(request):
    try:
        data = json.loads(request.body)
        cpf = data.get('cpf')
        cpf_limpo = ''.join(filter(str.isdigit, str(cpf)))

        if not cpf_limpo or len(cpf_limpo) != 11:
             return JsonResponse({'status': 'erro', 'mensagem': 'CPF inválido'}, status=400)

        ID_RESTAURANTE = 'b5bcffc5-90c7-4e76-bd19-5c56dbf31b3d'
        
        # 1. Tenta achar o cliente (NÃO CRIA MAIS AUTOMATICAMENTE!)
        cliente = Cliente.objects.filter(cpf=cpf_limpo, restaurante_id=ID_RESTAURANTE).first()
        
        if not cliente:
             return JsonResponse({'status': 'erro', 'mensagem': 'CPF não encontrado. Vá ao caixa abrir sua comanda!'}, status=404)

        # 2. Busca uma comanda ABERTA
        comanda = Comanda.objects.filter(cliente=cliente, restaurante_id=ID_RESTAURANTE, status='ABERTA').first()

        if not comanda:
            return JsonResponse({'status': 'erro', 'mensagem': 'Você não possui uma comanda aberta. Fale com um atendente.'}, status=403)

        # 3. Salva na Sessão (Login do cliente)
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


@csrf_exempt
@require_http_methods(["POST"])
def fechar_pedido(request):
    try:
        data = json.loads(request.body)
        carrinho = request.session.get('carrinho', {})
        
        if not carrinho:
            return JsonResponse({'status': 'erro', 'msg': 'Seu carrinho está vazio!'}, status=400)

        cpf_digitado = data.get('cpf', '').replace('.', '').replace('-', '')
        tipo_entrega = data.get('tipo_entrega') # 'retirada' ou 'mesa'
        numero_mesa = data.get('numero_mesa')

        ID_RESTAURANTE = 'b5bcffc5-90c7-4e76-bd19-5c56dbf31b3d'
        
        # 1. Puxa da sessão (se já estiver logado) ou valida o CPF enviado
        cliente_id = request.session.get('cliente_id')
        if cliente_id:
            cliente = Cliente.objects.filter(id=cliente_id).first()
        else:
            cliente = Cliente.objects.filter(cpf=cpf_digitado, restaurante_id=ID_RESTAURANTE).first()

        if not cliente:
            return JsonResponse({'status': 'erro', 'msg': 'CPF não encontrado. Procure o caixa!'}, status=404)

        # 2. Verifica se a comanda está aberta
        comanda = Comanda.objects.filter(cliente=cliente, restaurante_id=ID_RESTAURANTE, status='ABERTA').first()
        if not comanda:
            return JsonResponse({'status': 'erro', 'msg': 'Sua comanda não está aberta!'}, status=403)

        # 3. Resolve a Mesa
        obj_mesa = None
        if tipo_entrega == 'mesa':
            if not numero_mesa:
                return JsonResponse({'status': 'erro', 'msg': 'Informe o número da mesa!'}, status=400)
            
            obj_mesa = Mesa.objects.filter(numero=numero_mesa, restaurante_id=ID_RESTAURANTE).first()
            if not obj_mesa:
                 return JsonResponse({'status': 'erro', 'msg': f'Mesa {numero_mesa} não existe!'}, status=404)

        # 4. Cria o Pedido Oficial
        novo_pedido = Pedido.objects.create(
            restaurante_id=ID_RESTAURANTE,
            comanda=comanda,
            mesa=obj_mesa, 
            status='PENDENTE', # Vai aparecer no painel da cozinha
            tipo_entrega=tipo_entrega.upper() if hasattr(Pedido, 'tipo_entrega') else '', # Segurança caso esqueça a migration
            valor_total=0 
        )

        total_pedido = 0
        
        # 5. Salva Itens
        produtos_db = Produto.objects.filter(id__in=carrinho.keys())
        for produto in produtos_db:
            qtd = carrinho[str(produto.id)]
            total_item = produto.preco_atual * qtd
            total_pedido += total_item
            
            ItemPedido.objects.create(
                pedido=novo_pedido,
                produto=produto,
                nome_produto_snapshot=produto.nome,
                preco_unitario_snapshot=produto.preco_atual,
                quantidade=qtd,
                total_item=total_item
            )

        # 6. Atualiza Totais
        novo_pedido.valor_total = total_pedido
        novo_pedido.save()
        
        # Soma todos os pedidos da comanda para atualizar o total dela
        pedidos_da_comanda = Pedido.objects.filter(comanda=comanda)
        comanda.total_atual = sum(p.valor_total for p in pedidos_da_comanda)
        comanda.save()

        # 7. Limpa o Carrinho
        request.session['carrinho'] = {}
        request.session.modified = True

        # Gera o tokenzinho bonito pro cliente buscar no bar
        token_retirada = f"P-{str(novo_pedido.id)[:4].upper()}"

        return JsonResponse({
            'status': 'sucesso', 
            'pedido_id': str(novo_pedido.id),
            'token': token_retirada,
            'tipo_entrega': tipo_entrega
        })

    except Exception as e:
        print(f"Erro Crítico ao fechar pedido: {e}")
        return JsonResponse({'status': 'erro', 'msg': 'Erro interno. Tente novamente.'}, status=500)