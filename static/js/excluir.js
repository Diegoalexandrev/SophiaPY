document
  .getElementById("form-excluir")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const busca = document.getElementById("titulo").value;

    if (!busca.trim()) {
      alert("Por favor, preencha o campo de exclusão.");
      return;
    }

    const confirmar = confirm(`Deseja realmente excluir o livro: "${busca}"?`);

    if (confirmar) {
      alert("Livro excluído:\n" + JSON.stringify({ titulo: busca }, null, 2));
      e.target.reset();
    } else {
      alert("Exclusão cancelada.");
    }
  });
