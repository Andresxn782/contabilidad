1. Explicacion del proyecto

He creado la base de datos en relacion a mi proyecto de contabilidad personal, sin mucho lio, que no sea complicada, que sea facil de usar y visible para que no cause lios a la persona, la aplicacion esta hecha para personas jovenes, sin muchos ingresos, para que puedan ahorrar dinero y ver sus gastos e ingresos claramente, aparte de una tabla grafica y los presupuestos que tienen previstos para el siguiente mes.

2. Modelo de datos

El modelo de datos de la base de datos contabilidad está diseñado para gestionar usuarios y su información financiera, incluyendo:

-ingresos
-gastos
-categorías
-presupuestos.

Todas las entidades están relacionadas mediante claves foráneas al usuario, asi garantizamos la integridad de los datos y permitiendo la eliminación en cascada. Este modelo facilita el control y análisis financiero individual de cada usuario de forma organizada.

A continuacion vamos a explicar el modelo de datos y como hemos creado la base de datos y la explicacion de sus tablas y la vista general.

El proyecto se compone de 5 tablas:

-usuario
-ingresos
-gastos
-categorías
-presupuestos

Vamos a empezar por la de usuarios:

-- Archivo: tabla_usuarios.sql
-- Creación de la tabla 'usuarios' con explicación línea por línea

CREATE TABLE usuarios (
id INT AUTO_INCREMENT PRIMARY KEY,
usuario VARCHAR(50) NOT NULL,
email VARCHAR(100) NOT NULL UNIQUE,
password VARCHAR(100) NOT NULL,
is_admin TINYINT(1) NOT NULL DEFAULT 0
);

-Como se puede ver en esta tabla aqui añadiremos los usuarios y el administrador y los datos de estos.
Con el varchar indicamos el maximo de caracteres que pueden tener tanto el nombre de usuario como el correo electronico y la contraseña. Con el not null indecamos que el dato que tiene que insertar es obligatorio y que sino lo inserta no dejara acceder a la seguiente pagina.

Ahora vamos con categorias:

CCREATE TABLE categorias (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(50) NOT NULL,
type ENUM('ingreso','gasto') NOT NULL,
usuario_id INT NOT NULL,
FOREIGN KEY (usuario_id)
REFERENCES usuarios(id)
ON DELETE CASCADE
);

-En esta tabla guardaremos las categorias que puede usar cada usuario para clasificar sus ingresos o gastos la columna id sirve para identificar de forma unica cada categoria y se genera automaticamente, nombre guarda el nombre de la categoria y con el varchar indicamos el maximo de caracteres que se pueden, type indica si la categoria es de tipo ingreso o gasto y tambien es obligatorio usuario_id relaciona la categoria con un usuario especifico de la tabla usuarios asegurando que cada categoria pertenezca a un usuario la relacion con la tabla usuarios usa foreign key con on delete cascade lo que significa que si se elimina un usuario todas sus categorias asociadas tambien se borraran automaticamente.

Ahora vamos con ingresos:

CREATE TABLE ingresos (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(50) NOT NULL,
cantidad DECIMAL(10,2) NOT NULL,
date DATE NOT NULL,
nota TEXT,
categoria_id INT,
usuario_id INT NOT NULL,
FOREIGN KEY (usuario_id)
REFERENCES usuarios(id)
ON DELETE CASCADE,
FOREIGN KEY (categoria_id)
REFERENCES categorias(id)
ON DELETE SET NULL
);

-En esta tabla guardaremos todos los ingresos de los usuarios cada ingreso tiene un nombre obligatorio que con el varchar indicamos el maximo de caracteres que se pueden, cantidad es el dinero del ingreso obligatorio, date que indica la fecha del ingreso nota que es opcional, categoria_id relaciona el ingreso con una categoria y puede ser nula y usuario_id que indica que usuario registro el ingreso, la columna id sirve para identificar de forma unica cada ingreso y se genera automaticamente las relaciones con usuario y categoria usan foreign key si se elimina el usuario se borran sus ingresos y si se elimina la categoria se pone en null categoria_id.

Ahora vamos con gastos:

CREATE TABLE gastos (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(50) NOT NULL,
cantidad DECIMAL(10,2) NOT NULL,
date DATE NOT NULL,
nota TEXT,
categoria_id INT,
usuario_id INT NOT NULL,
FOREIGN KEY (usuario_id)
REFERENCES usuarios(id)
ON DELETE CASCADE,
FOREIGN KEY (categoria_id)
REFERENCES categorias(id)
ON DELETE SET NULL
);

-En esta tabla guardaremos todos los gastos de los usuarios cada gasto tiene un nombre obligatorio que con el varchar indicamos el maximo de caracteres que se pueden, cantidad que es el dinero del gasto obligatorio, date indica la fecha del gasto, nota es opcional, categoria_id relaciona el gasto con una categoria y puede ser nula y usuario_id indica que usuario registro el gasto, la columna id sirve para identificar de forma unica cada gasto y se genera automaticamente las relaciones con usuario y categoria usan foreign key si se elimina el usuario se borran sus gastos y si se elimina la categoria se pone en null categoria_id

Y por ultimo vamos con presupuestos:

CREATE TABLE presupuestos (
id INT AUTO_INCREMENT PRIMARY KEY,
cantidad DECIMAL(10,2) NOT NULL,
periodo ENUM('mensual') NOT NULL,
usuario_id INT NOT NULL,
FOREIGN KEY (usuario_id)
REFERENCES usuarios(id)
ON DELETE CASCADE
);

-En esta tabla guardaremos los presupuestos de cada usuario, la columna id sirve para identificar de forma unica cada presupuesto y se genera automaticamente cantidad indica el dinero del presupuesto obligatorio, periodo indica el periodo del presupuesto que es mensual y es obligatorio, usuario_id relaciona el presupuesto con un usuario la relacion usa foreign key con on delete cascade si se elimina el usuario se borran sus presupuestos.

A continuacion creamos la vista:

CREATE VIEW vista_dashboard AS
SELECT
u.id AS usuario_id,
COALESCE(SUM(i.cantidad), 0) AS ingresos,
COALESCE(SUM(g.cantidad), 0) AS gastos
FROM usuarios u
LEFT JOIN ingresos i ON u.id = i.usuario_id
LEFT JOIN gastos g ON u.id = g.usuario_id
GROUP BY u.id;

La vista vista_dashboard muestra un resumen de ingresos y gastos por usuario. Para cada usuario, suma todos sus ingresos y todos sus gastos, reemplazando los valores nulos por cero si no tiene movimientos. Usa LEFT JOIN para incluir a todos los usuarios, incluso los que no tienen ingresos o gastos. Finalmente, agrupa los resultados por usuario, mostrando una fila por cada uno con sus totales.
