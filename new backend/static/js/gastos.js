const btn = document.getElementById("btnGasto");
const form = document.getElementById("formGasto");
const guardar = document.getElementById("guardarGasto");
const lista = document.querySelector(".lista-movimientos");

btn.onclick = function () {
  form.classList.toggle("oculto");
};

guardar.onclick = function () {
  const nombre = document.getElementById("nombreGasto").value;
  const cantidad = document.getElementById("cantidadGasto").value;
  const fecha = document.getElementById("fechaGasto").value;

  if (nombre === "" || cantidad === "" || fecha === "") {
    alert("Rellena todos los campos");
    return;
  }

  const div = document.createElement("div");
  div.className = "movimiento gasto";
  div.innerHTML = `
    <span>${nombre}</span>
    <span>- €${cantidad}</span>
    <span>${fecha}</span>
  `;

  lista.prepend(div);
  form.classList.add("oculto");
};
