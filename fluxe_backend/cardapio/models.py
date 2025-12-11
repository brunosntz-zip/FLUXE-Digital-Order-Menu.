from django.db import models

class Restaurante(models.Model):
    id = models.UUIDField(primary_key=True)
    nome = models.CharField(max_length=100)
    slug = models.CharField(unique=True, max_length=80)
    fuso_horario = models.CharField(max_length=40)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    criado_em = models.DateTimeField(blank=True, null=True)
    atualizado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'restaurante'
    
    def __str__(self):
        return self.nome 

class CategoriaProduto(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey('Restaurante', models.PROTECT) 
    nome = models.CharField(max_length=60)
    ordem_exibicao = models.IntegerField(blank=True, null=True)
    descricao = models.CharField(max_length=255, blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    criado_em = models.DateTimeField(blank=True, null=True)
    atualizado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'categoria_produto'

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey('Restaurante', models.PROTECT) 
    cpf = models.CharField(max_length=11)
    nome = models.CharField(max_length=100, blank=True, null=True)
    criado_em = models.DateTimeField(blank=True, null=True)
    atualizado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
       
        db_table = 'cliente'
        unique_together = (('restaurante', 'cpf'),)

    def __str__(self):
        return f"{self.nome} ({self.cpf})" 

class Usuario(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey(Restaurante, models.PROTECT) 
    nome = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=120)
    senha_hash = models.CharField(max_length=255)
    perfil = models.CharField(max_length=20)
    ativo = models.BooleanField(blank=True, null=True)
    ultimo_login_em = models.DateTimeField(blank=True, null=True)
    criado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'usuario'

    def __str__(self):
        return self.nome 

class Comanda(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey('Restaurante', models.PROTECT) 
    cliente = models.ForeignKey(Cliente, models.PROTECT) 
    status = models.CharField(max_length=12)
    total_atual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    aberta_em = models.DateTimeField(blank=True, null=True)
    encerrada_em = models.DateTimeField(blank=True, null=True)
    encerrada_por = models.ForeignKey('Usuario', models.PROTECT, db_column='encerrada_por', blank=True, null=True) # <-- CORRIGIDO

    class Meta:
        
        db_table = 'comanda'

    def __str__(self):
        return f"Comanda {self.id} (Cliente: {self.cliente.nome})" 

class Mesa(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey('Restaurante', models.PROTECT) 
    numero = models.CharField(max_length=10)
    qr_code_slug = models.CharField(unique=True, max_length=120)
    ativo = models.BooleanField(blank=True, null=True)
    criado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'mesa'

    def __str__(self):
        return self.numero 

class Produto(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey('Restaurante', models.PROTECT) 
    categoria = models.ForeignKey(CategoriaProduto, models.PROTECT) 
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255, blank=True, null=True)
    preco_atual = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=60, blank=True, null=True)
    foto_url = models.CharField(max_length=255, blank=True, null=True)
    ordem_exibicao = models.IntegerField(blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    criado_em = models.DateTimeField(blank=True, null=True)
    atualizado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'produto'

    def __str__(self):
        return self.nome 

class Pedido(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey('Restaurante', models.PROTECT) 
    comanda = models.ForeignKey(Comanda, models.PROTECT) 
    mesa = models.ForeignKey(Mesa, models.PROTECT) 
    status = models.CharField(max_length=15)
    observacao = models.CharField(max_length=255, blank=True, null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(blank=True, null=True)
    preparado_em = models.DateTimeField(blank=True, null=True)
    entregue_em = models.DateTimeField(blank=True, null=True)
    atualizado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'pedido'

    def __str__(self):
        return f"Pedido {self.id} (Comanda: {self.comanda.id})" # Adiciona um nome legível no Admin

class ItemPedido(models.Model):
    id = models.UUIDField(primary_key=True)
    pedido = models.ForeignKey('Pedido', models.PROTECT) # <-- CORRIGIDO
    produto = models.ForeignKey('Produto', models.PROTECT, blank=True, null=True) # <-- CORRIGIDO
    nome_produto_snapshot = models.CharField(max_length=100)
    preco_unitario_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    total_item = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
       
        db_table = 'item_pedido'

class PedidoStatusHistorico(models.Model):
    id = models.UUIDField(primary_key=True)
    pedido = models.ForeignKey(Pedido, models.PROTECT) # <-- CORRIGIDO
    status = models.CharField(max_length=15)
    alterado_por = models.ForeignKey('Usuario', models.PROTECT, db_column='alterado_por', blank=True, null=True) # <-- CORRIGIDO
    motivo = models.CharField(max_length=255, blank=True, null=True)
    alterado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        
        db_table = 'pedido_status_historico'