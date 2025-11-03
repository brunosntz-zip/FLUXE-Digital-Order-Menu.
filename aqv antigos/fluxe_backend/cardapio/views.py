from django.shortcuts import render
from rest_framework import viewsets
from .models import CategoriaProduto
from .serializers import CategoriaProdutoSerializer

class CategoriaProdutoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaProduto.objects.all().order_by('ordem_exibicao')
    serializer_class = CategoriaProdutoSerializer
