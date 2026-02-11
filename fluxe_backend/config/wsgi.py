import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Adiciona a pasta 'fluxe_backend' ao caminho do Python
# Isso permite que ele encontre 'config' e 'cardapio'
current_path = Path(__file__).resolve().parent.parent
sys.path.append(str(current_path))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
app = application