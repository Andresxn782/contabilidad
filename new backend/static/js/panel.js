// =============================
// panel.js
// Script encargado de gestionar el panel del usuario
// =============================

// Obtiene el usuario_id guardado en el navegador (localStorage)
// Este valor normalmente se guarda al hacer login correctamente
var usuario_id = localStorage.getItem('usuario_id');

// Si no existe un usuario_id, significa que el usuario no está logueado
// En ese caso, se redirige automáticamente a la página de login
if (!usuario_id) {
  window.location.href = 'login.html';
}

// =============================
// CARGA DE DATOS GENERALES DEL PANEL
// =============================

// Hace una petición al backend para cargar el panel del usuario
// Se pasa el usuario_id en la URL
fetch('http://127.0.0.1:5000/panel/' + usuario_id)
  .then(function (res) {
    // El endpoint devuelve HTML renderizado con Jinja2, no JSON
    return res.text();
  })
  .then(function (html) {
    // No se hace nada con el HTML porque el servidor ya
    // renderiza saldo, ingresos y gastos directamente
    // El simple acceso a esta ruta valida la sesión del usuario
  });

// =============================
// HISTORIAL DE INGRESOS
// =============================

// Petición al backend para obtener los ingresos del usuario
fetch('http://127.0.0.1:5000/ingresos/' + usuario_id)
  .then(function (res) {
    // La respuesta se convierte a JSON
    return res.json();
  })
  .then(function (lista_ingresos) {
    // Selecciona el contenedor del historial de ingresos
    var historial = document.querySelector('.historial-ingresos');

    // Si el contenedor no existe, se detiene la ejecución
    if (!historial) return;

    // Inserta el título del historial
    historial.innerHTML = '<h2>Historial de Ingresos</h2>';

    // Recorre cada ingreso recibido del backend
    lista_ingresos.forEach(function (ingreso) {
      // Crea un div para cada movimiento
      var div = document.createElement('div');

      // Asigna clases CSS para estilos
      div.className = 'movimiento ingreso';

      // Inserta la información del ingreso
      // nombre → concepto del ingreso
      // cantidad → se formatea a 2 decimales
      // date → se convierte a fecha legible
      div.innerHTML =
        '<span>' +
        ingreso.nombre +
        '</span>' +
        '<span>+ €' +
        parseFloat(ingreso.cantidad).toFixed(2) +
        '</span>' +
        '<span>' +
        new Date(ingreso.date).toLocaleDateString() +
        '</span>';

      // Añade el ingreso al historial
      historial.appendChild(div);
    });
  });

// =============================
// HISTORIAL DE GASTOS
// =============================

// Petición al backend para obtener los gastos del usuario
fetch('http://127.0.0.1:5000/gastos/' + usuario_id)
  .then(function (res) {
    // Convierte la respuesta a JSON
    return res.json();
  })
  .then(function (lista_gastos) {
    // Selecciona el contenedor del historial de gastos
    var historial = document.querySelector('.historial-gastos');

    // Si el contenedor no existe, se detiene la ejecución
    if (!historial) return;

    // Inserta el título del historial
    historial.innerHTML = '<h2>Historial de Gastos</h2>';

    // Recorre cada gasto recibido
    lista_gastos.forEach(function (gasto) {
      // Crea un div para el gasto
      var div = document.createElement('div');

      // Asigna clases CSS
      div.className = 'movimiento gasto';

      // Inserta la información del gasto
      div.innerHTML =
        '<span>' +
        gasto.nombre +
        '</span>' +
        '<span>- €' +
        parseFloat(gasto.cantidad).toFixed(2) +
        '</span>' +
        '<span>' +
        new Date(gasto.date).toLocaleDateString() +
        '</span>';

      // Añade el gasto al historial
      historial.appendChild(div);
    });
  });
