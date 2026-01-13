-- ------------------------
-- INSERTAR USUARIO ADMIN
-- ------------------------
INSERT INTO usuarios (usuario, email, password)
VALUES ('admin', 'admin@correo.com', 'admin123');

-- Suponiendo que el id generado es 1
-- ------------------------
-- INSERTAR CATEGORIAS
-- ------------------------
INSERT INTO categorias (nombre, type, usuario_id)
VALUES 
('Nómina', 'ingreso', 1),
('Regalo', 'ingreso', 1),
('Alquiler', 'gasto', 1),
('Supermercado', 'gasto', 1);

-- ------------------------
-- INSERTAR INGRESOS
-- ------------------------
INSERT INTO ingresos (nombre, cantidad, date, nota, categoria_id, usuario_id)
VALUES
('Nómina Enero', 1200.00, '2026-01-01', 'Pago mensual', 1, 1),
('Regalo Cumpleaños', 50.00, '2026-01-05', 'Dinero recibido', 2, 1);

-- ------------------------
-- INSERTAR GASTOS
-- ------------------------
INSERT INTO gastos (nombre, cantidad, date, nota, categoria_id, usuario_id)
VALUES
('Alquiler Piso', 700.00, '2026-01-10', 'Pago mensual alquiler', 3, 1),
('Compra Supermercado', 45.99, '2026-01-12', 'Supermercado semanal', 4, 1);

-- ------------------------
-- INSERTAR PRESUPUESTO
-- ------------------------
INSERT INTO presupuestos (cantidad, periodo, usuario_id)
VALUES
(1500.00, 'mensual', 1);
