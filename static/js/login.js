document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('#form-login');
  const matriculaInput = document.querySelector('input[name="matricula"]');
  const senhaInput = document.querySelector('input[name="senha"]');
  const mensagemErro = document.querySelector('#mensagem-erro');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const dados = {
      matricula: matriculaInput.value.trim(),
      senha: senhaInput.value.trim()
    };

    try {
      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
      });

      const result = await response.json();
      console.log(result);

      if (!response.ok) {
        mensagemErro.textContent = result.erro || 'Erro no login';
        mensagemErro.style.display = 'block';
        return;
      }

      mensagemErro.style.display = 'none';
      //alert('Login realizado com sucesso!');

      // Salva o token no cookie
      document.cookie = `token=${result.token}; path=/; max-age=86400`;

      // redireciona
      window.location.href = "/index";

    } catch (error) {
      mensagemErro.textContent = 'Erro de conexão com o servidor.';
      mensagemErro.style.display = 'block';
    }
  });
});
