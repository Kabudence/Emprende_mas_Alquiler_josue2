-- Insertando datos en la tabla `rubros`
INSERT INTO `rubros` VALUES (2,'Electrodomésticos'),(3,'Ropa y moda'),(1,'Tecnología');

-- Insertando datos en la tabla `tipos_categoria`
INSERT INTO `tipos_categoria` VALUES (1,'Producto'),(2,'Servicio');

-- Insertando datos en la tabla `categorias`
INSERT INTO `categorias` VALUES 
(1,'Laptops',1,1),
(2,'Soporte Técnico',1,2),
(3,'Refrigeradores',2,1),
(4,'Instalación de Electrodomésticos',2,2),
(5,'Ropa de Mujer',3,1),
(6,'Asesoría de Estilo',3,2),
(7,'Celular',1,1),
(8,'Reparación de laptop',1,2);

-- Insertando datos en la tabla `categorias_feedback`
INSERT INTO `categorias_feedback` VALUES (1,'comentario'),(2,'reconocimiento');

-- Insertando datos en la tabla `colores`
INSERT INTO `colores` VALUES 
(1,'Rojo','#FF0000'),
(2,'Azul','#0000FF'),
(3,'Verde','#00FF00'),
(4,'Negro','#000000'),
(5,'Blanco','#FFFFFF'),
(6,'Amarillo','#FFFF00'),
(7,'Lila','#E04CE0');

-- Insertando datos en la tabla `productos`
INSERT INTO `productos` VALUES 
(2,'Galaxy A55','El Samsung Galaxy A55 8GB RAM 256GB es un smartphone de alto rendimiento diseñado para ofrecer una experiencia fluida y potente. Equipado con el procesador Exynos 1480 octa-core, con velocidades de hasta 2.75 GHz, y 8GB de RAM, este dispositivo asegura un rendimiento superior para todas tus tareas. Su pantalla de 6.6 pulgadas te permite disfrutar de imágenes nítidas y vibrantes, mientras que la cámara frontal de 32 MP captura selfies de alta calidad. Con una batería de 5000 mAh, podrás usar tu teléfono durante todo el día sin problemas. Además, cuenta con lector de huella, GPS integrado y sistema operativo Android. Disponible en un elegante color lila.',7);

-- Insertando datos en la tabla `tamanios`
INSERT INTO `tamanios` VALUES 
(1,'Pequeño',1),
(2,'Mediano',1),
(3,'Grande',1),
(4,'Chico',2),
(5,'Mediano',2),
(6,'Grande',2),
(7,'S',3),
(8,'M',3),
(9,'L',3),
(10,'6 pulgadas',7);

-- Insertando datos en la tabla `detalles`
INSERT INTO `detalles` VALUES 
(2,4,2,10,50,'ddb211d9ec6b468c85ebb88be89845df_galaxy_negro.png',600.00,'64gb de almacenamiento'),
(3,7,2,10,40,'6c1dc4c14d4942b98f4aee49bdfb4f2e_galaxy_lila.png',700.00,'128gb de almacenamiento');

-- Insertando datos en la tabla `usuarios`
INSERT INTO `usuarios` VALUES 
(1,'Juan Pérez','juanperez','juan@correo.com','hashed_password_here','business_owner'),
(2,'Carlos García','carlosgarcia','carlos@correo.com','hashed_password_here','cliente'),
(3,'Ana Martínez','anamartinez','ana@correo.com','hashed_password_here','cliente');

-- Insertando datos en la tabla `negocios`
INSERT INTO `negocios` VALUES 
(1,'ElectroStore','12345678901','ElectroStore S.A.C.','Av. Siempre Viva 123','999999999','Lima','Lima','Miraflores',1,1);

-- Insertando datos en la tabla `servicios`
INSERT INTO `servicios` VALUES 
(1,'Reparación de Celulares','Servicio completo de reparación de celulares que incluye cambio de pantalla, batería, y resolución de problemas de software.',150.00,120.00,'c39244182d864813903d45ab7ae3934c_reparacion_de_celular.jpg','922574309','miguel@mail.com',2),
(2,'Reparación de Laptops','Servicio especializado en reparación de laptops, incluyendo reemplazo de pantalla, teclado, y solución de problemas de hardware y software.',200.00,150.00,'4b379ba53247427195f9ae5a6cf20e44_reparacion_de_laptops.jpg','922574309','carlos.huaman@gmail.com',8);

-- Insertando datos en la tabla `feedbacks`
INSERT INTO `feedbacks` VALUES 
(1,'Producto llegó tarde','El producto llegó mucho más tarde de lo esperado, lo cual causó inconvenientes.','pantalla_rota.jpg','producto_dañado.jpg',2,2);

-- Insertando datos en la tabla `ventas`
INSERT INTO `ventas` VALUES 
(1,1,'2024-12-16 09:00:00',850.00);