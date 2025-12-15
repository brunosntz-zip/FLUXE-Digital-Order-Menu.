document.addEventListener("DOMContentLoaded", () => {
    
      const SUPABASE_URL = 'https://fkxejnpjeoctlxiuhpvs.supabase.co';
      const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZreGVqbnBqZW9jdGx4aXVocHZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEyMjA1NDksImV4cCI6MjA3Njc5NjU0OX0.gwu5S7lLK4XjBMseNYQavBgWrfidGAgqo17HrfsbIWk'; 
    
      const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

      // Cache de produtos, ele carrega tudo.
      let todosOsProdutos = [];

      // Ela NÃO vai ao Supabase. Ela só "lê" da "gaveta".
      function renderizarProdutos(categoriaId) {
        console.log(`Renderizando produtos da "gaveta" para a categoria: ${categoriaId}`);

        const menuGrid = document.querySelector('.menu-grid');
        if (!menuGrid) { return; }
        
        // FILTRA a "gaveta" (todosOsProdutos)
        const produtosFiltrados = todosOsProdutos.filter(produto => produto.categoria_id === categoriaId);

        // Verifica se o filtro encontrou algo
        if (!produtosFiltrados || produtosFiltrados.length === 0) {
          console.warn("Nenhum produto encontrado para esta categoria.");
          menuGrid.innerHTML = "<p>Nenhum produto encontrado nesta categoria.</p>";
          return;
        }

        // Limpa o grid e desenha os produtos
        menuGrid.innerHTML = ''; 

        produtosFiltrados.forEach(produto => {
          const cardHTML = `
            <article class="card">
              <img class="thumb" src="${produto.foto_url}" alt="${produto.nome}">
              <div class="meta">
                <div class="name">${produto.nome}</div>
                <div class="desc">${produto.descricao || ''}</div>
                <div class="price">R$ ${produto.preco_atual}</div>
              </div>
              
              <a href="http://127.0.0.1:8000/carrinho/add/${produto.id}/" class="add" aria-label="Add ${produto.nome}">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                  <path d="M12 5v14M5 12h14" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </a>

            </article>
          `;
          menuGrid.insertAdjacentHTML('beforeend', cardHTML);
        });

        console.log("Cardápio renderizado da 'gaveta' com sucesso!");
      }
      
      // Função Mestra que carrega tudo
      async function carregarDadosIniciais() {
        console.log("Buscando TODOS os dados iniciais do Supabase...");
        
        const tabsContainer = document.querySelector('.tabs');
        const tituloCategoria = document.querySelector('#titulo-categoria');
        const menuGrid = document.querySelector('.menu-grid');

        if (!tabsContainer || !tituloCategoria || !menuGrid) {
          console.error("Erro: Um dos containers principais não foi encontrado!");
          return;
        }

        menuGrid.innerHTML = '<p>Carregando cardápio completo...</p>'; 

        // Puxa as CATEGORIAS
        const { data: categorias, errorCat } = await supabaseClient
          .from('categoria_produto')
          .select('*')
          .order('ordem_exibicao');

        // Puxa TODOS OS PRODUTOS
        const { data: produtos, errorProd } = await supabaseClient
          .from('produto')
          .select('*');

        // Checagem de Erros
        if (errorCat || errorProd) {
          console.error("Erro ao buscar categorias:", errorCat?.message);
          console.error("Erro ao buscar produtos:", errorProd?.message);
          alert("Ops! Não consegui carregar o cardápio. Verifique suas regras RLS (SELECT).");
          return;
        }

        // Salva os produtos na "gaveta"
        todosOsProdutos = produtos;
        console.log("Gaveta de produtos preenchida!", todosOsProdutos);

        // Limpa o container de tabs
        tabsContainer.innerHTML = '';
        
        // Cria os botões (tabs)
        categorias.forEach((categoria, index) => {
          const isActive = index === 0;
          const tabHTML = `
            <button class="tab ${isActive ? 'active' : ''}" data-categoria-id="${categoria.id}">
              ${categoria.nome}
            </button>
          `;
          tabsContainer.insertAdjacentHTML('beforeend', tabHTML);
        });
        
        tabsContainer.querySelectorAll('.tab').forEach(button => {
          button.addEventListener('click', () => {
            if (tabsContainer.querySelector('.tab.active')) {
                tabsContainer.querySelector('.tab.active').classList.remove('active');
            }
            button.classList.add('active');
            
            const categoriaId = button.dataset.categoriaId;
            const categoriaNome = button.textContent.trim();
            
            tituloCategoria.textContent = categoriaNome;
            
            // CHAMA A FUNÇÃO RÁPIDA (que lê da gaveta)
            renderizarProdutos(categoriaId);
          });
        });
        
        // Carrega os produtos da primeira categoria
        if (categorias.length > 0) {
          tituloCategoria.textContent = categorias[0].nome;
          renderizarProdutos(categorias[0].id); // Chama a função rápida
        } else {
          console.warn("Nenhuma categoria encontrada.");
          tituloCategoria.textContent = "Sem produtos";
          menuGrid.innerHTML = "<p>Nenhuma categoria cadastrada.</p>";
        }
      }
      
      carregarDadosIniciais();

});