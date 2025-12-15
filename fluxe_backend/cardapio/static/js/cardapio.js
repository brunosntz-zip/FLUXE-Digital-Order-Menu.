document.addEventListener("DOMContentLoaded", () => {
    
    let todosOsProdutos = [];
    let todasCategorias = [];

    // URL da API local do Django
    const API_CATEGORIAS = '/api/categorias/';
    const API_PRODUTOS = '/api/produtos/';

    // Função para desenhar os produtos na tela
    function renderizarProdutos(categoriaId) {
        console.log(`Renderizando categoria: ${categoriaId}`);

        const menuGrid = document.querySelector('.menu-grid');
        const tituloCategoria = document.querySelector('#titulo-categoria');
        
        if (!menuGrid) return;

        const produtosFiltrados = todosOsProdutos.filter(p => p.categoria == categoriaId);

        // Atualiza o título da seção
        const cat = todasCategorias.find(c => c.id == categoriaId);
        if (cat) tituloCategoria.textContent = cat.nome;

        menuGrid.innerHTML = ''; // Limpa a tela

        if (produtosFiltrados.length === 0) {
            menuGrid.innerHTML = '<p class="muted">Nenhum produto nesta categoria.</p>';
            return;
        }

        // Desenha os cards
        produtosFiltrados.forEach(produto => {
            const cardHTML = `
            <article class="card">
                <img class="thumb" src="${produto.foto_url}" alt="${produto.nome}" onerror="this.src='/static/imagens/xequemate.webp'">
                <div class="meta">
                <div class="name">${produto.nome}</div>
                <div class="desc">${produto.descricao || ''}</div>
                <div class="price">R$ ${produto.preco_atual}</div>
                </div>
                
                <a href="/carrinho/add/${produto.id}/" class="add" aria-label="Add ${produto.nome}">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                    <path d="M12 5v14M5 12h14" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
                </svg>
                </a>
            </article>
            `;
            menuGrid.insertAdjacentHTML('beforeend', cardHTML);
        });
    }

    async function carregarDados() {
        try {
            console.log("Buscando dados do Django...");
            
            const [resCat, resProd] = await Promise.all([
                fetch(API_CATEGORIAS),
                fetch(API_PRODUTOS)
            ]);

            todasCategorias = await resCat.json();
            todosOsProdutos = await resProd.json();

            console.log("Categorias:", todasCategorias);
            console.log("Produtos:", todosOsProdutos);

            const tabsContainer = document.querySelector('.tabs');
            if (tabsContainer && todasCategorias.length > 0) {
                tabsContainer.innerHTML = ''; // Limpa abas antigas

                todasCategorias.forEach((cat, index) => {
                    const btn = document.createElement('button');
                    btn.className = `tab ${index === 0 ? 'active' : ''}`; // Primeiro já vem ativo
                    btn.textContent = cat.nome;
                    
                    btn.addEventListener('click', () => {
                        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                        btn.classList.add('active');
                        renderizarProdutos(cat.id);
                    });

                    tabsContainer.appendChild(btn);
                });

                renderizarProdutos(todasCategorias[0].id);
            }

        } catch (error) {
            console.error("Erro ao carregar API:", error);
            const menuGrid = document.querySelector('.menu-grid');
            if(menuGrid) menuGrid.innerHTML = '<p style="color:red">Erro ao carregar cardápio. Verifique o console.</p>';
        }
    }

    carregarDados();
});