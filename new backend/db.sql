-- sudo mysql -u root -p

-- Crear base de datos
CREATE DATABASE contabilidad;

USE contabilidad;

-- TABLA USUARIOS --
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);
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
