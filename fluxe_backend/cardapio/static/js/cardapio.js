document.addEventListener("DOMContentLoaded", () => {
    
    // Cache de dados
    let todosOsProdutos = [];
    let todasCategorias = [];

    // URLs da API
    const API_CATEGORIAS = '/api/categorias/';
    const API_PRODUTOS = '/api/produtos/';
    const API_POPULARES = '/api/populares/';

    // Elementos da tela
    const containerCardapio = document.getElementById('cardapio-completo'); 
    const inputBusca = document.querySelector('.search input'); 

    // --- ELEMENTOS DO MENU LATERAL ---
    const btnAbrir = document.getElementById('btn-menu-abrir');
    const btnFechar = document.getElementById('btn-menu-fechar');
    const overlay = document.getElementById('menu-overlay');
    const sidebar = document.getElementById('sidebar');
    const sidebarCategorias = document.getElementById('sidebar-categorias-container');
    const linkQueridinhosSidebar = document.getElementById('link-queridinhos-sidebar');

    // --- FUNÇÕES DE CONTROLE DO MENU ---
    function abrirMenu() { document.body.classList.add('menu-open', 'body-no-scroll'); }
    function fecharMenu() { document.body.classList.remove('menu-open', 'body-no-scroll'); }

    if(btnAbrir) btnAbrir.addEventListener('click', abrirMenu);
    if(btnFechar) btnFechar.addEventListener('click', fecharMenu);
    if(overlay) overlay.addEventListener('click', fecharMenu);

    // formatação do "." pra "," no valor decimal
    function formatarMoeda(valor) {
        return parseFloat(valor).toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    // --- NOVA FUNÇÃO AJAX (ADICIONAR RAPIDINHO) ---
    // Fica aqui, logo depois das funções básicas e antes de renderizar
    async function adicionarRapidinho(event, produtoId) {
        // 1. Para tudo! Não deixa o link carregar a página
        event.preventDefault();
        event.stopPropagation(); // Não abre os detalhes do card

        const btn = event.currentTarget; // O botão que foi clicado
        
        // Efeito visual simples (botão dá uma encolhidinha)
        btn.style.transform = "scale(0.9)";
        setTimeout(() => btn.style.transform = "scale(1)", 150);

        try {
            // 2. Chama o Django no sigilo
            const response = await fetch(`/carrinho/add/${produtoId}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Senha pro Django saber q é AJAX
                }
            });

            if (response.ok) {
                const data = await response.json();
                
                // 3. Atualiza a bolinha vermelha lá em cima
                const badge = document.querySelector('.badge-cart');
                if (badge) {
                    badge.textContent = data.qtd;
                    // Efeitinho de "pulo" na bolinha
                    badge.style.transform = "scale(1.5)";
                    setTimeout(() => badge.style.transform = "scale(1)", 200);
                }
            }
        } catch (error) {
            console.error('Erro ao adicionar:', error);
        }
    }
    // IMPORTANTE: Isso aqui libera a função pra ser usada no HTML
    window.adicionarRapidinho = adicionarRapidinho;


    // --- LÓGICA DE RENDERIZAR TUDO (SCROLL INFINITO) ---

    function renderizarTudo(termoBusca = '') {
        if (!containerCardapio) return;
        containerCardapio.innerHTML = ''; // Limpa tudo pra reconstruir

        let encontrouAlgumProduto = false;
        termoBusca = termoBusca.toLowerCase();

        // Para cada categoria, cria um bloco visual
        todasCategorias.forEach(cat => {
            // Filtra os produtos dessa categoria
            const produtosDaCategoria = todosOsProdutos.filter(p => String(p.categoria) === String(cat.id));

            // Se tem busca, filtra mais ainda
            const produtosVisiveis = produtosDaCategoria.filter(p => 
                p.nome.toLowerCase().includes(termoBusca) || 
                (p.descricao && p.descricao.toLowerCase().includes(termoBusca))
            );

            // Se não sobrou nenhum produto nessa categoria, pula ela
            if (produtosVisiveis.length === 0) return;

            encontrouAlgumProduto = true;

            // Cria o HTML do Título da Categoria e dos Cards
            const secaoHTML = `
                <div id="cat-${cat.id}" class="categoria-wrapper" style="scroll-margin-top: 140px;"> 
                    <h2 class="section-title">${cat.nome}</h2>
                    <section class="menu-grid">
                        ${produtosVisiveis.map(produto => `
                            <article class="card" onclick="window.location.href='/detalhes/${produto.id}/'" style="cursor: pointer;">
                                
                                <img class="thumb" src="${produto.foto_url}" alt="${produto.nome}" onerror="this.src='/static/imagens/xequemate.webp'">
                                
                                <div class="meta">
                                    <div class="name">${produto.nome}</div>
                                    <div class="desc">${produto.descricao || ''}</div>
                                    <div class="price">R$ ${formatarMoeda(produto.preco_atual)}</div>
                                </div>

                                <button class="add" aria-label="Add ${produto.nome}" onclick="adicionarRapidinho(event, '${produto.id}')">
                                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                                        <path d="M12 5v14M5 12h14" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
                                    </svg>
                                </button>

                            </article>
                        `).join('')}
                    </section>
                </div>
            `;
            
            containerCardapio.insertAdjacentHTML('beforeend', secaoHTML);
        });

        // Se digitou algo que não existe em lugar nenhum
        if (!encontrouAlgumProduto) {
            containerCardapio.innerHTML = `
                <div style="text-align:center; padding: 40px; color:#666;">
                    <p>Nenhum produto encontrado para "<strong>${inputBusca.value}</strong>".</p>
                </div>
            `;
        }
    }

    // Função de Rolagem Suave
    function rolarParaCategoria(categoriaId) {
        const elemento = document.getElementById(`cat-${categoriaId}`);
        if (elemento) {
            elemento.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    // Função Principal (Busca API)
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

            // 1. Renderiza os Populares (Queridinhos)
            const containerPopulares = document.querySelector('.hscroll');
            if (containerPopulares) {
                containerPopulares.innerHTML = '';
                if (produtosPopulares.length === 0) {
                    containerPopulares.innerHTML = '<p style="padding:10px; color:#999; font-size:14px;">Sem destaques hoje.</p>';
                } else {
                    produtosPopulares.forEach(prod => {
                        const html = `
                        <article class="popular-card" onclick="window.location.href='/detalhes/${prod.id}/'">
                            <img src="${prod.foto_url}" alt="${prod.nome}" onerror="this.src='/static/imagens/xequemate.webp'">
                            <div class="popular-info">
                                <div class="popular-title">${prod.nome}</div>
                                <div class="popular-price">R$ ${formatarMoeda(prod.preco_atual)}</div>
                            </div>
                        </article>
                        `;
                        containerPopulares.insertAdjacentHTML('beforeend', html);
                    });
                }
            }

            // 2. Renderiza o Cardápio Completo
            renderizarTudo();

            // 3. Prepara as Abas
            const tabsContainer = document.querySelector('.tabs');
            
            if (tabsContainer) tabsContainer.innerHTML = ''; 
            if (sidebarCategorias) sidebarCategorias.innerHTML = '';

            if (todasCategorias.length > 0) {
                todasCategorias.forEach((cat, index) => {
                    // --- A. Aba Superior (Tabs) ---
                    const btn = document.createElement('button');
                    btn.className = `tab ${index === 0 ? 'active' : ''}`; 
                    btn.textContent = cat.nome;
                    
                    btn.addEventListener('click', () => {
                        if(inputBusca.value !== '') {
                            inputBusca.value = '';
                            renderizarTudo(); 
                        }
                        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                        btn.classList.add('active');
                        rolarParaCategoria(cat.id);
                    });

                    if (tabsContainer) tabsContainer.appendChild(btn);

                    // --- B. Menu Lateral ---
                    if (sidebarCategorias) {
                        const linkMenu = document.createElement('a');
                        linkMenu.href = '#';
                        linkMenu.className = 'sidebar-link';
                        linkMenu.textContent = cat.nome;
                        linkMenu.addEventListener('click', (e) => {
                            e.preventDefault();
                            fecharMenu();
                            
                            if(inputBusca.value !== '') {
                                inputBusca.value = '';
                                renderizarTudo(); 
                            }
                            rolarParaCategoria(cat.id);
                        });
                        sidebarCategorias.appendChild(linkMenu);
                    }
                });
            }

            // Link "Os Queridinhos" no Sidebar
            if (linkQueridinhosSidebar) {
                linkQueridinhosSidebar.addEventListener('click', (e) => {
                    e.preventDefault();
                    fecharMenu();
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                });
            }

            // 4. Busca em Tempo Real 
            if (inputBusca) {
                inputBusca.addEventListener('input', (e) => {
                    const termo = e.target.value;
                    renderizarTudo(termo); 
                });
            }

        } catch (error) {
            console.error("Erro ao carregar API:", error);
        }
    }

    carregarDados();
});