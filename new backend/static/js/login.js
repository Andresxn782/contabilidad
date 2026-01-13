document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();

    var email = document.getElementById('usuario').value;
    var password = document.getElementById('password').value;

    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, password: password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // Redirige al panel con el ID del usuario
            window.location.href = `/panel/${data.usuario_id}`;
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.log('Error:', error));
  });
});
