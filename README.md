# Fluxe - Cardápio Digital com Autoatendimento

![Status do Projeto](https://img.shields.io/badge/status-em_desenvolvimento-yellow)
![Tecnologia](https://img.shields.io/badge/backend-Supabase-green)
![Tecnologia](https://img.shields.io/badge/database-PostgreSQL-lightblue)
![Tecnologia](https://img.shields.io/badge/frontend-JS-orange)

[cite_start]Projeto Integrador (P.I.) do 4º semestre de Análise e Desenvolvimento de Sistemas[cite: 5]. [cite_start]Este projeto é um MVP (Produto Mínimo Viável) de uma plataforma de gestão de comandas e autoatendimento para bares, restaurantes e casas de show[cite: 3].

## 1. O Problema
[cite_start]Em ambientes lotados (bares, baladas, shows), o processo de chamar um garçom, fazer um pedido e esperar por ele gera atrito, frustração para o cliente e perda de receita para o estabelecimento[cite: 13].

## 2. A Solução: Fluxe
[cite_start]O Fluxe substitui o controle manual por uma solução digital ágil, inspirada em plataformas como o ZIG[cite: 9, 259]. [cite_start]O cliente escaneia um QR Code, acessa o cardápio e faz o pedido diretamente pelo seu smartphone[cite: 11].

### Diferenciais do Nosso Modelo (Modelo "Balada")
O grande diferencial deste projeto é o foco na mobilidade do cliente, ideal para casas de show:
* [cite_start]**Comanda por Cliente (CPF):** A comanda é vinculada ao CPF do cliente, não a uma mesa física[cite: 15].
* [cite_start]**Cliente Móvel:** O cliente pode se locomover pelo evento e pedir de diferentes pontos (Bar 1, Pista, Camarote)[cite: 16].
* [cite_start]**Modelo Híbrido:** Otimiza a função do garçom, que pode lançar pedidos para clientes no método tradicional, mas foca no autoatendimento[cite: 18].

## 3. Tecnologias Utilizadas (Stack)
Este projeto foi construído com uma arquitetura "backend-as-a-service" (BaaS) para agilidade no desenvolvimento.

* **Frontend:** HTML5, CSS3 e JavaScript puro (Vanilla JS).
* **Backend:** **Supabase** (BaaS)
* **Banco de Dados:** **PostgreSQL** (fornecido pelo Supabase)
* **Autenticação e Segurança:** Supabase RLS (Row Level Security).
* **Armazenamento de Arquivos:** Supabase Storage (para as fotos dos produtos).

## 4. Como Rodar o Projeto (Frontend)
O frontend é um site estático que consome a API do Supabase.

1.  Clone este repositório:
    ```bash
    git clone [URL_DO_SEU_REPO_GIT]
    ```
2.  Abra o projeto no VS Code.
3.  Instale a extensão [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer).
4.  Clique com o botão direito no arquivo `index.html` (ou `tela-inicial-cardapio.html`) e selecione "Open with Live Server".

## 5. Configuração do Backend (Supabase)
O backend é 100% gerenciado pelo Supabase. Para o frontend funcionar, o Supabase precisa estar configurado:

1.  **Chaves de API:** O `index.html` precisa ter as variáveis `SUPABASE_URL` e `SUPABASE_KEY` (anon key) preenchidas.
2.  **Banco de Dados:** As tabelas do PostgreSQL devem ser criadas usando o script (`script-postgres.sql`) presente neste repositório.
3.  **Segurança (RLS):** As Políticas de "Row Level Security" precisam estar ativas para permitir a leitura pública (`SELECT`) das tabelas `produto`, `categoria_produto`, etc., e a escrita (`INSERT`) nas tabelas `cliente`, `pedido`, etc..
4.  **Storage:** As fotos dos produtos devem ser enviadas para um Bucket público no Supabase Storage.
