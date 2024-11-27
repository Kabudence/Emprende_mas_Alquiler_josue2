-- Insertar un usuario (dueño del negocio)
INSERT INTO usuarios (nombre_usuario, username, email, password, tipo_usuario)
VALUES 
('Juan Pérez', 'juanperez', 'juan@correo.com', 'hashed_password_here', 'business_owner');

INSERT INTO usuarios (nombre_usuario, username, email, password, tipo_usuario)
VALUES 
('Carlos García', 'carlosgarcia', 'carlos@correo.com', 'hashed_password_here', 'cliente'),
('Ana Martínez', 'anamartinez', 'ana@correo.com', 'hashed_password_here', 'cliente');

INSERT INTO rubros (nombre) 
VALUES 
('Tecnología'),
('Electrodomésticos'),
('Ropa y moda');

INSERT INTO negocios (nombre_negocio, ruc, razon_social, direccion, telefono, departamento, provincia, distrito, rubro_id, usuario_id)
VALUES 
('ElectroStore', '12345678901', 'ElectroStore S.A.C.', 'Av. Siempre Viva 123', '999999999', 'Lima', 'Lima', 'Miraflores', 1, 1);  -- Asume que el rubro 'Tecnología' tiene id 1 y el usuario tiene id 1

INSERT INTO categorias (nombre, rubro_id) 
VALUES 
('Laptops', 1),
('Smartphones', 1), 
('Refrigeradores', 2),
('Lavadoras', 2),
('Ropa de Mujer', 3),
('Ropa de Hombre', 3);

INSERT INTO tamanios (nombre, categoria_id)
VALUES 
('Pequeño', 1),  -- Laptops
('Mediano', 1),  -- Laptops
('Grande', 2),  -- Smartphones
('Extra Grande', 2),  -- Smartphones
('Chico', 3),  -- Refrigeradores
('Grande', 3),  -- Refrigeradores
('Mediano', 4),  -- Lavadoras
('Grande', 4),  -- Lavadoras
('S', 5),  -- Ropa de Mujer
('M', 5),  -- Ropa de Mujer
('L', 6),  -- Ropa de Hombre
('XL', 6);  -- Ropa de Hombre

INSERT INTO colores (nombre, hexadecimal) 
VALUES 
('Rojo', '#FF0000'),
('Azul', '#0000FF'),
('Verde', '#00FF00'),
('Negro', '#000000'),
('Blanco', '#FFFFFF'),
('Amarillo', '#FFFF00');
