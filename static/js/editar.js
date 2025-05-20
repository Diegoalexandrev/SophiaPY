document.getElementById("form-editar").addEventListener("submit", function (e) {
  e.preventDefault();

  const campoBusca = document.getElementById("busca");

  if (!campoBusca.checkValidity()) {
    campoBusca.reportValidity();
    return;
  }

  alert(
    "Editando livro:\n" + JSON.stringify({ busca: campoBusca.value }, null, 2)
  );

  e.target.reset();
});
