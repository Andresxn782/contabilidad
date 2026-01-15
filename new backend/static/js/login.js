// Espera a que todo el HTML esté completamente cargado antes de ejecutar el código
// Esto evita errores por intentar acceder a elementos que aún no existen
document.addEventListener('DOMContentLoaded', function () {
  // Selecciona el primer formulario (<form>) que encuentre en el documento
  const form = document.querySelector('form');

  // Si no existe ningún formulario, se detiene la ejecución del script
  if (!form) return;

  // Añade un listener al evento "submit" del formulario
  form.addEventListener('submit', function (e) {
    // Previene el comportamiento por defecto del formulario
    // (evita que la página se recargue automáticamente)
    e.preventDefault();

    // Obtiene el valor del input con id "email"
    const email = document.getElementById('email').value;

    // Obtiene el valor del input con id "password"
    const password = document.getElementById('password').value;

    // Realiza una petición HTTP al servidor usando fetch
    fetch('/', {
      // Método POST para enviar datos al servidor
      method: 'POST',

      // Indica el tipo de contenido que se envía
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },

      // Convierte los datos en formato URL encoded (email=...&password=...)
      body: new URLSearchParams({
        email: email,
        password: password,
      }),
    })
      // Maneja la respuesta del servidor
      .then((res) =>
        // Si el servidor responde con una redirección
        // se cambia la URL del navegador a la nueva dirección
        res.redirected ? (window.location.href = res.url) : res.text()
      )
      // Captura y muestra errores en la consola
      .catch((err) => console.log(err));
  });
});
