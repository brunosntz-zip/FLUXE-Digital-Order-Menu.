# ⚡ Fluxe - Cardápio Digital com Autoatendimento

![Status](https://img.shields.io/badge/Status-MVP%20Funcional-success?style=for-the-badge&logo=statuspage&logoColor=white)
![Backend](https://img.shields.io/badge/Backend-Django%20REST-092E20?style=for-the-badge&logo=django&logoColor=white)
![Database](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-Vanilla%20JS-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

> **Projeto Integrador (P.I.) a partir do 4º semestre de Análise e Desenvolvimento de Sistemas.**

O **Fluxe** é uma plataforma de autoatendimento criada para reduzir filas, aumentar o giro de pedidos e modernizar a experiência em bares, baladas e eventos. Focado na mobilidade, permite que o cliente faça pedidos de qualquer lugar do estabelecimento sem depender do garçom.

---

## 📱 Screenshots

| Cardápio Mobile | Detalhes & Cross-Selling | Carrinho (AJAX) |
|:---:|:---:|:---:|
| <img src="docs/screenshots/home.png" width="200" alt="Home Screen" /> | <img src="docs/screenshots/detalhes.png" width="200" alt="Detalhes" /> | <img src="docs/screenshots/carrinho.png" width="200" alt="Carrinho" /> |

*(Adicione os prints na pasta `docs/screenshots` do seu projeto)*

---

## 1. O Problema 🧩
Em ambientes de alto fluxo (bares lotados, shows), o modelo tradicional gera atrito:
* Dificuldade de chamar o garçom.
* Longas esperas apenas para pedir uma bebida simples.
* Perda de receita por desistência do cliente.

## 2. A Solução: Fluxe 💡
Uma aplicação web **Mobile-First** que digitaliza o processo. Ao escanear o QR Code, o cliente acessa o cardápio, monta seu pedido e envia para a produção instantaneamente.

### Diferenciais do Modelo (Foco em UX e Vendas)
* **📍 Cliente Móvel (Comanda via CPF):** A comanda segue o cliente, não a mesa. Ideal para quem transita entre pista, bar e camarote.
* **🔥 Cross-Selling Inteligente:** O sistema sugere acompanhamentos automaticamente na tela de detalhes (ex: *Whisky* puxa sugestão de *Gelo de Coco* e *Red Bull*), aumentando o ticket médio.
* **⚡ Carrinho AJAX:** Adição de itens e atualização de quantidade sem recarregar a página (Zero Refresh), garantindo fluidez mesmo em 4G/5G.
* **🤝 Modelo Híbrido:** Não elimina o garçom, mas o transforma em um facilitador, permitindo também o lançamento manual quando necessário.

---

## 3. Tecnologias Utilizadas (Stack) 🛠️

A arquitetura segue o padrão **MVC (Model-View-Controller)**, priorizando performance e escalabilidade.

* **Frontend:**
    * **HTML5 & CSS3 Moderno:** Layout responsivo e animações nativas.
    * **JavaScript (Vanilla):** Zero dependência de frameworks pesados para garantir carregamento instantâneo.
* **Backend:**
    * **Python & Django:** Framework robusto para regras de negócio complexas.
    * **Django REST Framework:** API para comunicação assíncrona.
    * **Django Admin Personalizado:** Painel de gestão otimizado com widgets de seleção e filtros.
* **Banco de Dados & Infra:**
    * **PostgreSQL:** Hospedado no **Supabase**.
    * **Server-side Sessions:** Gerenciamento seguro de carrinho.

---

## 4. Como Rodar o Projeto ▶️

Pré-requisitos: Python 3.10+ instalado.

1.  **Clone este repositório:**
    ```bash
    git clone [https://github.com/SEU_USUARIO/fluxe-backend.git](https://github.com/SEU_USUARIO/fluxe-backend.git)
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
    * Crie um arquivo `.env` na raiz ou configure o `settings.py` com sua URL de conexão do Supabase/Postgres.

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
* **API Endpoints:** `/api/produtos/`, `/api/categorias/`, `/api/populares/` (Usados para carregamento dinâmico).
* **Admin:** Gestão de cardápio, controle de "Queridinhos" e Pedidos.

**Próximos Passos (Backlog):**
* [ ] Integração com Pagamento (Pix/Cartão).
* [ ] Dashboard KDS (Kitchen Display System) para a cozinha.
* [ ] Histórico de pedidos do cliente.

---

<p align="center">
  Desenvolvido por <strong>Bruno Santos</strong> 🚀
</p>
