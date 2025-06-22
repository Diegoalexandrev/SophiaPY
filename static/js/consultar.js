let tabelaSelecionada = null;
let ultimaBusca = '';

document.addEventListener('DOMContentLoaded', () => {
  const inputBusca = document.querySelector('.search-bar input');
  const lupa = document.querySelector('.search-bar .material-icons');

  async function executarBusca() {
    const texto = document.querySelector('.search-bar input').value.trim();

    if (!tabelaSelecionada) {
      mostrarAviso("Selecione uma tabela primeiro");
      return;
    }

    if (texto === "") {
      switch (tabelaSelecionada) {
        case 'exemplares': carregarExemplares(); break;
        case 'livros': carregarLivros(); break;
        case 'usuarios': carregarUsuarios(); break;
        case 'emprestimos': carregarEmprestimos(); break;
        case 'autores': carregarAutores(); break;
        case 'reservas': carregarReservas(); break;
      }
      return;
    }

    try {
      const response = await fetch('/consultar/buscar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texto, tipo: tabelaSelecionada })
      });

      const resultados = await response.json();
      exibirResultados(resultados);

    } catch (error) {
      console.error("Erro:", error);
      mostrarAviso("Erro ao buscar");
    }
  }

  function atualizarDicaBusca() {
    const dica = document.getElementById('dica-busca');

    switch (tabelaSelecionada) {
      case 'exemplares':
        dica.innerText = 'Você pode buscar por título do livro, número de chamada ou estado do exemplar.';
        break;
      case 'livros':
        dica.innerText = 'Busque por título, autores ou categoria.';
        break;
      case 'usuarios':
        dica.innerText = 'Busque por nome, matrícula ou email.';
        break;
      case 'emprestimos':
        dica.innerText = 'Busque por título do livro ou nome do usuário.';
        break;
      case 'autores':
        dica.innerText = 'Busque por nome do autor.';
        break;
      case 'reservas':
        dica.innerText = 'Busque por título do livro ou nome do usuário.';
        break;
      default:
        dica.innerText = 'Selecione uma tabela para ver as opções de filtro.';
    }
  }

  function exibirResultados(resultados) {
    const container = document.querySelector('.cards');
    container.innerHTML = '';

    if (!resultados || resultados.length === 0) {
      container.innerHTML = '<div class="card aviso"><p>Nenhum resultado encontrado</p></div>';
      return;
    }

    resultados.forEach(item => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
            <h4>${item.livro.titulo}</h4>
            <p><strong>Código:</strong> ${item.numero_chamada}</p>
            <p><strong>Autores:</strong> ${item.livro.autores.join(', ')}</p>
            <p><strong>Ano:</strong> ${item.livro.ano}</p>
            <p><strong>Categoria:</strong> ${item.livro.categoria}</p>
            <p><strong>Status:</strong> ${item.estado}</p>
        `;
      container.appendChild(card);
    });
  }

  function exibirExemplares(exemplares) {
    const container = document.querySelector('.cards');
    container.innerHTML = '';

    if (!exemplares || exemplares.length === 0) {
      mostrarAviso('Nenhum exemplar encontrado');
      return;
    }

    exemplares.forEach(exemplar => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
            <h4>Exemplar #${exemplar.id}</h4>
            <p><strong>Título:</strong> ${exemplar.livro.titulo}</p>
            <p><strong>Autores:</strong> ${exemplar.livro.autores.join(', ')}</p>
            <p><strong>Número:</strong> ${exemplar.numero_chamada}</p>
            <p><strong>Estado:</strong> ${exemplar.estado}</p>
        `;
      container.appendChild(card);
    });
  }

  function exibirExemplares(exemplares) {
    const container = document.querySelector('.cards');
    container.innerHTML = '';

    if (exemplares.length === 0) {
      mostrarAviso('Nenhum exemplar encontrado');
      return;
    }

    exemplares.forEach(exemplar => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
            <h4>Exemplar #${exemplar.id}</h4>
            <p><strong>Título:</strong> ${exemplar.livro.titulo}</p>
            <p><strong>Autores:</strong> ${exemplar.livro.autores.join(', ')}</p>
            <p><strong>Número:</strong> ${exemplar.numero_chamada}</p>
            <p><strong>Estado:</strong> ${exemplar.estado}</p>
        `;
      container.appendChild(card);
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    executarBusca();
  });

  function exibirResultados(dados) {
    const cardsContainer = document.querySelector('.cards');
    cardsContainer.innerHTML = '';

    if (!dados || dados.length === 0) {
      mostrarAviso('Nenhum resultado encontrado');
      return;
    }

    switch (tabelaSelecionada) {
      case 'exemplares': exibirExemplares(dados); break;
      case 'livros': exibirLivros(dados); break;
      case 'usuarios': exibirUsuarios(dados); break;
      case 'emprestimos': exibirEmprestimos(dados); break;
      case 'autores': exibirAutores(dados); break;
      case 'reservas': exibirReservas(dados); break;
    }
  }

  function mostrarAviso(mensagem) {
    const cardsContainer = document.querySelector('.cards');
    cardsContainer.innerHTML = `
      <div class="card aviso">
        <h4>${mensagem}</h4>
      </div>
    `;
  }

  function exibirExemplares(dados) {
    const cardsContainer = document.querySelector('.cards');
    cardsContainer.innerHTML = '';

    dados.forEach(exemplar => {
      const card = document.createElement('div');
      card.classList.add('card');

      card.innerHTML = `
        <h4>Exemplar #${exemplar.id || 'N/A'}</h4>
        <p><strong>Título do Livro:</strong> ${exemplar.livro?.titulo || 'N/A'}</p>
        <p><strong>Autores:</strong> ${exemplar.livro?.autores?.join(', ') || 'N/A'}</p>
        <p><strong>Estado:</strong> ${exemplar.estado || 'N/A'}</p>
        <p><strong>Número de Chamada:</strong> ${exemplar.numero_chamada || 'N/A'}</p>
      `;

      cardsContainer.appendChild(card);
    });
  }

  function exibirLivros(dados) {
    const cardsContainer = document.querySelector('.cards');
    cardsContainer.innerHTML = '';

    dados.forEach(livro => {
      const card = document.createElement('div');
      card.classList.add('card');

      card.innerHTML = `
        <h4>${livro.titulo || 'Sem título'}</h4>
        <p><strong>Autores:</strong> ${livro.autores?.join(', ') || 'N/A'}</p>
        <p><strong>Ano:</strong> ${livro.ano_publicacao || 'N/A'}</p>
        <p><strong>Categoria:</strong> ${livro.categoria || 'N/A'}</p>
        <p><strong>Exemplares:</strong> ${livro.quantidade_exemplares || 0}</p>
      `;

      cardsContainer.appendChild(card);
    });
  }

  function exibirUsuarios(dados) {
    const container = document.querySelector('.cards');
    container.innerHTML = '';

    dados.forEach(usuario => {
      const card = document.createElement('div');
      card.classList.add('card');

      card.innerHTML = `
        <h3>${usuario.nome || 'Usuário sem nome'}</h3>
        <p><strong>Matrícula:</strong> ${usuario.matricula || 'N/A'}</p>
        <p><strong>Email:</strong> ${usuario.email || 'N/A'}</p>
        <p><strong>Telefone:</strong> ${usuario.telefone || 'N/A'}</p>
      `;

      container.appendChild(card);
    });
  }

  function exibirEmprestimos(dados) {
    const container = document.querySelector('.cards');
    container.innerHTML = '';

    dados.forEach(e => {
      const card = document.createElement('div');
      card.classList.add('card');
      card.innerHTML = `
      <h3>${e.livro?.titulo || 'Empréstimo sem título'}</h3>
      <p><strong>Número de Chamada:</strong> ${e.livro?.numero_chamada || 'N/A'}</p>
      <p><strong>Usuário:</strong> ${e.usuario?.nome || 'N/A'} (${e.usuario?.matricula || 'N/A'})</p>
      <p><strong>Data Empréstimo:</strong> ${e.data_emprestimo || 'N/A'}</p>
      <p><strong>Data Devolução:</strong> ${e.data_devolucao || 'Pendente'}</p>
    `;

      container.appendChild(card);
    });
  }


  function exibirAutores(dados) {
    const container = document.querySelector('.cards');
    container.innerHTML = '';

    dados.forEach(autor => {
      const card = document.createElement('div');
      card.classList.add('card');

      card.innerHTML = `<h3>${autor.nome || 'Autor sem nome'}</h3>`;
      container.appendChild(card);
    });
  }

  function exibirReservas(dados) {
    const container = document.querySelector('.cards');
    container.innerHTML = '';
    console.log(dados);

    dados.forEach(r => {
      console.log(JSON.stringify);
      const card = document.createElement('div');
      card.classList.add('card');
      card.innerHTML = `
        <h3>${r.exemplar?.livro?.titulo || r.livro?.titulo || 'Reserva sem título'}</h3>
        <p><strong>Usuário:</strong> ${r.usuario?.nome || 'N/A'} (${r.usuario?.matricula || 'N/A'})</p>
        <p><strong>Status:</strong> ${r.status || 'N/A'}</p>
      `;

      container.appendChild(card);
    });
  }

  async function carregarExemplares() {
    try {
      const response = await fetch('/consultar/exemplares');
      const data = await response.json();
      exibirExemplares(data);
    } catch (err) {
      console.error('Erro ao carregar exemplares:', err);
      mostrarAviso('Erro ao carregar exemplares');
    }
  }

  async function carregarLivros() {
    try {
      const response = await fetch('/consultar/livros');
      const data = await response.json();
      exibirLivros(data);
    } catch (error) {
      console.error('Erro ao carregar livros:', error);
      mostrarAviso('Erro ao carregar livros');
    }
  }

  async function carregarUsuarios() {
    try {
      const response = await fetch('/consultar/usuarios');
      const data = await response.json();
      exibirUsuarios(data);
    } catch (err) {
      console.error('Erro ao carregar usuários:', err);
      mostrarAviso('Erro ao carregar usuários');
    }
  }

  async function carregarEmprestimos() {
    try {
      const response = await fetch('/consultar/emprestimos');
      const data = await response.json();
      exibirEmprestimos(data);
    } catch (error) {
      console.error('Erro ao carregar empréstimos:', error);
      mostrarAviso('Erro ao carregar empréstimos');
    }
  }

  async function carregarAutores() {
    try {
      const response = await fetch('/consultar/autores');
      const data = await response.json();
      exibirAutores(data);
    } catch (err) {
      console.error('Erro ao carregar autores:', err);
      mostrarAviso('Erro ao carregar autores');
    }
  }

  async function carregarReservas() {
    try {
      const response = await fetch('/consultar/reservas');
      const data = await response.json();
      exibirReservas(data.reservas || []);
    } catch (error) {
      console.error('Erro ao carregar reservas:', error);
      mostrarAviso('Erro ao carregar reservas');
    }
  }

  lupa.addEventListener('click', executarBusca);
  inputBusca.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') executarBusca();
  });

  // Menu lateral
  document.querySelectorAll('.menu-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();

      document.querySelectorAll('.menu-link').forEach(l => l.classList.remove('active'));
      link.classList.add('active');

      tabelaSelecionada = link.getAttribute('data-tabela');
      inputBusca.value = '';


      // Mensagens de filtros 
      const mensagensFiltro = {
        exemplares: "A consulta de Exemplares pode ser feita por: título, autor, estado, numero de chamada ou ano",
        livros: "A consulta de Livros pode ser feita por: título, autor, categoria...",
        usuarios: "A consulta de Usuários pode ser feita por: nome, email, matrícula...",
        emprestimos: "A consulta de Empréstimos pode ser feita por: usuário e livro",
        autores: "A consulta de Autores pode ser feita pelo nome",
        reservas: "A consulta de Reservas pode ser feita por: usuário, livro, datas..."
      };

      const dicaBuscaDiv = document.getElementById('dica-busca');
      dicaBuscaDiv.textContent = mensagensFiltro[tabelaSelecionada] || 'Selecione uma tabela válida.';

      switch (tabelaSelecionada) {
        case 'exemplares': carregarExemplares(); break;
        case 'livros': carregarLivros(); break;
        case 'usuarios': carregarUsuarios(); break;
        case 'emprestimos': carregarEmprestimos(); break;
        case 'autores': carregarAutores(); break;
        case 'reservas': carregarReservas(); break;
      }
    });
  });

  async function carregarPilhaLivros() {
    try {
      const response = await fetch('/consultar/pilha_livros');
      const data = await response.json();

      const container = document.querySelector('.cards');
      container.innerHTML = '';

      if (!data || data.length === 0) {
        container.innerHTML = '<div class="pilha-vazia"><p>A pilha de livros está vazia.</p></div>';
        return;
      }

      data.forEach((titulo, index) => {
        const card = document.createElement('div');
        card.classList.add('pilha-card');
        card.innerHTML = `
        <h4>${index + 1}º Livro Empilhado:</h4>
        <p>${titulo}</p>
      `;
        container.appendChild(card);
      });
    } catch (error) {
      console.error('Erro ao carregar pilha de livros:', error);
    }
  }


  document.getElementById('ver-pilha').addEventListener('click', (e) => {
    e.preventDefault();
    carregarPilhaLivros();
  });



  mostrarAviso('Selecione um filtro no menu lateral para começar');
});