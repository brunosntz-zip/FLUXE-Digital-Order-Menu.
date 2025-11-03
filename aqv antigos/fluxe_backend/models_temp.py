# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CategoriaProduto(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey('Restaurante', models.DO_NOTHING)
    nome = models.CharField(max_length=60)
    ordem_exibicao = models.IntegerField(blank=True, null=True)
    descricao = models.CharField(max_length=255, blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    criado_em = models.DateTimeField(blank=True, null=True)
    atualizado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoria_produto'


class Cliente(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey('Restaurante', models.DO_NOTHING)
    cpf = models.CharField(max_length=11)
    nome = models.CharField(max_length=100, blank=True, null=True)
    criado_em = models.DateTimeField(blank=True, null=True)
    atualizado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'
        unique_together = (('restaurante', 'cpf'),)


class Comanda(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey('Restaurante', models.DO_NOTHING)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)
    status = models.CharField(max_length=12)
    total_atual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    aberta_em = models.DateTimeField(blank=True, null=True)
    encerrada_em = models.DateTimeField(blank=True, null=True)
    encerrada_por = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='encerrada_por', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comanda'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ItemPedido(models.Model):
    id = models.UUIDField(primary_key=True)
    pedido = models.ForeignKey('Pedido', models.DO_NOTHING)
    produto = models.ForeignKey('Produto', models.DO_NOTHING, blank=True, null=True)
    nome_produto_snapshot = models.CharField(max_length=100)
    preco_unitario_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    total_item = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item_pedido'


class Mesa(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey('Restaurante', models.DO_NOTHING)
    numero = models.CharField(max_length=10)
    qr_code_slug = models.CharField(unique=True, max_length=120)
    ativo = models.BooleanField(blank=True, null=True)
    criado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mesa'


class Pedido(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey('Restaurante', models.DO_NOTHING)
    comanda = models.ForeignKey(Comanda, models.DO_NOTHING)
    mesa = models.ForeignKey(Mesa, models.DO_NOTHING)
    status = models.CharField(max_length=15)
    observacao = models.CharField(max_length=255, blank=True, null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(blank=True, null=True)
    preparado_em = models.DateTimeField(blank=True, null=True)
    entregue_em = models.DateTimeField(blank=True, null=True)
    atualizado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedido'


class PedidoStatusHistorico(models.Model):
    id = models.UUIDField(primary_key=True)
    pedido = models.ForeignKey(Pedido, models.DO_NOTHING)
    status = models.CharField(max_length=15)
    alterado_por = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='alterado_por', blank=True, null=True)
    motivo = models.CharField(max_length=255, blank=True, null=True)
    alterado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedido_status_historico'


class Produto(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey('Restaurante', models.DO_NOTHING)
    categoria = models.ForeignKey(CategoriaProduto, models.DO_NOTHING)
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
        managed = False
        db_table = 'produto'


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
        managed = False
        db_table = 'restaurante'


class Usuario(models.Model):
    id = models.UUIDField(primary_key=True)
    restaurante = models.ForeignKey(Restaurante, models.DO_NOTHING)
    nome = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=120)
    senha_hash = models.CharField(max_length=255)
    perfil = models.CharField(max_length=20)
    ativo = models.BooleanField(blank=True, null=True)
    ultimo_login_em = models.DateTimeField(blank=True, null=True)
    criado_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'
