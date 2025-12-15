from rest_framework import serializers
from .models import CategoriaProduto, Produto

class CategoriaProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProduto
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'