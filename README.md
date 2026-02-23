# ⚡ FLUXE. - Cardápio Digital com Autoatendimento

<div align="center">

[![Deploy with Vercel](https://vercel.com/button)](https://fluxe-digital-order-menu.vercel.app)
![Status](https://img.shields.io/badge/Status-MVP%20Online-2ea44f?style=flat&logo=vercel&logoColor=white)

<br>

<img src="https://skillicons.dev/icons?i=python,django,postgres,js,html,css,vercel&perline=7" />

</div>

> **Projeto Integrador (P.I.) do 4º semestre de Análise e Desenvolvimento de Sistemas.**

### 🚀 [Acesse o MVP ao Vivo (Demo)](https://fluxe-digital-order-menu.vercel.app)

O **Fluxe** é uma plataforma de autoatendimento criada para reduzir filas, aumentar o giro de pedidos e modernizar a experiência em bares, baladas e eventos. Focado na mobilidade, permite que o cliente faça pedidos de qualquer lugar do estabelecimento sem depender do garçom.

---

## 📱 Screenshots

| Cardápio Mobile | Detalhes & Cross-Selling | Checkout Híbrido (Novo) |
|:---:|:---:|:---:|
| <img src="docs/screenshots/home.png" width="200" alt="Home Screen" /> | <img src="docs/screenshots/detalhes.png" width="200" alt="Detalhes" /> | <img src="docs/screenshots/carrinho.png" width="200" alt="Carrinho" /> |

*(O projeto é Mobile-First. Para melhor experiência, acesse pelo celular)*

---

## 1. O Problema 🧩
Em ambientes de alto fluxo (bares lotados, shows), o modelo tradicional gera atrito:
* Dificuldade de chamar o garçom.
* Longas esperas apenas para pedir uma bebida simples.
* Perda de receita por desistência do cliente.

## 2. A Solução: Fluxe 💡
Uma aplicação web que digitaliza o processo. Ao escanear o QR Code, o cliente acessa o cardápio, monta seu pedido e envia para a produção instantaneamente.

### Diferenciais do Modelo (Foco em UX e Vendas)
* **📍 Cliente Móvel (Comanda via CPF):** A comanda segue o cliente, não a mesa. Ideal para quem transita entre pista, bar e camarote.
* **🔥 Cross-Selling Inteligente:** O sistema sugere acompanhamentos automaticamente na tela de detalhes (ex: *Whisky* puxa sugestão de *Gelo de Coco* e *Red Bull*), aumentando o ticket médio.
* **⚡ Carrinho AJAX & Zero Refresh:** Adição de itens e atualização de quantidade sem recarregar a página, garantindo fluidez mesmo em conexões instáveis (3G/4G).
* **🛒 Checkout Flexível:** UX otimizada onde o cliente escolhe se vai **Buscar no Bar** 🍺 (padrão balada) ou se deseja serviço **Na Mesa** 🛎️.

---

## 3. Tecnologias Utilizadas (Stack) 🛠️

A arquitetura segue o padrão **MVC (Model-View-Controller)**, priorizando performance e escalabilidade na nuvem.

* **Frontend:**
    * **HTML5 & CSS3 Moderno:** Layout responsivo, animações nativas (Bottom Sheet) e Design System próprio.
    * **JavaScript (Vanilla):** Zero dependência de frameworks pesados para garantir carregamento instantâneo.
* **Backend:**
    * **Python & Django:** Framework robusto para regras de negócio complexas.
    * **Django REST Framework:** API para comunicação assíncrona com o front.
    * **Django Admin Personalizado:** Painel de gestão otimizado para o estabelecimento.
* **Infraestrutura & Dados:**
    * **PostgreSQL:** Hospedado no **Supabase**.
    * **Vercel:** Deploy Serverless escalável.
    * **Whitenoise:** Otimização de arquivos estáticos para alta performance.

---

## 4. Como Rodar Localmente ▶️

Pré-requisitos: Python 3.10+ instalado.

1.  **Clone este repositório:**
    ```bash
    git clone [https://github.com/brunosntz/fluxe-digital-order-menu.git](https://github.com/brunosntz/fluxe-digital-order-menu.git)
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
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados:**
    * Crie um arquivo `.env` na raiz com sua URL do Supabase ou use o banco local SQLite (padrão de dev).

5.  **Execute as Migrações:**
    ```bash
    cd fluxe_backend
    python manage.py migrate
    ```

6.  **Inicie o Servidor:**
    ```bash
    python manage.py runserver
    ```

7.  **Acesse o Sistema:**
    * **📱 Cardápio (Cliente):** `http://127.0.0.1:8000/`
    * **⚙️ Painel Administrativo:** `http://127.0.0.1:8000/admin/`

---

## 5. Estrutura e Roadmap 🔮

**Backend Structure:**
* **API Endpoints:** `/api/produtos/`, `/api/categorias/`, `/api/fechar_pedido/` (Fluxo completo via JSON).
* **Admin:** Gestão de cardápio, controle de "Queridinhos" e Pedidos em tempo real.

**Próximos Passos (Backlog):**
* [ ] Integração com Pagamento (Pix/Cartão).
* [ ] Dashboard KDS (Kitchen Display System) para a cozinha.
* [ ] Histórico de pedidos do cliente.

---

<p align="center">
  coded by: <strong>brunosntz</strong> 🎭
</p>
