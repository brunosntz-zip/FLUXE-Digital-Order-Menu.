# Fluxe - Cardápio Digital com Autoatendimento

![Status do Projeto](https://img.shields.io/badge/status-em_desenvolvimento-yellow)
![Backend](https://img.shields.io/badge/backend-Django-092E20?style=flat&logo=django&logoColor=white)
![Database](https://img.shields.io/badge/database-PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![Frontend](https://img.shields.io/badge/frontend-JS%20Vanilla-F7DF1E?style=flat&logo=javascript&logoColor=black)

Projeto Integrador (P.I.) do 4º semestre de Análise e Desenvolvimento de Sistemas. Este projeto é um MVP (Produto Mínimo Viável) de uma plataforma de gestão de comandas e autoatendimento para bares, restaurantes e casas de show.

## 1. O Problema
Em ambientes lotados (bares, baladas, shows), o processo de chamar um garçom, fazer um pedido e esperar por ele gera atrito, frustração para o cliente e perda de receita para o estabelecimento.

## 2. A Solução: Fluxe
O Fluxe substitui o controle manual por uma solução digital ágil, inspirada em plataformas como o ZIG. O cliente escaneia um QR Code, acessa o cardápio e faz o pedido diretamente pelo seu smartphone.

### Diferenciais do Nosso Modelo (Modelo "Balada")
O grande diferencial deste projeto é o foco na mobilidade do cliente, ideal para casas de show:
* **Comanda por Cliente (CPF):** A comanda é vinculada ao CPF do cliente, não a uma mesa física.
* **Cliente Móvel:** O cliente pode se locomover pelo evento e pedir de diferentes pontos (Bar 1, Pista, Camarote).
* **Modelo Híbrido:** Otimiza a função do garçom, que pode lançar pedidos para clientes no método tradicional, mas foca no autoatendimento.

## 3. Tecnologias Utilizadas (Stack)
Este projeto utiliza uma arquitetura MVC com Django servindo APIs REST para o frontend.

* **Frontend:** HTML5, CSS3 e JavaScript puro (Vanilla JS) consumindo API interna.
* **Backend:** **Python & Django** (Django REST Framework).
* **Banco de Dados:** **PostgreSQL** (Hospedado no Supabase).
* **Infraestrutura:** Supabase (Database Hosting & Storage).

## 4. Como Rodar o Projeto

O projeto requer Python instalado. Siga os passos abaixo:

1.  **Clone este repositório:**
    ```bash
    git clone [URL_DO_SEU_REPO_GIT]
    cd P.I4
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install django djangorestframework psycopg2-binary dj-database-url
    ```

4.  **Configure o Banco de Dados:**
    Certifique-se de que a string de conexão do Supabase está configurada no `settings.py` ou nas variáveis de ambiente.

5.  **Execute as Migrações (Sincronizar Banco):**
    ```bash
    cd fluxe_backend
    python manage.py migrate
    ```

6.  **Inicie o Servidor:**
    ```bash
    python manage.py runserver
    ```

7.  **Acesse o Sistema:**
    * **Cardápio (Home):** `http://127.0.0.1:8000/`
    * **Painel Administrativo:** `http://127.0.0.1:8000/admin/`

## 5. Estrutura do Backend (Django)
* **API REST:** Endpoints em `/api/produtos/`, `/api/categorias/` e `/api/populares/`.
* **Admin:** Interface para cadastro de produtos e gestão de "Queridinhos" (Destaques).
* **Session:** Gerenciamento de carrinho de compras via sessão do servidor.