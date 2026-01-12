// principal.js

var usuario_id = localStorage.getItem('usuario_id');

// si no hay usuario logueado, volver al login
if (!usuario_id) {
  window.location.href = 'login.html';
}

// cargar dashboard
fetch('http://127.0.0.1:5000/dashboard/' + usuario_id)
  .then(function (res) {
    return res.json();
  })
  .then(function (data) {
    document.querySelector('.saldo-card .amount').textContent = '€ ' + data.saldo.toFixed(2);
    document.querySelector('.resumen .ingresos').textContent = '+ € ' + data.ingresos.toFixed(2);
    document.querySelector('.resumen .gastos').textContent = '- € ' + data.gastos.toFixed(2);
  });

// cargar historial de ingresos
fetch('http://127.0.0.1:5000/ingresos/' + usuario_id)
  .then(function (res) {
    return res.json();
  })
  .then(function (ingresos) {
    var historial = document.querySelector('.historial');
    historial.innerHTML = '<h2>Historial de movimientos</h2>';

    ingresos.forEach(function (ingreso) {
      var div = document.createElement('div');
      div.className = 'movimiento ingreso';
      div.innerHTML =
        '<span>' +
        ingreso.nombre +
        '</span>' +
        '<span>+ €' +
        ingreso.cantidad.toFixed(2) +
        '</span>' +
        '<span>' +
        new Date(ingreso.date).toLocaleDateString() +
        '</span>';
      historial.appendChild(div);
    });
  });

// cargar historial de gastos
fetch('http://127.0.0.1:5000/gastos/' + usuario_id)
  .then(function (res) {
    return res.json();
  })
  .then(function (gastos) {
    var historial = document.querySelector('.historial');

    gastos.forEach(function (gasto) {
      var div = document.createElement('div');
      div.className = 'movimiento gasto';
      div.innerHTML =
        '<span>' +
        gasto.nombre +
        '</span>' +
        '<span>- €' +
        gasto.cantidad.toFixed(2) +
        '</span>' +
        '<span>' +
        new Date(gasto.date).toLocaleDateString() +
        '</span>';
      historial.appendChild(div);
    });
  });
