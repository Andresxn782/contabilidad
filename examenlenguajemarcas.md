1. Explicacion del proyecto

Hemos creado el front para la aplicacion de contabilidad, que sea facil de utilizar y se vea bonito, que no tenga muchos apartados, solo los necesarios, para que asi al usuario le sea mas comodo.La aplicacion esta hecha para personas jovenes, sin muchos ingresos, para que puedan ahorrar dinero y ver sus gastos e ingresos claramente, aparte de una tabla grafica y los presupuestos que tienen previstos para el siguiente mes.

2. Moddelo de datos

├── README.md
├── app.py
├── db.sql
├── inserciones.sql
├── static
│ ├── css
│ │ ├── estadisticas.css
│ │ ├── gastos.css
│ │ ├── ingresos.css
│ │ ├── login.css
│ │ ├── panel.css
│ │ ├── perfil.css
│ │ └── presupuestos.css
│ └── js
│ ├── gastos.js
│ ├── ingresos.js
│ ├── login.js
│ └── panel.js
└── templates
├── estadisticas.html
├── gastos.html
├── ingresos.html
├── login.html
├── panel.html
├── perfil.html
└── presupuestos.html

```

Este de aqui es el modelo de datos, como se puede ver el proyecto se divide en dos carpetas para el front, static y templates, en static se añaden los css y js en sus respectivas carpetas y en templates los html, aunque por errores que me fueron apareciendo acabamos metiendo los css en los html mediente <style></style> y asi si que conseguimos que se cargaran los css.

El proyecto empieza en el login, al acceder atraves del login con tu usuario y contraseña te lleva al panel principal, y saldran varias cosas, primero la vista principal del panel donde se podra ver el sueldo actual, los ingresos, loa gastos y un historial de estos, y luego a la izquierda una sidebar con los apartados de:

-panel
-ingresos
-gastos
-presupuestos
-estadisticas
-perfil

Cada una tiene sus diferentes pestañas, por ejemplo si entras a ingresos o gastos desaparece la sidebar y tienes centrado los ingresos que has tenido y si quieres añadir algun ingreso o gastos y abajo de ingresos y de gastos un boton de volver al panel, en cambio en estaditicas se sigue manteniendo la sibebar y se muestran los graficos de tus ingresos vs tus gastos.

 Luego en cada archivo estan los enlaces dinamicos con flask:

        <a href="{{ url_for('panel', usuario_id=usuario_id) }}">🏠 Panel</a>
        <a href="{{ url_for('ingresos', usuario_id=usuario_id) }}">💰 Ingresos</a>
        <a href="{{ url_for('gastos', usuario_id=usuario_id) }}">💸 Gastos</a>
        <a href="{{ url_for('presupuestos', usuario_id=usuario_id) }}">📅 Presupuestos</a>
        <a href="{{ url_for('estadisticas', usuario_id=usuario_id) }}">📈 Estadísticas</a>
        <a href="{{ url_for('perfil', usuario_id=usuario_id) }}">👤 Perfil</a>

Con esto lo que creamos es un menu de navegacion que alga en todos los apartados menos en ingresos y gastos, que no tienen sidebar.

A continuacion vay a proceder poner el codigo y abajo su funcionamiento.

Login html:

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Login | Contabilidad</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/login.css') }}">
</head>
<body>
  <div class="login-container">
    <h1>Iniciar sesión</h1>
    {% if error %}
      <p class="error">{{ error }}</p>
    {% endif %}
    <form method="POST">
      <input type="email" id="email" name="email" placeholder="Email" required>
      <input type="password" id="password" name="password" placeholder="Contraseña" required>
      <input type="submit" value="Entrar">
    </form>
  </div>
  <script src="{{ url_for('static', filename='js/login.js') }}"></script>
</body>
</html>


En este archivo se crea la estructura de la pagina de inicio de sesion, se utiliza HTML basico junto con Jinja2 para mostrar mensajes de error si el login falla, el formulario pide el email y la contraseña y ambos campos son obligatorios gracias al atributo required el formulario envia los datos por metodo POST al backend tambien se enlaza un archivo CSS para el diseño y un archivo JavaScript para gestionar el envio del formulario sin recargar la pagina.


Login.js

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


Este archivo se encarga de gestionar el comportamiento del formulario de login espera a que todo el contenido HTML se cargue correctamente selecciona el formulario y evita que la pagina se recargue al enviarlo recoge los valores del email y la contraseña y los envia al servidor mediante fetch usando el metodo POST si el servidor responde con una redireccion el navegador cambia automaticamente de pagina y si ocurre algun error se muestra en la consola.


Login.css

/* login.css */
body, html {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  background: #f0f2f5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-container {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
  width: 300px;
  text-align: center;
}

.login-container h1 {
  margin-bottom: 20px;
}

.login-container input[type="email"],
.login-container input[type="password"] {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.login-container input[type="submit"] {
  width: 100%;
  padding: 10px;
  background: teal;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.login-container input[type="submit"]:hover {
  background: #006666;
}

.error {
  color: red;
  margin-bottom: 10px;
}


Este archivo define el diseño visual de la pagina de login se centra el formulario en la pantalla se aplica un fondo claro y una tarjeta blanca con sombra se estilizan los inputs y el boton de envio para que sea mas claro y usable tambien se define un estilo para los mensajes de error en color rojo.

Ya hemos explicado los archivos de login, ahora vamos a por los de panel.

Panel.html


<!DOCTYPE html>
<!-- Documento HTML5 -->
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <!-- Permite mostrar correctamente acentos y caracteres especiales -->

    <title>Panel | Contabilidad</title>
    <!-- Título que aparece en la pestaña del navegador -->

    <style>
      /* Estilos generales para todo el documento */
      body,
      html {
        margin: 0; /* elimina márgenes por defecto */
        height: 100%; /* ocupa toda la altura */
        font-family: Arial, sans-serif; /* tipo de letra */
        background: #f4f6f8; /* color de fondo */
      }

      /* Layout general: divide pantalla en sidebar + contenido */
      .layout {
        display: flex; /* coloca elementos en fila */
        height: 100vh; /* altura total de la pantalla */
      }

      /* Barra lateral izquierda */
      .sidebar {
        width: 220px; /* ancho fijo */
        background: teal; /* color de fondo */
        color: white; /* texto blanco */
        padding: 20px;
        box-sizing: border-box;
      }

      /* Título del menú */
      .sidebar h2 {
        margin-top: 0;
        text-align: center;
      }

      /* Enlaces del menú */
      .sidebar a {
        display: block; /* cada enlace ocupa una línea */
        margin: 15px 0;
        color: white;
        text-decoration: none;
        font-size: 18px;
      }

      /* Efecto al pasar el ratón */
      .sidebar a:hover {
        text-decoration: underline;
      }

      /* Área de contenido principal */
      .content {
        flex: 1; /* ocupa el resto del espacio */
        padding: 30px;
      }

      /* Encabezado */
      header {
        text-align: center;
        margin-bottom: 30px;
      }

      /* Área principal */
      main {
        max-width: 800px;
        margin: auto; /* centra el contenido */
      }

      /* Tarjetas */
      .card {
        background: white;
        border-radius: 10px; /* bordes redondeados */
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* sombra */
      }

      .card h3 {
        margin-top: 0;
      }

      /* Tarjeta de saldo */
      .saldo {
        margin-bottom: 30px;
        font-size: 24px;
      }

      /* Fila que contiene ingresos y gastos */
      .cards-row {
        display: flex;
        gap: 20px; /* separación entre tarjetas */
        justify-content: center;
      }

      /* Colores de tarjetas */
      .ingreso {
        background: #e0f7e0;
        width: 250px;
      }

      .gasto {
        background: #fde0e0;
        width: 250px;
      }
    </style>
  </head>

  <body>
    <!-- Contenedor general -->
    <div class="layout">
      <!-- Barra lateral de navegación -->
      <aside class="sidebar">
        <h2>Menú</h2>

        <!--
        Enlaces generados por Flask con url_for
        usuario_id se pasa como parámetro a la ruta
      -->
        <a href="{{ url_for('ingresos', usuario_id=usuario_id) }}">💰 Ingresos</a>
        <a href="{{ url_for('gastos', usuario_id=usuario_id) }}">💸 Gastos</a>
        <a href="{{ url_for('presupuestos', usuario_id=usuario_id) }}">📅 Presupuestos</a>
        <a href="{{ url_for('estadisticas', usuario_id=usuario_id) }}">📈 Estadísticas</a>
        <a href="{{ url_for('perfil', usuario_id=usuario_id) }}">👤 Perfil</a>
      </aside>

      <!-- Contenido principal -->
      <div class="content">
        <!-- Cabecera -->
        <header>
          <h1>Panel de Control</h1>

          <!-- Muestra el ID del usuario enviado desde Flask -->
          <p>Usuario ID: {{ usuario_id }}</p>
        </header>

        <main>
          <!-- Tarjeta de saldo -->
          <div class="card saldo">
            <h3>Saldo actual</h3>
            <p>€{{ saldo }}</p>
            <!-- saldo viene desde el backend Flask -->
          </div>

          <!-- Tarjetas de ingresos y gastos -->
          <div class="cards-row">
            <div class="card ingreso">
              <h3>Ingresos</h3>
              <p>€{{ ingresos }}</p>
              <!-- ingresos viene desde Flask -->
            </div>

            <div class="card gasto">
              <h3>Gastos</h3>
              <p>€{{ gastos }}</p>
              <!-- gastos viene desde Flask -->
            </div>
          </div>
        </main>
      </div>
    </div>
  </body>
</html>


Este archivo corresponde al panel principal del usuario se divide la pantalla en una barra lateral y un area de contenido en la barra lateral aparecen los enlaces de navegacion a las distintas secciones de la aplicacion el contenido principal muestra el saldo actual los ingresos y los gastos estos datos se reciben desde el backend usando Flask y se insertan en la pagina mediante variables de Jinja2.


Panel.js


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


Este archivo controla el funcionamiento del panel primero comprueba si existe un usuario_id guardado en el navegador si no existe redirige al login despues realiza peticiones al backend para validar la sesion y obtener los ingresos y gastos del usuario los datos recibidos se recorren y se muestran dinamicamente en el historial creando elementos HTML desde JavaScript.

Ahora vamos con los archivos de ingresos.

Ingresos.html

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Ingresos | Contabilidad</title>
  <style>
    /* style.css */
body, html {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  background: #f9f9f9;
}

header {
  width: 800px;
  margin: auto;
  padding: 20px 0;
  text-align: center;
}

header h1 {
  margin: 0;
}

main {
  width: 800px;
  margin: auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

/* Resumen del panel */
.resumen p {
  font-size: 18px;
  margin: 10px 0;
}

/* Lista de movimientos */
.lista-movimientos {
  margin-top: 20px;
}

.movimiento {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #eee;
  border-radius: 5px;
  margin-bottom: 5px;
}

.ingreso {
  background: #e0f7e0;
}

.gasto {
  background: #fde0e0;
}

/* Formularios para añadir ingreso/gasto */
form {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

form input[type="text"],
form input[type="number"],
form input[type="date"] {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

form input[type="submit"] {
  padding: 10px;
  background: teal;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

form input[type="submit"]:hover {
  background: #006666;
}

/* Botón flotante para añadir movimientos (opcional) */
#nuevo {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: teal;
  color: white;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  text-align: center;
  font-size: 30px;
  line-height: 50px;
  text-decoration: none;
  font-weight: bold;
  box-shadow: 0 0 5px rgba(0,0,0,0.2);
}

#nuevo:hover {
  background: #006666;
}
  </style>
</head>
<body>
  <header>
    <h1>Ingresos</h1>
    <a href="{{ url_for('panel', usuario_id=usuario_id) }}">Volver al panel</a>
  </header>

  <main>
    <div class="lista-movimientos">
      {% for ingreso in ingresos %}
        <div class="movimiento ingreso">
          <span>{{ ingreso.nombre }}</span>
          <span>+ €{{ ingreso.cantidad }}</span>
          <span>{{ ingreso.date }}</span>
        </div>
      {% endfor %}
    </div>

    <h2>Añadir ingreso</h2>
    <form action="{{ url_for('nuevo_ingreso', usuario_id=usuario_id) }}" method="POST">
      <input type="text" name="nombre" placeholder="Nombre del ingreso" required>
      <input type="number" step="0.01" name="cantidad" placeholder="Cantidad" required>
      <input type="date" name="date" required>
      <input type="text" name="nota" placeholder="Nota (opcional)">
      <input type="submit" value="Añadir ingreso">
    </form>
  </main>
</body>
</html>


Este archivo muestra la pagina de ingresos del usuario se listan todos los ingresos guardados en la base de datos usando un bucle de Jinja2 tambien incluye un formulario para añadir un nuevo ingreso donde todos los campos principales son obligatorios la pagina mantiene un diseño sencillo y claro para facilitar la lectura de los movimientos.


Ingresos.js


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


Este archivo gestiona la parte visual de los ingresos permite mostrar u ocultar el formulario para añadir ingresos valida que los campos no esten vacios y añade el nuevo ingreso directamente a la lista de movimientos sin necesidad de recargar la pagina todo esto se hace de forma dinamica con JavaScript.

P.D: El de gastos es el miso pero en vez de ingresos de gastos por eso no lo he añadido, por que son miy similares por no decir practicamente iguales pero cambiando esas palabras.

Ahora vamos a por las estadisticas.


Estadisticas.html


<!DOCTYPE html>
<!-- Documento HTML5 -->
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <!-- Codificación para caracteres especiales -->

    <title>Estadísticas | Contabilidad</title>
    <!-- Título de la pestaña -->

    <style>
      /* Estilos generales */
      body,
      html {
        margin: 0;
        height: 100%;
        font-family: Arial, sans-serif;
        background: #f4f6f8;
      }

      /* Layout general: sidebar + contenido */
      .layout {
        display: flex;
        height: 100vh;
      }

      /* Barra lateral */
      .sidebar {
        width: 220px;
        background: teal;
        color: white;
        padding: 20px;
        box-sizing: border-box;
      }

      /* Título del menú */
      .sidebar h2 {
        margin-top: 0;
        text-align: center;
      }

      /* Enlaces del menú */
      .sidebar a {
        display: block;
        margin: 15px 0;
        color: white;
        text-decoration: none;
        font-size: 18px;
      }

      /* Efecto hover */
      .sidebar a:hover {
        text-decoration: underline;
      }

      /* Área principal */
      .content {
        flex: 1;
        padding: 30px;
      }

      /* Cabecera */
      header {
        text-align: center;
        margin-bottom: 30px;
      }

      /* Contenedor principal */
      main {
        max-width: 900px;
        margin: auto;
      }

      /* Tarjetas de estadísticas */
      .card {
        background: white;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
      }

      .card h3 {
        margin-top: 0;
        margin-bottom: 15px;
      }

      /* Zona donde irá el gráfico */
      .grafico {
        height: 180px;
        background: #e0e0e0;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #555;
        font-size: 18px;
      }
    </style>
  </head>

  <body>
    <!-- Contenedor general -->
    <div class="layout">
      <!-- Barra lateral de navegación -->
      <aside class="sidebar">
        <h2>Menú</h2>

        <!-- Enlaces dinámicos con Flask -->
        <a href="{{ url_for('panel', usuario_id=usuario_id) }}">🏠 Panel</a>
        <a href="{{ url_for('ingresos', usuario_id=usuario_id) }}">💰 Ingresos</a>
        <a href="{{ url_for('gastos', usuario_id=usuario_id) }}">💸 Gastos</a>
        <a href="{{ url_for('presupuestos', usuario_id=usuario_id) }}">📅 Presupuestos</a>
        <a href="{{ url_for('estadisticas', usuario_id=usuario_id) }}">📈 Estadísticas</a>
        <a href="{{ url_for('perfil', usuario_id=usuario_id) }}">👤 Perfil</a>
      </aside>

      <!-- Contenido principal -->
      <div class="content">
        <!-- Encabezado -->
        <header>
          <h1>Estadísticas</h1>
          <p>Resumen visual de tus finanzas</p>
        </header>

        <main>
          <!-- Tarjeta 1 -->
          <div class="card">
            <h3>Ingresos vs Gastos</h3>

            <!-- Aquí luego irá un gráfico real -->
            <div class="grafico">Próximamente gráfico 📊</div>
          </div>

          <!-- Tarjeta 2 -->
          <div class="card">
            <h3>Distribución de gastos</h3>

            <!-- Zona del segundo gráfico -->
            <div class="grafico">Próximamente gráfico 📉</div>
          </div>
        </main>
      </div>
    </div>
  </body>
</html>


Este archivo corresponde a la seccion de estadisticas mantiene la misma estructura de panel con barra lateral y contenido principal se muestran tarjetas preparadas para incluir graficos en el futuro actualmente se usan contenedores de prueba que indican donde iran los graficos de ingresos y gastos.

Ahora vamos con presupuestos.

Presupuestos.hmtl


<!DOCTYPE html>
<!-- Documento HTML5 -->
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <!-- Codificación para mostrar correctamente acentos y caracteres especiales -->

    <title>Presupuesto | Aplicación de Cuentas</title>
    <!-- Título de la pestaña -->

    <!-- Enlace a hoja de estilos externa -->
    <link rel="stylesheet" href="estilo/style.css" />
  </head>

  <body>
    <!-- Contenedor principal de la aplicación -->
    <div class="app">
      <!-- ============================
           BARRA LATERAL
      ============================ -->
      <aside class="sidebar">
        <!-- Logo de la app -->
        <h2 class="logo">A P C</h2>

        <!-- Menú de navegación -->
        <nav>
          <a href="../../../panel/index.html">Dashboard</a>
          <a href="../ingresos/ingresos.html">Ingresos</a>
          <a href="../gastos/gastos.html">Gastos</a>
          <!-- Página actual marcada como activa -->
          <a class="active" href="../presupuestos/presupuestos.html">Presupuesto</a>
          <a href="../estadisticas/estadisticas.html">Estadísticas</a>
          <a href="../perfil/perfil.html">Perfil</a>
        </nav>
      </aside>

      <!-- ============================
           CONTENIDO PRINCIPAL
      ============================ -->
      <main class="content">
        <!-- Título de la sección -->
        <h2>Presupuesto Mensual</h2>

        <!-- Tarjeta de ingresos previstos -->
        <div class="presupuesto-card">
          <p>Ingresos previstos</p>
          <h3>€1.500,00</h3>
        </div>

        <!-- Tarjeta de gastos previstos -->
        <div class="presupuesto-card">
          <p>Gastos previstos</p>
          <h3>€1.000,00</h3>
        </div>

        <!-- Tarjeta de saldo estimado -->
        <div class="presupuesto-card">
          <p>Saldo estimado</p>
          <h3>€500,00</h3>
        </div>
      </main>
    </div>
  </body>
</html>


Este archivo muestra la pagina de presupuestos mensuales se presenta la informacion en tarjetas donde se indican los ingresos previstos los gastos previstos y el saldo estimado la estructura esta pensada para mostrar un resumen rapido del presupuesto del usuario.

Ahora vamos con perfil.

Perfil.html

<!DOCTYPE html>
<!-- Documento HTML5 -->
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <!-- Permite mostrar acentos y caracteres especiales -->

    <title>Perfil | Aplicación de Cuentas</title>
    <!-- Título que aparece en la pestaña -->

    <!-- Enlace a la hoja de estilos externa -->
    <link rel="stylesheet" href="estilo/style.css" />
  </head>

  <body>
    <!-- Contenedor principal de la app -->
    <div class="app">
      <!-- ============================
           BARRA LATERAL
      ============================ -->
      <aside class="sidebar">
        <!-- Logo o nombre de la aplicación -->
        <h2 class="logo">A P C</h2>

        <!-- Menú de navegación -->
        <nav>
          <a href="../../../panel/index.html">Dashboard</a>
          <a href="../ingresos/ingresos.html">Ingresos</a>
          <a href="../gastos/gastos.html">Gastos</a>
          <a href="../presupuestos/presupuestos.html">Presupuesto</a>
          <a href="../estadisticas/estadisticas.html">Estadísticas</a>
          <!-- La página actual se marca como activa -->
          <a class="active" href="perfil.html">Perfil</a>
        </nav>
      </aside>

      <!-- ============================
           CONTENIDO PRINCIPAL
      ============================ -->
      <main class="content">
        <!-- Título de la sección -->
        <h2>Perfil</h2>

        <!-- Tarjeta con el nombre del usuario -->
        <div class="perfil-card">
          <p>Usuario:</p>
          <h3>Juan Pérez</h3>
        </div>

        <!-- Tarjeta con el email -->
        <div class="perfil-card">
          <p>Email:</p>
          <h3>juan@email.com</h3>
        </div>

        <!-- Tarjeta con la contraseña (oculta) -->
        <div class="perfil-card">
          <p>Contraseña:</p>
          <h3>********</h3>
        </div>

        <!-- Botón para editar el perfil -->
        <button class="editar-btn">Editar perfil</button>
      </main>
    </div>
  </body>
</html>


Este archivo corresponde a la pagina de perfil del usuario se muestran los datos personales como el nombre el email y la contraseña oculta tambien incluye un boton para editar el perfil mantiene la misma estructura visual que el resto de la aplicacion para que todo sea coherente.


3. Conclusion

A lo largo del desarrollo hemos trabajado con HTML, CSS y JavaScript para el frontend, y con Flask para la navegación dinámica y la conexión con el backend, utilizando Jinja2 para pasar los datos entre servidor y cliente. También hemos aprendido a estructurar un proyecto real, a manejar rutas, formularios, peticiones al servidor y a mostrar la información de forma dinámica según el usuario que inicia sesión.

Aunque surgieron algunos problemas, como la carga de los estilos CSS, se pudieron solucionar adaptando el código y añadiendo los estilos directamente en los archivos HTML, lo que nos permitió seguir avanzando con el proyecto. En general, el resultado final cumple los objetivos planteados, ya que permite al usuario gestionar sus ingresos, gastos, presupuestos y visualizar estadísticas de forma clara, sentando una buena base para futuras mejoras como gráficos reales o más opciones de personalización.
```
