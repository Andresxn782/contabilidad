// =============================
// gastos.js
// Script para mostrar y añadir gastos en el panel
// =============================

// Botón que muestra u oculta el formulario de gastos
const btn = document.getElementById('btnGasto');

// Formulario donde se introducen los datos del gasto
const form = document.getElementById('formGasto');

// Botón para guardar el gasto
const guardar = document.getElementById('guardarGasto');

// Contenedor donde se muestran los movimientos (gastos)
const lista = document.querySelector('.lista-movimientos');

// =============================
// MOSTRAR / OCULTAR FORMULARIO
// =============================

// Al hacer click en el botón, se alterna la clase "oculto"
// Si el formulario está visible se oculta, y viceversa
btn.onclick = function () {
  form.classList.toggle('oculto');
};

// =============================
// GUARDAR GASTO
// =============================

guardar.onclick = function () {
  // Obtiene los valores introducidos por el usuario
  const nombre = document.getElementById('nombreGasto').value;
  const cantidad = document.getElementById('cantidadGasto').value;
  const fecha = document.getElementById('fechaGasto').value;

  // Validación básica: comprueba que ningún campo esté vacío
  if (nombre === '' || cantidad === '' || fecha === '') {
    alert('Rellena todos los campos');
    return; // Detiene la ejecución si falta algún dato
  }

  // Crea un nuevo div para mostrar el gasto
  const div = document.createElement('div');

  // Asigna clases CSS para el estilo del movimiento
  div.className = 'movimiento gasto';

  // Inserta los datos del gasto en el HTML
  // - € indica que es un gasto
  div.innerHTML = `
    <span>${nombre}</span>
    <span>- €${cantidad}</span>
    <span>${fecha}</span>
  `;

  // Añade el nuevo gasto al inicio de la lista
  lista.prepend(div);

  // Oculta el formulario después de guardar
  form.classList.add('oculto');
};
