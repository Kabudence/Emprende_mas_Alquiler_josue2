-- Insertar la tabla tipos_categoria
INSERT INTO tipos_categoria (nombre) 
VALUES 
('Producto'),
('Servicio');

-- Insertar usuarios
INSERT INTO usuarios (nombre, username, email, password, tipo_usuario)
VALUES 
('Juan Pérez', 'juanperez', 'juan@correo.com', 'hashed_password_here', 'business_owner'),
('Carlos García', 'carlosgarcia', 'carlos@correo.com', 'hashed_password_here', 'cliente'),
('Ana Martínez', 'anamartinez', 'ana@correo.com', 'hashed_password_here', 'cliente');

-- Insertar rubros
INSERT INTO rubros (nombre) 
VALUES 
('Tecnología'),
('Electrodomésticos'),
('Ropa y moda');

-- Insertar negocios
INSERT INTO negocios (nombre, ruc, razon_social, direccion, telefono, departamento, provincia, distrito, rubro_id, usuario_id)
VALUES 
('ElectroStore', '12345678901', 'ElectroStore S.A.C.', 'Av. Siempre Viva 123', '999999999', 'Lima', 'Lima', 'Miraflores', 1, 1);

-- Insertar categorías
INSERT INTO categorias (nombre, rubro_id, tipo_id) 
VALUES 
-- Tecnología
('Laptops', 1, 1),  -- Producto
('Soporte Técnico', 1, 2),  -- Servicio

-- Electrodomésticos
('Refrigeradores', 2, 1),  -- Producto
('Instalación de Electrodomésticos', 2, 2),  -- Servicio

-- Ropa y moda
('Ropa de Mujer', 3, 1),  -- Producto
('Asesoría de Estilo', 3, 2);  -- Servicio

-- Insertar tamaños
INSERT INTO tamanios (nombre, categoria_id)
VALUES 
-- Tecnología
('Pequeño', 1),
('Mediano', 1),
('Grande', 1),

-- Electrodomésticos
('Chico', 2),
('Mediano', 2),
('Grande', 2),

-- Ropa y moda
('S', 3),
('M', 3),
('L', 3);

-- Insertar colores
INSERT INTO colores (nombre, hexadecimal) 
VALUES 
('Rojo', '#FF0000'),
('Azul', '#0000FF'),
('Verde', '#00FF00'),
('Negro', '#000000'),
('Blanco', '#FFFFFF'),
('Amarillo', '#FFFF00');
