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
    // --- FUNCIONALIDADE: CLICAR NO LOCAL PARA VOLTAR AO TOPO ---
    const btnLocation = document.querySelector('.place'); // Pega a div do nome do bar

    if (btnLocation) {
        // Deixa o cursor como "mãozinha" pra indicar que é clicável
        btnLocation.style.cursor = 'pointer';

        btnLocation.addEventListener('click', () => {
            // 1. Rola suavemente para o topo zero
            window.scrollTo({ top: 0, behavior: 'smooth' });

            // 2. Se tiver barra de busca, foca nela automaticamente
            if (inputBusca) {
                // Pequeno delay para a rolagem começar antes de focar
                setTimeout(() => {
                    inputBusca.focus(); // Abre o teclado no celular / Põe o cursor
                    
                    // Opcional: Dá um destaque visual (piscar) na busca
                    inputBusca.parentElement.style.transform = "scale(1.05)";
                    setTimeout(() => inputBusca.parentElement.style.transform = "scale(1)", 200);
                }, 300);
            }
        });
    }

    // --- FUNÇÕES DE CONTROLE DO MENU ---
    function abrirMenu() { document.body.classList.add('menu-open', 'body-no-scroll'); }
    function fecharMenu() { document.body.classList.remove('menu-open', 'body-no-scroll'); }

    if(btnAbrir) btnAbrir.addEventListener('click', abrirMenu);
    if(btnFechar) btnFechar.addEventListener('click', fecharMenu);
    if(overlay) overlay.addEventListener('click', fecharMenu);

    // Formatação de Moeda (R$ 20,00)
    function formatarMoeda(valor) {
        return parseFloat(valor).toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    // --- FUNÇÃO PARA MOSTRAR O TOAST ---
    function mostrarToast(mensagem) {
        const toast = document.getElementById("toast-box");
        if(toast) {
            toast.textContent = mensagem; // Muda o texto
            toast.className = "toast show"; // Mostra
            
            // Esconde depois de 2.5 segundos
            setTimeout(function(){ 
                toast.className = toast.className.replace("show", ""); 
            }, 2500);
        }
    }

    // --- NOVA FUNÇÃO AJAX (ADICIONAR RAPIDINHO) ---
    async function adicionarRapidinho(event, produtoId) {
        event.preventDefault();
        event.stopPropagation(); // Não abre os detalhes do card

        const btn = event.currentTarget;
        
        // Efeito visual (click)
        btn.style.transform = "scale(0.9)";
        setTimeout(() => btn.style.transform = "scale(1)", 150);

        try {
            // Chama o Django no sigilo
            const response = await fetch(`/carrinho/add/${produtoId}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const data = await response.json();
                
                // Atualiza a bolinha vermelha
                const badge = document.querySelector('.badge-cart');
                if (badge) {
                    badge.textContent = data.qtd;
                    badge.style.transform = "scale(1.5)";
                    setTimeout(() => badge.style.transform = "scale(1)", 200);
                }
                
                // Chama o aviso Toast
                mostrarToast("Item adicionado com sucesso! ✅"); 
            }
        } catch (error) {
            console.error('Erro ao adicionar:', error);
        }
    }
    // Libera a função para o HTML usar no onclick
    window.adicionarRapidinho = adicionarRapidinho;


    // --- LÓGICA DE RENDERIZAR TUDO (LISTAGEM DOS PRODUTOS) ---
    function renderizarTudo(termoBusca = '') {
        if (!containerCardapio) return;
        containerCardapio.innerHTML = ''; 

        let encontrouAlgumProduto = false;
        termoBusca = termoBusca.toLowerCase();

        // Para cada categoria, cria um bloco visual
        todasCategorias.forEach(cat => {
            // Filtra os produtos dessa categoria
            const produtosDaCategoria = todosOsProdutos.filter(p => String(p.categoria) === String(cat.id));

            // Filtra pela busca (se houver)
            const produtosVisiveis = produtosDaCategoria.filter(p => 
                p.nome.toLowerCase().includes(termoBusca) || 
                (p.descricao && p.descricao.toLowerCase().includes(termoBusca))
            );

            // Se não tiver produtos visíveis, não desenha essa categoria
            if (produtosVisiveis.length === 0) return;

            encontrouAlgumProduto = true;

            // HTML da Seção (Título + Grid de Cards)
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

        // Feedback de "Não encontrado"
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

    // --- FUNÇÃO PRINCIPAL (CARREGAR DADOS + ABAS) ---
    async function carregarDados() {
        try {
            console.log("🚀 Iniciando busca de dados...");
            
            const [resCat, resProd, resPop] = await Promise.all([
                fetch(API_CATEGORIAS),
                fetch(API_PRODUTOS),
                fetch(API_POPULARES)
            ]);

            // Carrega TUDO
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

            // 2. Renderiza o Cardápio (Produtos)
            renderizarTudo();

            // 3. Monta as Abas (Tabs) - VERIFICANDO SE A CATEGORIA TEM PRODUTO
            const tabsContainer = document.querySelector('.tabs');
            
            if (tabsContainer) tabsContainer.innerHTML = ''; 
            if (sidebarCategorias) sidebarCategorias.innerHTML = '';

            if (todasCategorias.length > 0) {
                let primeiraCategoriaAtiva = false; // Controle para ativar a primeira aba válida

                todasCategorias.forEach((cat) => {
                    
                    // 🔍 CHECK: Essa categoria tem produto?
                    const temProduto = todosOsProdutos.some(p => String(p.categoria) === String(cat.id));
                    
                    // Se não tiver produto, PULA (Não cria aba, nem link no menu)
                    if (!temProduto) return;

                    // --- A. Aba Superior ---
                    const btn = document.createElement('button');
                    
                    if (!primeiraCategoriaAtiva) {
                        btn.className = 'tab active';
                        primeiraCategoriaAtiva = true;
                    } else {
                        btn.className = 'tab';
                    }

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

            // 4. Ativa a Busca
            if (inputBusca) {
                inputBusca.addEventListener('input', (e) => {
                    const termo = e.target.value;
                    renderizarTudo(termo); 
                });
            }

        } catch (error) {
            console.error("❌ Erro fatal no JS:", error);
        }
    }

    carregarDados();
});