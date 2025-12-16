document.addEventListener("DOMContentLoaded", () => {
    
    // Cache de dados
    let todosOsProdutos = [];
    let todasCategorias = [];

    // URLs da API
    const API_CATEGORIAS = '/api/categorias/';
    const API_PRODUTOS = '/api/produtos/';
    const API_POPULARES = '/api/populares/';

    // Elementos da tela
    const menuGrid = document.querySelector('.menu-grid');
    const tituloCategoria = document.querySelector('#titulo-categoria');
    const inputBusca = document.querySelector('.search input'); 

    // --- ELEMENTOS DO MENU LATERAL (NOVO) ---
    const btnAbrir = document.getElementById('btn-menu-abrir');
    const btnFechar = document.getElementById('btn-menu-fechar');
    const overlay = document.getElementById('menu-overlay');
    const sidebar = document.getElementById('sidebar');
    const sidebarCategorias = document.getElementById('sidebar-categorias-container');
    const linkQueridinhosSidebar = document.getElementById('link-queridinhos-sidebar');

    // --- FUNÇÕES DE CONTROLE DO MENU (NOVO) ---
    function abrirMenu() {
        document.body.classList.add('menu-open', 'body-no-scroll');
    }

    function fecharMenu() {
        document.body.classList.remove('menu-open', 'body-no-scroll');
    }

    // Eventos do Menu
    if(btnAbrir) btnAbrir.addEventListener('click', abrirMenu);
    if(btnFechar) btnFechar.addEventListener('click', fecharMenu);
    if(overlay) overlay.addEventListener('click', fecharMenu);

    // --- LÓGICA DE RENDERIZAÇÃO ---

    function renderizarLista(listaDeProdutos, titulo = null) {
        if (!menuGrid) return;
        menuGrid.innerHTML = ''; 

        if (titulo) tituloCategoria.textContent = titulo;

        if (listaDeProdutos.length === 0) {
            menuGrid.innerHTML = '<p class="muted" style="padding:10px; text-align:center;">Nenhum produto encontrado.</p>';
            return;
        }

        listaDeProdutos.forEach(produto => {
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

    function carregarCategoriaEspecifica(categoriaId) {
        const produtosFiltrados = todosOsProdutos.filter(p => String(p.categoria) === String(categoriaId));
        const cat = todasCategorias.find(c => String(c.id) === String(categoriaId));
        const nomeTitulo = cat ? cat.nome : 'Produtos';
        renderizarLista(produtosFiltrados, nomeTitulo);
    }

    // Função Principal
    async function carregarDados() {
        try {
            console.log("Buscando dados do Django...");
            
            const [resCat, resProd, resPop] = await Promise.all([
                fetch(API_CATEGORIAS),
                fetch(API_PRODUTOS),
                fetch(API_POPULARES)
            ]);

            todasCategorias = await resCat.json();
            todosOsProdutos = await resProd.json();
            const produtosPopulares = await resPop.json();

            // 1. Queridinhos
            const containerPopulares = document.querySelector('.hscroll');
            if (containerPopulares) {
                containerPopulares.innerHTML = '';
                if (produtosPopulares.length === 0) {
                    containerPopulares.innerHTML = '<p style="padding:10px; color:#999; font-size:14px;">Sem destaques hoje.</p>';
                } else {
                    produtosPopulares.forEach(prod => {
                        const html = `
                        <article class="popular-card" onclick="window.location.href='/detalhes/'">
                            <img src="${prod.foto_url}" alt="${prod.nome}" onerror="this.src='/static/imagens/xequemate.webp'">
                            <div class="popular-info">
                                <div class="popular-title">${prod.nome}</div>
                                <div class="popular-price">R$ ${prod.preco_atual}</div>
                            </div>
                        </article>
                        `;
                        containerPopulares.insertAdjacentHTML('beforeend', html);
                    });
                }
            }

            // 2. Abas de Categoria e MENU LATERAL (NOVO)
            const tabsContainer = document.querySelector('.tabs');
            
            // Limpa containers
            if (tabsContainer) tabsContainer.innerHTML = ''; 
            if (sidebarCategorias) sidebarCategorias.innerHTML = '';

            if (todasCategorias.length > 0) {
                todasCategorias.forEach((cat, index) => {
                    // --- A. Cria a Aba Superior ---
                    const btn = document.createElement('button');
                    btn.className = `tab ${index === 0 ? 'active' : ''}`;
                    btn.textContent = cat.nome;
                    btn.addEventListener('click', () => {
                        if(inputBusca) inputBusca.value = '';
                        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                        btn.classList.add('active');
                        carregarCategoriaEspecifica(cat.id);
                    });
                    if (tabsContainer) tabsContainer.appendChild(btn);

                    // --- B. Cria o Link no Menu Lateral (NOVO) ---
                    if (sidebarCategorias) {
                        const linkMenu = document.createElement('a');
                        linkMenu.href = '#';
                        linkMenu.className = 'sidebar-link';
                        linkMenu.textContent = cat.nome;
                        linkMenu.addEventListener('click', (e) => {
                            e.preventDefault(); // Não recarrega a página
                            
                            // Fecha o menu
                            fecharMenu();
                            
                            // Simula o clique na aba correta
                            if(inputBusca) inputBusca.value = '';
                            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                            // Acha a aba correspondente e ativa
                            const abaCorrespondente = document.querySelectorAll('.tab')[index];
                            if(abaCorrespondente) abaCorrespondente.classList.add('active');
                            
                            // Carrega os produtos
                            carregarCategoriaEspecifica(cat.id);
                        });
                        sidebarCategorias.appendChild(linkMenu);
                    }
                });

                // Carrega primeira categoria
                carregarCategoriaEspecifica(todasCategorias[0].id);
            }

            // Link "Os Queridinhos" no Sidebar (Rola pro topo)
            if (linkQueridinhosSidebar) {
                linkQueridinhosSidebar.addEventListener('click', (e) => {
                    e.preventDefault();
                    fecharMenu();
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                });
            }

            // Busca
            if (inputBusca) {
                inputBusca.addEventListener('input', (e) => {
                    const termo = e.target.value.toLowerCase();
                    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));

                    if (termo === '') {
                        if (todasCategorias.length > 0) {
                            const primeiraAba = document.querySelector('.tab');
                            if(primeiraAba) primeiraAba.classList.add('active');
                            carregarCategoriaEspecifica(todasCategorias[0].id);
                        }
                    } else {
                        const resultados = todosOsProdutos.filter(p => 
                            p.nome.toLowerCase().includes(termo) || 
                            (p.descricao && p.descricao.toLowerCase().includes(termo))
                        );
                        renderizarLista(resultados, `Resultados para "${e.target.value}"`);
                    }
                });
            }

        } catch (error) {
            console.error("Erro ao carregar API:", error);
        }
    }

    carregarDados();
});