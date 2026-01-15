// =============================
// ingresos.js
// Script para mostrar y añadir ingresos en el panel
// =============================

// Botón que muestra u oculta el formulario de ingresos
const btn = document.getElementById('btnIngreso');

// Formulario donde se introducen los datos del ingreso
const form = document.getElementById('formIngreso');

// Botón para guardar el ingreso
const guardar = document.getElementById('guardarIngreso');

// Contenedor donde se muestran los movimientos (ingresos)
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
// GUARDAR INGRESO
// =============================

guardar.onclick = function () {
  // Obtiene los valores introducidos por el usuario
  const nombre = document.getElementById('nombreIngreso').value;
  const cantidad = document.getElementById('cantidadIngreso').value;
  const fecha = document.getElementById('fechaIngreso').value;

  // Validación básica: comprueba que ningún campo esté vacío
  if (nombre === '' || cantidad === '' || fecha === '') {
    alert('Rellena todos los campos');
    return; // Detiene la ejecución si falta algún dato
  }

  // Crea un nuevo div para mostrar el ingreso
  const div = document.createElement('div');

  // Asigna clases CSS para el estilo del movimiento
  div.className = 'movimiento ingreso';

  // Inserta los datos del ingreso en el HTML
  // + € indica que es un ingreso
  div.innerHTML = `
    <span>${nombre}</span>
    <span>+ €${cantidad}</span>
    <span>${fecha}</span>
  `;

  // Añade el nuevo ingreso al inicio de la lista
  lista.prepend(div);

  // Oculta el formulario después de guardar
  form.classList.add('oculto');
};
