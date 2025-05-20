document.querySelector("form").addEventListener("submit", function (e) {
  e.preventDefault();

  const titulo = document.getElementById("titulo").value;
  const autor = document.getElementById("autor").value;
  const ano = document.getElementById("ano").value;
  const categoria = document.getElementById("categoria").value;

  const livro = {
    titulo,
    autor,
    ano,
    categoria,
  };

  alert("Livro cadastrado:\n" + JSON.stringify(livro, null, 2));

  e.target.reset();
});
