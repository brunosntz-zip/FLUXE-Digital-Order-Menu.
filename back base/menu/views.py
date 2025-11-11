from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def center_menu(request):
    
    return render(request, 'tela-inicial-cardapio.html')

def detail_iten(request):
    
    return render(request, 'detalhes.html')