// Espera a que el DOM cargue
document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');

  form.addEventListener('submit', function (e) {
    e.preventDefault(); // Evitar que recargue la página

    const email = document.getElementById('usuario').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, password: password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        // Guardamos id de usuario y redirigimos al panel
        localStorage.setItem('usuario_id', data.usuario_id);
        window.location.href = '/panel';
      } else {
        alert(data.error);
      }
    })
    .catch(error => console.log('Error:', error));
  });
});
