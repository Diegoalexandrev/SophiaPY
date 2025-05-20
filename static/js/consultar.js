const livros = [
  {
    titulo: "Clean Code",
    autor: "Robert C. Martin",
    ano: "2008",
    categoria: "Programação",
    disponivel: true,
    numeroAcervo: "TI001",
  },
  {
    titulo: "The Pragmatic Programmer",
    autor: "Andrew Hunt e David Thomas",
    ano: "1999",
    categoria: "Desenvolvimento de Software",
    disponivel: false,
    numeroAcervo: "TI002",
  },
  {
    titulo: "Estruturas de Dados e Algoritmos com JavaScript",
    autor: "Loiane Groner",
    ano: "2019",
    categoria: "Algoritmos",
    disponivel: true,
    numeroAcervo: "TI003",
  },
  {
    titulo: "Código Limpo",
    autor: "Robert C. Martin",
    ano: "2011",
    categoria: "Boas Práticas",
    disponivel: false,
    numeroAcervo: "TI004",
  },
  {
    titulo: "Design Patterns",
    autor: "Erich Gamma et al.",
    ano: "1994",
    categoria: "Engenharia de Software",
    disponivel: true,
    numeroAcervo: "TI005",
  },
  {
    titulo: "Python para Desenvolvedores",
    autor: "Luiz Eduardo Borges",
    ano: "2010",
    categoria: "Linguagem de Programação",
    disponivel: true,
    numeroAcervo: "TI006",
  },
  {
    titulo: "Entendendo Algoritmos",
    autor: "Aditya Bhargava",
    ano: "2016",
    categoria: "Algoritmos e Estrutura de Dados",
    disponivel: false,
    numeroAcervo: "TI007",
  },
];

function exibirLivros(lista) {
  const container = document.getElementById("lista-livros");
  container.innerHTML = ""; // limpa a lista

  lista.forEach((livro) => {
    const card = document.createElement("div");
    card.classList.add("livro-card");
    card.innerHTML = `
        <h3>${livro.titulo}</h3>
        <p><strong>Autor:</strong> ${livro.autor}</p>
        <p><strong>Ano:</strong> ${livro.ano}</p>
        <p><strong>Categoria:</strong> ${livro.categoria}</p>
        <p><strong>Nº Acervo:</strong> ${livro.numeroAcervo}</p>
        <p><strong>Disponível:</strong> ${livro.disponivel ? "Sim" : "Não"}</p>
      `;
    container.appendChild(card);
  });
}

document.getElementById("busca").addEventListener("input", function () {
  const termo = this.value.toLowerCase();
  const filtrados = livros.filter((livro) => {
    const disponibilidade = livro.disponivel ? "sim" : "não";
    return (
      livro.titulo.toLowerCase().includes(termo) ||
      livro.autor.toLowerCase().includes(termo) ||
      livro.categoria.toLowerCase().includes(termo) ||
      livro.numeroAcervo.toLowerCase().includes(termo)
    );
  });

  exibirLivros(filtrados);
});

exibirLivros(livros);
