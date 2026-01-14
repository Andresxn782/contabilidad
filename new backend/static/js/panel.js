// panel.js

var usuario_id = localStorage.getItem('usuario_id');

// si no hay usuario logueado, volver al login
if (!usuario_id) {
  window.location.href = 'login.html';
}

// Cargar datos del panel (saldo, ingresos y gastos)
fetch('http://127.0.0.1:5000/panel/' + usuario_id)
  .then(function(res) {
    return res.text(); // panel.html devuelve HTML, no JSON
  })
  .then(function(html) {
    // Como panel.html ya renderiza saldo, ingresos y gastos con Jinja2,
    // no necesitamos hacer nada más aquí
  });

// cargar historial de ingresos
fetch('http://127.0.0.1:5000/ingresos/' + usuario_id)
  .then(function(res) {
    return res.json();
  })
  .then(function(lista_ingresos) {
    var historial = document.querySelector('.historial-ingresos');
    if (!historial) return;
    historial.innerHTML = '<h2>Historial de Ingresos</h2>';

    lista_ingresos.forEach(function(ingreso) {
      var div = document.createElement('div');
      div.className = 'movimiento ingreso';
      div.innerHTML =
        '<span>' + ingreso.nombre + '</span>' +
        '<span>+ €' + parseFloat(ingreso.cantidad).toFixed(2) + '</span>' +
        '<span>' + new Date(ingreso.date).toLocaleDateString() + '</span>';
      historial.appendChild(div);
    });
  });

// cargar historial de gastos
fetch('http://127.0.0.1:5000/gastos/' + usuario_id)
  .then(function(res) {
    return res.json();
  })
  .then(function(lista_gastos) {
    var historial = document.querySelector('.historial-gastos');
    if (!historial) return;
    historial.innerHTML = '<h2>Historial de Gastos</h2>';

    lista_gastos.forEach(function(gasto) {
      var div = document.createElement('div');
      div.className = 'movimiento gasto';
      div.innerHTML =
        '<span>' + gasto.nombre + '</span>' +
        '<span>- €' + parseFloat(gasto.cantidad).toFixed(2) + '</span>' +
        '<span>' + new Date(gasto.date).toLocaleDateString() + '</span>';
      historial.appendChild(div);
    });
  });
