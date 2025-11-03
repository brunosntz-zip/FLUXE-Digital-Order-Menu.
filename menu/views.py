from django.shortcuts import render
from django.http import HttpResponse


def menu(request):
    return render(request, 'tela-inicial-cardapio.html')
