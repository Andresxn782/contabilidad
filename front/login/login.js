// login.js

document.querySelector('form').addEventListener('submit', function (e) {
  e.preventDefault(); // evitar que recargue la página

  var email = document.getElementById('usuario').value;
  var password = document.getElementById('password').value;

  fetch('http://127.0.0.1:5000/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email, password: password }),
  })
    .then(function (res) {
      return res.json();
    })
    .then(function (data) {
      if (data.usuario_id) {
        // login correcto
        localStorage.setItem('usuario_id', data.usuario_id);
        window.location.href = 'index.html'; // página principal
      } else {
        alert(data.error || 'Usuario o contraseña incorrectos');
      }
    })
    .catch(function (error) {
      console.log('Error:', error);
    });
});
