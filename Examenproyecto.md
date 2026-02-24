1. Introduccion

Hemos creado un proyecto de contabilidad personal, tiene su login, con el que accedes con tu usuario/correo y contraseña, cuando entras tienes varias cosas, una barra a la izquierda con los apartados y luego en el centro el sueldo actual y abajo los ingresos, los gastos y un historial de tu cuenta y luego en el menu de la izquierda cada apartado.

La aplicacion esta hecha para personas jovenes, sin muchos ingresos, para que puedan ahorrar dinero y ver sus gastos e ingresos claramente, aparte de una tabla grafica y los presupuestos que tienen previstos para el siguiente mes.

2. Por que este proyecto?

Escogimos este proyecto por que muchos jovenes hoy en dia no saben ahorrar, y malgastan el dinero en cosas innecesarias, por eso hemos creado la aplicacion de contabilidad personal, para que los jovenes aprendan a organizar su dinero y asi poder ahorrar .

3. Con quien he hecho el proyecto y por que?

He hecho el proyecto con Nicolás García, por que los dos estabamos de acuerdo en lo que queremos hacer, el se quiere dedicar al backend y yo al front, asi que decidimos hacerlo asi, el hacia el backend y me iba diciendo como lo iba creando y yo iba haciendo el front y lo ibamos explicando y entre los dos hicimos el app.py.

4. Tecnologias que han sido escogidas

En este proyecto hemos utilizado para el front html, css y js.Para unir todo python con flask y pymsql (debido a que cuando intentamos utilizar mysql.connect nos daba error y tras varios intentos lo cambiamos), y luego para la base de datos utilizamos mysql

5. Hablar del proyecto

Mi proyecto es una aplicación web de contabilidad personal hecha con Python y Flask en el backend, MySQL como base de datos y HTML, CSS y JavaScript en el frontend. La idea principal del proyecto es que cualquier persona pueda gestionar su dinero de forma sencilla, poder ver cuánto ingresa, cuánto gasta, cuánto dinero le queda, controlar presupuestos y ver estadísticas de sus gastos y ingresos. La necesidad que resuelve es la de organizar tus cuentas personales sin tener que depender de hojas de cálculo o de apuntes manuales, todo en un solo sitio y con información en tiempo real.

Cuando entras en la aplicación, la primera pantalla es el login. Aquí el usuario introduce su email y su contraseña. Esta pantalla valida que los datos existen en la base de datos y, si son correctos, te redirige al panel principal. Si el email o la contraseña no coinciden, te avisa con un mensaje de error. Además, los inputs están bien identificados: aparece “Usuario o Email”, “Contraseña” y el botón “Iniciar sesión”, para que todo sea claro desde el principio. Esto hace que la aplicación sea segura y personalizada, ya que cada usuario ve solo sus datos.

Una vez has iniciado sesion, llegas al panel principal. Esta pantalla funciona como el resume tu dinero. En la parte superior aparece tu saldo total restando los gastos de los ingresos. Luego, hay tarjetas separadas que muestran el total de ingresos y el total de gastos. La información se obtiene directamente de la base de datos usando consultas SQL que suman todas las entradas y salidas de dinero del usuario. La interfaz está organizada y usa colores: verde para los ingresos, rojo para los gastos, y tarjetas blancas con sombras que hacen que todo sea más visual. Desde el panel, también puedes ver tu ID de usuario, lo que ayuda a identificar a cada usuario dentro del sistema.

Desde el panel, puedes acceder a las secciones de ingresos y gastos. En ambas secciones puedes ver todos los movimientos que has registrado y añadir nuevos. Cada ingreso o gasto se guarda con su nombre, cantidad, fecha y nota opcional, y todo se guarda asociado a tu usuario. Esto hace que puedas revisar tu historial de movimientos de manera ordenada y con la información completa, incluyendo las fechas, lo que te permite llevar un control detallado de tus finanzas.

El apartado de presupuestos te permite establecer objetivos de gasto o ahorro para periodos concretos, por ejemplo mensuales. Aquí puedes ver cuánto dinero planeas gastar o ahorrar y comparar con tus ingresos y gastos reales. Esto te ayuda a planificar mejor tu dinero y no gastar más de lo que deberías. Los datos también vienen de la base de datos y se muestran en tarjetas visuales similares a las del panel principal, manteniendo la misma estética y coherencia en el diseño.

En el apartado de estadísticas, la aplicación muestra gráficos y resúmenes sobre tus movimientos. Por ejemplo, puedes comparar ingresos y gastos, o ver en qué categorías estás gastando más dinero. Esto te da una perspectiva visual de lo que haces en tu dia a dia con tu dinero y te permite identificar rápidamente dónde puedes ahorrar o mejorar tu gestión de dinero.

Finalmente, en la sección de perfil puedes ver tus datos personales guardados en la base de datos: tu nombre, email y contraseña (oculta para seguridad). Esto permite que cada usuario pueda tener control sobre su información y, si en el futuro añadimos edición de perfil, modificar estos datos.

En cuanto a la parte técnica, la aplicación funciona perfectamente con rutas dinámicas usando el usuario_id para que cada pantalla muestre solo los datos de quien está logueado. Se conectan los inputs con la base de datos usando MySQL y PyMySQL, y los datos se muestran en tiempo real en la interfaz usando Flask y Jinja para renderizar las plantillas. Además, el estilo es consistente en todas las pantallas: barra lateral teal fija, tarjetas blancas con sombras, colores diferenciando ingresos y gastos, y un layout flexible que se adapta a cualquier pantalla.

En resumen, este proyecto es una aplicación completa de gestión financiera personal. Permite registrar y visualizar ingresos y gastos, gestionar presupuestos, ver estadísticas y mantener un perfil de usuario seguro. Todo está conectado a la base de datos y funciona en tiempo real, con un diseño consistente y fácil de usar. He aprendido a integrar backend y frontend, manejar bases de datos, depurar errores y construir una interfaz coherente, resolviendo problemas reales de rutas, consultas SQL y presentación de datos. Esta aplicación no solo funciona, sino que está preparada para escalar y mejorar en el futuro, por ejemplo añadiendo gráficos reales en estadísticas o opciones de edición de perfil.
