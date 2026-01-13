const btn = document.getElementById("btnIngreso");
const form = document.getElementById("formIngreso");
const guardar = document.getElementById("guardarIngreso");
const lista = document.querySelector(".lista-movimientos");

btn.onclick = function () {
  form.classList.toggle("oculto");
};

guardar.onclick = function () {
  const nombre = document.getElementById("nombreIngreso").value;
  const cantidad = document.getElementById("cantidadIngreso").value;
  const fecha = document.getElementById("fechaIngreso").value;

  if (nombre === "" || cantidad === "" || fecha === "") {
    alert("Rellena todos los campos");
    return;
  }

  const div = document.createElement("div");
  div.className = "movimiento ingreso";
  div.innerHTML = `
    <span>${nombre}</span>
    <span>+ €${cantidad}</span>
    <span>${fecha}</span>
  `;

  lista.prepend(div);
  form.classList.add("oculto");
};
