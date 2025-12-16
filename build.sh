#!/usr/bin/env bash
# Sair se der erro
set -o errexit

# Instalar dependências
pip install -r requirements.txt

# Entrar na pasta do projeto Django
cd fluxe_backend

# Coletar arquivos estáticos e rodar migrações
python manage.py collectstatic --no-input
python manage.py migrate