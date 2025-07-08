 document.getElementById('preferencesForm').addEventListener('submit', function (e) {
      e.preventDefault();
      let isValid = true;

      document.getElementById('nameError').textContent = '';
      document.getElementById('ageError').textContent = '';
      document.getElementById('preferenceError').textContent = '';
      document.getElementById('genresError').textContent = '';

      const name = document.getElementById('name').value.trim();
      const age = document.getElementById('age').value.trim();
      const preference = document.getElementById('preference').value.trim();
      const genres = document.getElementById('genres').value.trim();

      if (!name) {
        document.getElementById('nameError').textContent = 'Por favor, preencha seu nome.';
        isValid = false;
      }

      if (!age || age < 1 || age > 120) {
        document.getElementById('ageError').textContent = 'Por favor, informe uma idade válida.';
        isValid = false;
      }

      if (!preference) {
        document.getElementById('preferenceError').textContent = 'Por favor, selecione uma preferência.';
        isValid = false;
      }

      if (!genres) {
        document.getElementById('genresError').textContent = 'Por favor, informe seus gêneros favoritos.';
        isValid = false;
      }

      if (isValid) {
        let preferenciaTraduzida = '';
        switch (preference) {
          case 'book': preferenciaTraduzida = 'livros'; break;
          case 'film': preferenciaTraduzida = 'filmes'; break;
          case 'both': preferenciaTraduzida = 'ambos'; break;
        }

        const formData = {
          nome: name,
          idade: age,
          preferencia: preferenciaTraduzida,
          generos: genres,
        };

        const jsonData = JSON.stringify(formData, null, 2);
        const blob = new Blob([jsonData], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const airplane = document.getElementById('airplane');
        airplane.classList.remove('hidden');
        airplane.classList.add('animate-fly-across');

        const a = document.createElement('a');
        a.href = url;
        a.download = 'preferencias.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        setTimeout(() => {
          alert('Obrigado! Suas preferências foram salvas como arquivo JSON.');
          document.getElementById('preferencesForm').reset();
          document.getElementById('btnText').innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
              <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
            </svg>
            Enviar Preferências
          `;
          airplane.classList.add('hidden');
          airplane.classList.remove('animate-fly-across');
        }, 1400);
      }
    });