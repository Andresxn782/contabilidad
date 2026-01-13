-- sudo mysql -u root -p

-- Crear base de datos
CREATE DATABASE contabilidad;

USE contabilidad;

-- Crear usuario y otorgar permisos
-- Creamos la base de datos contabilidad y un usuario específico llamado usuario_app con permisos completos sobre ella
CREATE USER 'usuario_app'@'localhost' IDENTIFIED BY 'Contabilidad123$';
GRANT ALL PRIVILEGES ON contabilidad.* TO 'usuario_app'@'localhost';
FLUSH PRIVILEGES;

/*
======================= TABLAS =======================
El sistema se divide en usuarios, categorías, ingresos, gastos y presupuestos para separar responsabilidades
Todas las tablas dependen del usuario mediante claves foráneas (FKs) con borrado en cascada
*/
-- TABLA USUARIOS --
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    is_admin TINYINT(1) NOT NULL DEFAULT 0
);
-- 0 = usuario normal, 1 = administrador

-- TABLA CATEGORIAS --
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    type ENUM('ingreso','gasto') NOT NULL,
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);
-- TABLA INGRESOS --
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
-- TABLA GASTOS --
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
-- TABLA PRESUPUESTOS --
CREATE TABLE presupuestos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cantidad DECIMAL(10,2) NOT NULL,
    periodo ENUM('mensual') NOT NULL,
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);

-- AÑADO USUARIO ADMNINISTRADOR A LA TABLA USUARIOS --
INSERT INTO usuarios (usuario, email, password, is_admin)
VALUES ('admin', 'admin@admin.com', 'admin123', 1);




-- ÍNDICES --
CREATE INDEX idx_ingresos_usuario ON ingresos(usuario_id);
CREATE INDEX idx_gastos_usuario ON gastos(usuario_id);
CREATE INDEX idx_categorias_usuario ON categorias(usuario_id);

-- JOIN EJEMPLO --
-- Usamos LEFT JOIN para mostrar información completa incluso cuando no hay categoría asociada
SELECT g.*, c.nombre
FROM gastos g
LEFT JOIN categorias c ON g.categoria_id = c.id;


-- VIEWS SQL --
-- Creamos una vista para simplificar el cálculo del dashboard y evitar repetir consultas complejas
CREATE VIEW vista_dashboard AS
SELECT
    u.id AS usuario_id,
    COALESCE(SUM(i.cantidad), 0) AS ingresos,
    COALESCE(SUM(g.cantidad), 0) AS gastos
FROM usuarios u
LEFT JOIN ingresos i ON u.id = i.usuario_id
LEFT JOIN gastos g ON u.id = g.usuario_id
GROUP BY u.id;

-- COMANDOS ADMIN --
-- Usamos SHOW TABLES, DESCRIBE y SELECT para inspección y control
SHOW TABLES;
DESCRIBE usuarios;
SELECT * FROM ingresos;

