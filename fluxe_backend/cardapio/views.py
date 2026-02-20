from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Importamos todos os "Moldes" (Models) do banco de dados que vamos precisar usar aqui
from .models import CategoriaProduto, Produto, Restaurante, Cliente, Comanda, Mesa, Pedido, ItemPedido
from .serializers import CategoriaProdutoSerializer, ProdutoSerializer

# ==========================================
# 📡 API REST (Usado no futuro pelo Front ou App)
# ==========================================
class CategoriaProdutoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProduto.objects.all().order_by('ordem_exibicao')
    serializer_class = CategoriaProdutoSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class ProdutoPopularViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Produto.objects.filter(ativo=True, eh_popular=True)
    serializer_class = ProdutoSerializer


# ==========================================
# 🛠️ FUNÇÕES AUXILIARES (Ferramentas de uso interno)
# ==========================================

def get_qtd_carrinho(session):
    """ Olha para a sessão (memória temporária do navegador) e conta quantos itens tem no carrinho """
    carrinho = session.get('carrinho', {})
    return sum(carrinho.values())

def excluir_item_carrinho(request, produto_id):
    """ Remove um produto completamente do carrinho, independente da quantidade """
    carrinho = request.session.get('carrinho', {})
    produto_id = str(produto_id)

    if produto_id in carrinho:
        del carrinho[produto_id] # Deleta o item do dicionário

    # Salva o carrinho atualizado de volta na sessão
    request.session['carrinho'] = carrinho
    request.session.modified = True
    return redirect('ver_carrinho')


# ==========================================
# 🖥️ VIEWS DE TELAS (O que o cliente vê)
# ==========================================

def home(request):
    """ Carrega a tela inicial do cardápio """
    # ID fixo do nosso bar de testes (Lado B)
    ID_OFICIAL = 'b5bcffc5-90c7-4e76-bd19-5c56dbf31b3d'
    
    # Busca o restaurante no banco. Se não achar pelo ID, pega o primeiro que estiver ativo (Fallback de segurança)
    restaurante = Restaurante.objects.filter(id=ID_OFICIAL).first()
    if not restaurante:
        restaurante = Restaurante.objects.filter(ativo=True).first()

    qtd = get_qtd_carrinho(request.session)
    
    # Empacota os dados para mandar pro HTML
    context = {
        'qtd_carrinho': qtd,
        'restaurante': restaurante, 
        'cliente_logado': request.session.get('cpf_cliente', None) # Se tiver CPF aqui, o front sabe que tá logado
    }
    
    return render(request, 'home.html', context)

def detalhes(request, produto_id):
    """ Tela de detalhes de um produto específico """
    # Tenta achar o produto. Se não existir, dá erro 404 (Página não encontrada) automático
    produto = get_object_or_404(Produto, id=produto_id)
    qtd = get_qtd_carrinho(request.session)
    return render(request, 'detalhes.html', {'produto': produto, 'qtd_carrinho': qtd})

def ver_carrinho(request):
    """ Monta a tela do carrinho puxando os itens da sessão e somando os valores """
    carrinho = request.session.get('carrinho', {})
    itens_carrinho = []
    total_geral = 0
    
    if carrinho:
        # Busca de uma vez só todos os produtos que estão no carrinho
        produtos_db = Produto.objects.filter(id__in=carrinho.keys())
        for produto in produtos_db:
            qtd = carrinho.get(str(produto.id))
            if qtd:
                subtotal = produto.preco_atual * qtd
                total_geral += subtotal
                # Adiciona na lista que vai pro HTML
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
    """ Adiciona um item ao carrinho. Funciona com clique normal (GET) ou formulário/AJAX (POST) """
    carrinho = request.session.get('carrinho', {})
    produto_id = str(produto_id)
    
    # Lógica de soma: Se mandou pelo form, usa a qtd do form. Se clicou no botão de +, soma 1.
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

    # Se a requisição veio do Javascript (AJAX Zero Refresh), devolve só um JSON em vez de recarregar a tela
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'qtd': qtd_total, 'status': 'sucesso'})

    # Se foi clique normal, redireciona de volta
    next_url = request.GET.get('next') or request.POST.get('next')
    if next_url:
        return redirect(next_url)
    
    return redirect('ver_carrinho') 

def remover_carrinho(request, produto_id):
    """ Subtrai 1 da quantidade. Se chegar a zero, remove o item do carrinho """
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
    """ Joga o carrinho fora (Botão de esvaziar) """
    if 'carrinho' in request.session:
        del request.session['carrinho']
        request.session.modified = True
    return redirect('ver_carrinho')


# ==========================================
# 🧠 APIS DE NEGÓCIO (O MOTOR DO CHECKOUT)
# ==========================================

@csrf_exempt 
@require_http_methods(["POST"])
def identificar_cliente(request):
    """ Verifica se o cliente existe e se tem comanda aberta antes de deixar ele pedir """
    try:
        data = json.loads(request.body)
        cpf = data.get('cpf')
        
        # Pega o que o usuário digitou e deixa só os números
        cpf_limpo = ''.join(filter(str.isdigit, str(cpf)))

        # Validação básica de tamanho de CPF
        if not cpf_limpo or len(cpf_limpo) != 11:
             return JsonResponse({'status': 'erro', 'mensagem': 'CPF inválido'}, status=400)

        ID_RESTAURANTE = 'b5bcffc5-90c7-4e76-bd19-5c56dbf31b3d'
        
        # 1. SEGURANÇA: Tenta achar o cliente. Se o Caixa (Admin) não cadastrou ele antes, barra aqui!
        cliente = Cliente.objects.filter(cpf=cpf_limpo, restaurante_id=ID_RESTAURANTE).first()
        if not cliente:
             return JsonResponse({'status': 'erro', 'mensagem': 'CPF não encontrado. Vá ao caixa abrir sua comanda!'}, status=404)

        # 2. Verifica se ele está com a comanda ABERTA na balada.
        comanda = Comanda.objects.filter(cliente=cliente, restaurante_id=ID_RESTAURANTE, status='ABERTA').first()
        if not comanda:
            return JsonResponse({'status': 'erro', 'mensagem': 'Você não possui uma comanda aberta. Fale com um atendente.'}, status=403)

        # 3. O Pulo do Gato: Se passou nas validações, salva os dados na Sessão (O famoso "Login silencioso")
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
    """ A função mais importante. Pega o carrinho, confere o cliente, cria o pedido e manda pra cozinha """
    try:
        data = json.loads(request.body)
        carrinho = request.session.get('carrinho', {})
        
        if not carrinho:
            return JsonResponse({'status': 'erro', 'msg': 'Seu carrinho está vazio!'}, status=400)

        # Extrai os dados que vieram do Javascript
        cpf_digitado = data.get('cpf', '').replace('.', '').replace('-', '')
        tipo_entrega = data.get('tipo_entrega') # Vem como 'retirada' ou 'mesa'
        numero_mesa = data.get('numero_mesa')

        ID_RESTAURANTE = 'b5bcffc5-90c7-4e76-bd19-5c56dbf31b3d'
        
        # 1. Identifica quem é o cliente (Lê da sessão se já logou, ou busca pelo CPF digitado na hora)
        cliente_id = request.session.get('cliente_id')
        if cliente_id:
            cliente = Cliente.objects.filter(id=cliente_id).first()
        else:
            cliente = Cliente.objects.filter(cpf=cpf_digitado, restaurante_id=ID_RESTAURANTE).first()

        if not cliente:
            return JsonResponse({'status': 'erro', 'msg': 'CPF não encontrado. Procure o caixa!'}, status=404)

        # 2. Confirma se a comanda dele não foi fechada no meio do processo
        comanda = Comanda.objects.filter(cliente=cliente, restaurante_id=ID_RESTAURANTE, status='ABERTA').first()
        if not comanda:
            return JsonResponse({'status': 'erro', 'msg': 'Sua comanda não está aberta!'}, status=403)

        # 3. LOGÍCA DE ENTREGA/MESA (Ajuste Crítico feito aqui!)
        obj_mesa = None
        is_retirada = True # Por padrão, assume que é buscar no bar
        
        if tipo_entrega == 'mesa':
            is_retirada = False # Se escolheu mesa, muda a flag
            if not numero_mesa:
                return JsonResponse({'status': 'erro', 'msg': 'Informe o número da mesa!'}, status=400)
            
            # Valida se a mesa realmente existe no bar
            obj_mesa = Mesa.objects.filter(numero=numero_mesa, restaurante_id=ID_RESTAURANTE).first()
            if not obj_mesa:
                 return JsonResponse({'status': 'erro', 'msg': f'Mesa {numero_mesa} não existe!'}, status=404)

        # 4. Cria o Pedido Oficial (A "Capa" do pedido)
        novo_pedido = Pedido.objects.create(
            restaurante_id=ID_RESTAURANTE,
            comanda=comanda,
            mesa=obj_mesa, 
            status='PENDENTE', # Vai aparecer no painel da cozinha
            eh_retirada=is_retirada, # Booleano correto que o banco pede
            valor_total=0 # Começa zerado, vamos somar os itens logo abaixo
        )

        total_pedido = 0
        
        # 5. Salva os Itens dentro do Pedido (A "Tripa" do pedido)
        produtos_db = Produto.objects.filter(id__in=carrinho.keys())
        for produto in produtos_db:
            qtd = carrinho[str(produto.id)]
            total_item = produto.preco_atual * qtd
            total_pedido += total_item
            
            # Cria a linha do item e salva o preço daquele momento (snapshot)
            ItemPedido.objects.create(
                pedido=novo_pedido,
                produto=produto,
                nome_produto_snapshot=produto.nome,
                preco_unitario_snapshot=produto.preco_atual,
                quantidade=qtd,
                total_item=total_item
            )

        # 6. Atualiza e salva o valor final do Pedido
        novo_pedido.valor_total = total_pedido
        novo_pedido.save()
        
        # Soma todos os pedidos para atualizar o total da Comanda (A conta do cliente!)
        pedidos_da_comanda = Pedido.objects.filter(comanda=comanda)
        comanda.total_atual = sum(p.valor_total for p in pedidos_da_comanda)
        comanda.save()

        # 7. Tudo certo! Esvazia o carrinho pra ele fazer novos pedidos depois
        request.session['carrinho'] = {}
        request.session.modified = True

        # Gera o tokenzinho bonito pro cliente buscar no bar (Ex: P-A8F2)
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