-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-01-2025 a las 18:19:29
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `emprende_masv2`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `rubro_id` int(11) NOT NULL,
  `tipo_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id`, `nombre`, `rubro_id`, `tipo_id`) VALUES
(1, 'Laptops', 1, 1),
(2, 'Soporte Técnico', 1, 2),
(3, 'Refrigeradores', 2, 1),
(4, 'Instalación de Electrodomésticos', 2, 2),
(5, 'Ropa de Mujer', 3, 1),
(6, 'Asesoría de Estilo', 3, 2),
(7, 'Celular', 1, 1),
(8, 'Reparación de laptop', 1, 2),
(9, 'videojuegos', 1, 1),
(10, 'Reparación de Videojuegos', 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias_feedback`
--

CREATE TABLE `categorias_feedback` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias_feedback`
--

INSERT INTO `categorias_feedback` (`id`, `nombre`) VALUES
(1, 'comentario'),
(2, 'reconocimiento');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `colores`
--

CREATE TABLE `colores` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `hexadecimal` varchar(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `colores`
--

INSERT INTO `colores` (`id`, `nombre`, `hexadecimal`) VALUES
(1, 'Rojo', '#FF0000'),
(2, 'Azul', '#0000FF'),
(3, 'Verde', '#00FF00'),
(4, 'Negro', '#000000'),
(5, 'Blanco', '#FFFFFF'),
(6, 'Amarillo', '#FFFF00'),
(7, 'Lila', '#E04CE0'),
(8, 'Rosado', '#DCA7D0');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `colorv`
--

CREATE TABLE `colorv` (
  `idColor` int(11) NOT NULL,
  `Nombre_principal` varchar(45) DEFAULT NULL,
  `Nombre_hexadecimal_principal` varchar(7) DEFAULT NULL,
  `idEmpresa` int(11) DEFAULT NULL,
  `Nombre_secundario` varchar(45) DEFAULT NULL,
  `Nombre_hexadecimal_secundario` varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `colorv`
--

INSERT INTO `colorv` (`idColor`, `Nombre_principal`, `Nombre_hexadecimal_principal`, `idEmpresa`, `Nombre_secundario`, `Nombre_hexadecimal_secundario`) VALUES
(19, '#264ff2', '#264FF2', 15, '#ef1f72', '#EF1F72'),
(22, '#b82828', '#B82828', 25, '#c90d0d', '#C90D0D'),
(23, '#1809ec', '#1809ec', 26, '#3093fd', '#3093fd');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles`
--

CREATE TABLE `detalles` (
  `id` int(11) NOT NULL,
  `color_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `tamanio_id` int(11) NOT NULL,
  `stock` int(11) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `capacidad` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles`
--

INSERT INTO `detalles` (`id`, `color_id`, `producto_id`, `tamanio_id`, `stock`, `imagen`, `precio`, `capacidad`) VALUES
(2, 4, 2, 10, 50, 'ddb211d9ec6b468c85ebb88be89845df_galaxy_negro.png', 600.00, '64gb de almacenamiento'),
(3, 7, 2, 10, 40, '6c1dc4c14d4942b98f4aee49bdfb4f2e_galaxy_lila.png', 700.00, '128gb de almacenamiento'),
(6, 4, 5, 12, 15, '50f42a8962de49259b4103bc5c541a7b_AEROBICOS.jpg', 500.00, '10 gb'),
(7, 1, 5, 12, 5, 'f207c30d11764a8b8f5c376bd3735198_FUNCTIONAL.jpg', 600.00, '20 gb'),
(8, 4, 5, 13, 10, '6c69177446e545f1be6accbd6386647b_almuerzo_2.jpg', 100.00, '5 gb'),
(9, 6, 5, 13, 5, '07ea5cafe9fb4561981e8afedcb17f7c_cena_1.jpg', 150.00, '6 gb');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_venta`
--

CREATE TABLE `detalles_venta` (
  `id` int(11) NOT NULL,
  `venta_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `distritos`
--

CREATE TABLE `distritos` (
  `ID` bigint(20) UNSIGNED NOT NULL,
  `Nombre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `distritos`
--

INSERT INTO `distritos` (`ID`, `Nombre`) VALUES
(1, 'Ancón'),
(2, 'Ate'),
(3, 'Barranco'),
(4, 'Breña'),
(5, 'Carabayllo'),
(6, 'Chaclacayo'),
(7, 'Chorrillos'),
(8, 'Cieneguilla'),
(9, 'Comas'),
(10, 'El Agustino'),
(11, 'Independencia'),
(12, 'Jesús María'),
(13, 'La Molina'),
(14, 'La Victoria'),
(15, 'Lince'),
(16, 'Los Olivos'),
(17, 'Lurigancho'),
(18, 'Lurín'),
(19, 'Magdalena del Mar'),
(20, 'Miraflores'),
(21, 'Pachacámac'),
(22, 'Pucusana'),
(23, 'Pueblo Libre'),
(24, 'Puente Piedra'),
(25, 'Punta Hermosa'),
(26, 'Punta Negra'),
(27, 'Rímac'),
(28, 'San Bartolo'),
(29, 'San Borja'),
(30, 'San Isidro'),
(31, 'San Juan de Lurigancho'),
(32, 'San Juan de Miraflores'),
(33, 'San Luis'),
(34, 'San Martín de Porres'),
(35, 'San Miguel'),
(36, 'Santa Anita'),
(37, 'Santa María del Mar'),
(38, 'Santa Rosa'),
(39, 'Santiago de Surco'),
(40, 'Surquillo'),
(41, 'Villa El Salvador'),
(42, 'Villa María del Triunfo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empresa`
--

CREATE TABLE `empresa` (
  `idEmpresa` int(11) NOT NULL,
  `Nombre` varchar(255) NOT NULL,
  `Mision` text DEFAULT NULL,
  `Vision` text DEFAULT NULL,
  `Objetivos` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empresa`
--

INSERT INTO `empresa` (`idEmpresa`, `Nombre`, `Mision`, `Vision`, `Objetivos`) VALUES
(15, 'Consigueventas', 'Conseguir muchas ventas para navidad\r\n', 'A', 'A'),
(25, 'ewewewewew', 'wewewewew', 'wewewewe', 'wewewewewew'),
(26, 'ewewewe', 'wewewew', 'eewewe', 'rewewew');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `feedbacks`
--

CREATE TABLE `feedbacks` (
  `id` int(11) NOT NULL,
  `asunto` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `imagen1` varchar(255) DEFAULT NULL,
  `imagen2` varchar(255) DEFAULT NULL,
  `categoria_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `feedbacks`
--

INSERT INTO `feedbacks` (`id`, `asunto`, `descripcion`, `imagen1`, `imagen2`, `categoria_id`, `usuario_id`) VALUES
(1, 'Producto llegó tarde', 'El producto llegó mucho más tarde de lo esperado, lo cual causó inconvenientes.', 'pantalla_rota.jpg', 'producto_dañado.jpg', 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagen`
--

CREATE TABLE `imagen` (
  `idImagen` int(11) NOT NULL,
  `Tipo_imagen` enum('logo','icono') NOT NULL,
  `Filename` varchar(255) NOT NULL,
  `idEmpresa` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `imagen`
--

INSERT INTO `imagen` (`idImagen`, `Tipo_imagen`, `Filename`, `idEmpresa`) VALUES
(17, 'logo', 'images.jpeg', 15),
(18, 'icono', 'images.jpeg', 15),
(24, 'logo', 'logo_25_4708fd7c50994abba6d11ad9528fe95c.png', 25),
(25, 'icono', 'icono_25_782dc3abc81143c2b439482704e912e3.png', 25),
(26, 'logo', 'logo_26_be1ecc6a5aeb40a6b90da5b3dfa677dd.png', 26),
(27, 'icono', 'icono_26_6a78eee0dd04493980d70a2d901d580d.png', 26);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `negocios`
--

CREATE TABLE `negocios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `ruc` varchar(11) NOT NULL,
  `razon_social` varchar(100) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `departamento` varchar(50) NOT NULL,
  `provincia` varchar(50) NOT NULL,
  `distrito` varchar(50) NOT NULL,
  `rubro_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `negocios`
--

INSERT INTO `negocios` (`id`, `nombre`, `ruc`, `razon_social`, `direccion`, `telefono`, `departamento`, `provincia`, `distrito`, `rubro_id`, `usuario_id`) VALUES
(1, 'ElectroStore', '12345678901', 'ElectroStore S.A.C.', 'Av. Siempre Viva 123', '999999999', 'Lima', 'Lima', 'Miraflores', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ofertas`
--

CREATE TABLE `ofertas` (
  `id` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `tipo` enum('Oferta','2x1','Segundo Producto Barato','Paquete Rebajado','Descuento') NOT NULL,
  `stock` int(11) NOT NULL,
  `estado` enum('Activo','Inactivo') NOT NULL DEFAULT 'Activo',
  `precio_oferta` decimal(10,2) DEFAULT NULL,
  `precio_desc` decimal(10,2) DEFAULT NULL,
  `precio_2x1` decimal(10,2) DEFAULT NULL,
  `precio_paquete` decimal(10,2) DEFAULT NULL,
  `precio_seg` decimal(10,2) DEFAULT NULL,
  `descuento` decimal(5,2) DEFAULT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ofertas`
--

INSERT INTO `ofertas` (`id`, `id_producto`, `nombre`, `descripcion`, `tipo`, `stock`, `estado`, `precio_oferta`, `precio_desc`, `precio_2x1`, `precio_paquete`, `precio_seg`, `descuento`, `cantidad`) VALUES
(6, 2, 'ewewe', '323323', 'Oferta', 21, 'Activo', 31.00, NULL, NULL, NULL, NULL, NULL, 1),
(7, 2, 'rerft', 'trtrtrt', 'Oferta', 21, 'Activo', 21.00, NULL, NULL, NULL, NULL, NULL, 1),
(8, 2, 'Oferta Galaxy', 'Oferta Galaxy', 'Oferta', 10, 'Activo', 500.00, NULL, NULL, NULL, NULL, NULL, 1),
(10, 2, 'Oferta Galaxy', 'Oferta Galaxy', 'Segundo Producto Barato', 2, 'Activo', NULL, NULL, NULL, NULL, 1002.00, NULL, 2),
(11, 2, 'Oferta Galaxy', 'Oferta Galaxy', 'Descuento', 2, 'Activo', NULL, 420.00, NULL, NULL, NULL, 30.00, 1),
(12, 2, 'Oferta Galaxy', 'Oferta Galaxy', '2x1', 2, 'Activo', NULL, NULL, 1500.00, NULL, NULL, NULL, 1),
(13, 2, 'Oferta Galaxy', 'Oferta Galaxy', 'Oferta', 2, 'Activo', 333.00, NULL, NULL, NULL, NULL, NULL, 1),
(14, 2, 'Oferta Galaxy', 'Oferta Galaxy', 'Oferta', 2, 'Activo', 322.00, NULL, NULL, NULL, NULL, NULL, 1),
(15, 2, 'Oferta Galaxy', 'Oferta Galaxy', 'Oferta', 2, 'Activo', 200.00, NULL, NULL, NULL, NULL, NULL, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ofertas_detalles`
--

CREATE TABLE `ofertas_detalles` (
  `id` int(11) NOT NULL,
  `id_oferta` int(11) NOT NULL,
  `id_detalle` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ofertas_detalles`
--

INSERT INTO `ofertas_detalles` (`id`, `id_oferta`, `id_detalle`) VALUES
(6, 6, 2),
(7, 7, 3),
(8, 8, 2),
(10, 10, 3),
(11, 11, 2),
(12, 12, 2),
(13, 13, 2),
(14, 14, 2),
(15, 15, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `politicas_internas`
--

CREATE TABLE `politicas_internas` (
  `id` int(11) NOT NULL,
  `fecha_creacion` date NOT NULL,
  `fecha_implementacion` date NOT NULL,
  `nombre_politica` varchar(255) NOT NULL,
  `descripcion` text NOT NULL,
  `creado_por` varchar(50) DEFAULT 'business_owner'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `politicas_internas`
--

INSERT INTO `politicas_internas` (`id`, `fecha_creacion`, `fecha_implementacion`, `nombre_politica`, `descripcion`, `creado_por`) VALUES
(1, '2024-11-01', '2024-12-01', 'Política Interna A', 'Detalles de la política interna A', 'business_owner'),
(2, '2024-11-15', '2024-12-20', 'Política Interna B', 'Detalles de la política interna B', 'business_owner'),
(5, '2025-01-23', '2025-01-23', 'politica1', 'descripcion1', 'business_owner');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `categoria_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `descripcion`, `categoria_id`) VALUES
(2, 'Galaxy A55', 'El Samsung Galaxy A55 8GB RAM 256GB es un smartphone de alto rendimiento diseñado para ofrecer una experiencia fluida y potente. Equipado con el procesador Exynos 1480 octa-core, con velocidades de hasta 2.75 GHz, y 8GB de RAM, este dispositivo asegura un rendimiento superior para todas tus tareas. Su pantalla de 6.6 pulgadas te permite disfrutar de imágenes nítidas y vibrantes, mientras que la cámara frontal de 32 MP captura selfies de alta calidad. Con una batería de 5000 mAh, podrás usar tu teléfono durante todo el día sin problemas. Además, cuenta con lector de huella, GPS integrado y sistema operativo Android. Disponible en un elegante color lila.', 7),
(5, 'videojuego Play station 5', 'videojuego Play station 5', 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `red_social`
--

CREATE TABLE `red_social` (
  `idRed_Social` int(11) NOT NULL,
  `Nombre_red` enum('Instagram','Facebook') DEFAULT NULL,
  `Url_red` varchar(255) NOT NULL,
  `idEmpresa` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `red_social`
--

INSERT INTO `red_social` (`idRed_Social`, `Nombre_red`, `Url_red`, `idEmpresa`) VALUES
(49, 'Facebook', 'https://www.facebook.com/melbetpe/', 15),
(50, 'Instagram', 'https://www.instagram.com/melbet_peru/', 15),
(69, 'Facebook', 'https://www.facebook.com/', 25),
(70, 'Instagram', 'https://www.facebook.com/', 25),
(73, 'Facebook', 'https://www.facebook.com/', 26),
(74, 'Instagram', 'https://www.facebook.com/', 26);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_usuarios`
--

CREATE TABLE `registro_usuarios` (
  `id` int(11) NOT NULL,
  `nombre_completo` varchar(255) NOT NULL,
  `whatsapp` varchar(20) DEFAULT NULL,
  `correo` varchar(100) NOT NULL,
  `departamento` varchar(100) DEFAULT NULL,
  `provincia` varchar(100) DEFAULT NULL,
  `distrito` varchar(100) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `referencia` text DEFAULT NULL,
  `nombre_usuario` varchar(50) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `foto` varchar(255) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `estado` enum('Activo','Inactivo') NOT NULL DEFAULT 'Activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `registro_usuarios`
--

INSERT INTO `registro_usuarios` (`id`, `nombre_completo`, `whatsapp`, `correo`, `departamento`, `provincia`, `distrito`, `direccion`, `referencia`, `nombre_usuario`, `contrasena`, `foto`, `fecha`, `estado`) VALUES
(1, 'sssss', '934830424', 'correo123@gmail.com', 'Department', 'Provincia', 'Distrito', 'Direccion', 'frenteee', 'kenny', '$2b$12$bW4e003m0WRVI3fukthDlehcM8sWySCh3l4T1oOZPdcHHuG0a0qcu', 'logo_prueba.png', '2025-01-27 00:00:00', 'Activo'),
(3, '1111111111', '934830424', 'correo123@gmail.com', 'Department', 'Provincia', 'Distrito', 'Direccion', 'frenteee111', 'kenny123', '$2b$12$WQoBRuLLOJYWOwrv1lEkRe7KFAmH/QrEdPVk6kPlKzyT4O7dYtA9O', 'foto2.jpg', '2025-01-27 00:00:00', 'Activo'),
(4, 'ewewewewewe', '333333333', 'correo123@gmail.com', 'Department', 'Provincia', 'Distrito', 'Direccion', 'frenteee111', 'kenny1234', '$2b$12$j.Ae9wZpeMWGc1TePoo3xOxrRmOtqlK9bWpkvurw0dGYxZuaQ.T/a', 'logo_prueba.png', '2025-01-27 00:00:00', 'Activo'),
(5, 'EEEEEEEEEEEEEE', '999999999', 'correo123@gmail.com', 'Prueba16', 'Provincia', 'Prueba16', 'Estados Unidos', 'Torre Blanca', 'usuario1', '$2b$12$blQ.O58z191oJpYdRjzou.xlm8FQ7okrx4MANltOa7pJO3Y6nJhcS', 'logo_prueba.png', '2025-01-30 00:00:00', 'Activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rubros`
--

CREATE TABLE `rubros` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `rubros`
--

INSERT INTO `rubros` (`id`, `nombre`) VALUES
(2, 'Electrodomésticos'),
(3, 'Ropa y moda'),
(1, 'Tecnología');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `precio_oferta` decimal(10,2) DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(255) DEFAULT NULL,
  `categoria_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`id`, `nombre`, `descripcion`, `precio`, `precio_oferta`, `imagen`, `telefono`, `correo`, `categoria_id`) VALUES
(1, 'Reparación de Celulares', 'Servicio completo de reparación de celulares que incluye cambio de pantalla, batería, y resolución de problemas de software.', 150.00, 120.00, 'c39244182d864813903d45ab7ae3934c_reparacion_de_celular.jpg', '922574309', 'miguel@mail.com', 2),
(2, 'Reparación de Laptops', 'Servicio especializado en reparación de laptops, incluyendo reemplazo de pantalla, teclado, y solución de problemas de hardware y software.', 200.00, 150.00, '4b379ba53247427195f9ae5a6cf20e44_reparacion_de_laptops.jpg', '922574309', 'carlos.huaman@gmail.com', 8),
(3, 'Reparacion de videojuegos Play station', 'Reparacion de videojuegos Play station', 100.00, 100.00, '54e4aaf0c1334dd68c9abf5ba581d3b7_AEROBICOS.jpg', '976655444', 'vendedor@gmail.commm', 10),
(4, 'mantenimiento de videojuegos', 'mantenimiento de videojuegos', 200.00, 200.00, 'e9b984ef6d694af7a9eaa9022a3d59ac_almuerzo_2.jpg', '976655444', 'vendedor@gmail.commm', 10),
(5, 'mantenimiento de videojuegos2', 'mantenimiento de videojuegos', 300.00, 300.00, '573e19c156254ae39f1bb849c05c419e_5ae21cc526c97415d3213554.png', '976633323', 'vendedor2@gmail.commm', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `slider`
--

CREATE TABLE `slider` (
  `id` int(11) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `titulo` varchar(255) NOT NULL,
  `estado` enum('Activo','Inactivo') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `slider`
--

INSERT INTO `slider` (`id`, `imagen`, `titulo`, `estado`) VALUES
(3, '8d45416295204e5bbd90dc9b05e18595_proteina.jpg', 'Proteina', 'Inactivo'),
(4, '33b370f490a648959a29975691f5e43b_logo_prueba.png', 'ewewewewe', 'Activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sucursales`
--

CREATE TABLE `sucursales` (
  `ID` int(11) NOT NULL,
  `id_negocio` int(11) NOT NULL,
  `NombreSucursal` varchar(255) NOT NULL,
  `Distrito` varchar(255) NOT NULL,
  `Direccion` varchar(255) NOT NULL,
  `Correo` varchar(255) DEFAULT NULL,
  `Celular` varchar(20) DEFAULT NULL,
  `Latitud` decimal(10,8) DEFAULT NULL,
  `Longitud` decimal(11,8) DEFAULT NULL,
  `Estado` enum('Activo','Inactivo') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `sucursales`
--

INSERT INTO `sucursales` (`ID`, `id_negocio`, `NombreSucursal`, `Distrito`, `Direccion`, `Correo`, `Celular`, `Latitud`, `Longitud`, `Estado`) VALUES
(7, 1, 'Sucursal', 'Lince', 'Direccion', 'correo123@gmail.com', '11111111', 0.00000000, 0.00000000, 'Inactivo'),
(9, 1, 'Sucursal', 'Breña', 'Direccion', 'correo123@gmail.com', '99999999', 0.00000000, 0.00000000, 'Activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tamanios`
--

CREATE TABLE `tamanios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `categoria_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tamanios`
--

INSERT INTO `tamanios` (`id`, `nombre`, `categoria_id`) VALUES
(1, 'Pequeño', 1),
(2, 'Mediano', 1),
(3, 'Grande', 1),
(4, 'Chico', 2),
(5, 'Mediano', 2),
(6, 'Grande', 2),
(7, 'S', 3),
(8, 'M', 3),
(9, 'L', 3),
(10, '6 pulgadas', 7),
(11, '8 pulgadas', 7),
(12, 'Standar', 9),
(13, 'Personal', 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipos_categoria`
--

CREATE TABLE `tipos_categoria` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipos_categoria`
--

INSERT INTO `tipos_categoria` (`id`, `nombre`) VALUES
(1, 'Producto'),
(2, 'Servicio');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `tipo_usuario` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `username`, `email`, `password`, `tipo_usuario`) VALUES
(1, 'Juan Pérez', 'juanperez', 'juan@correo.com', '123', 'business_owner'),
(2, 'Carlos García', 'carlosgarcia', 'carlos@correo.com', 'hashed_password_here', 'cliente'),
(3, 'Ana Martínez', 'anamartinez', 'ana@correo.com', 'hashed_password_here', 'cliente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `fecha` datetime NOT NULL,
  `total` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `video`
--

CREATE TABLE `video` (
  `idVideo` int(11) NOT NULL,
  `idEmpresa` int(11) DEFAULT NULL,
  `Tipo` enum('YouTube','Vimeo') DEFAULT 'YouTube',
  `Url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `video`
--

INSERT INTO `video` (`idVideo`, `idEmpresa`, `Tipo`, `Url`) VALUES
(15, 15, 'YouTube', 'https://www.youtube.com/watch?v=HKp05QW6OAY'),
(16, 15, 'YouTube', 'https://www.youtube.com/watch?v=jgU-QSuTJek'),
(35, 25, 'YouTube', 'https://www.facebook.com/'),
(36, 25, 'YouTube', 'https://www.facebook.com/'),
(39, 26, 'YouTube', 'https://www.facebook.com/'),
(40, 26, 'YouTube', 'https://www.facebook.com/');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `colorv`
--
ALTER TABLE `colorv`
  ADD PRIMARY KEY (`idColor`),
  ADD KEY `idx_color_negocio` (`idEmpresa`);

--
-- Indices de la tabla `detalles`
--
ALTER TABLE `detalles`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `distritos`
--
ALTER TABLE `distritos`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `empresa`
--
ALTER TABLE `empresa`
  ADD PRIMARY KEY (`idEmpresa`);

--
-- Indices de la tabla `imagen`
--
ALTER TABLE `imagen`
  ADD PRIMARY KEY (`idImagen`),
  ADD UNIQUE KEY `idEmpresa` (`idEmpresa`,`Tipo_imagen`),
  ADD KEY `idx_imagen_negocio` (`idEmpresa`);

--
-- Indices de la tabla `negocios`
--
ALTER TABLE `negocios`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ofertas`
--
ALTER TABLE `ofertas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ofertas_detalles`
--
ALTER TABLE `ofertas_detalles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_oferta` (`id_oferta`),
  ADD KEY `id_detalle` (`id_detalle`);

--
-- Indices de la tabla `politicas_internas`
--
ALTER TABLE `politicas_internas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `red_social`
--
ALTER TABLE `red_social`
  ADD PRIMARY KEY (`idRed_Social`),
  ADD UNIQUE KEY `idEmpresa` (`idEmpresa`,`Nombre_red`),
  ADD KEY `idx_redes_negocio` (`idEmpresa`);

--
-- Indices de la tabla `registro_usuarios`
--
ALTER TABLE `registro_usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre_usuario` (`nombre_usuario`);

--
-- Indices de la tabla `slider`
--
ALTER TABLE `slider`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `sucursales`
--
ALTER TABLE `sucursales`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `id_negocio` (`id_negocio`);

--
-- Indices de la tabla `video`
--
ALTER TABLE `video`
  ADD PRIMARY KEY (`idVideo`),
  ADD KEY `idEmpresa` (`idEmpresa`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `colorv`
--
ALTER TABLE `colorv`
  MODIFY `idColor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `detalles`
--
ALTER TABLE `detalles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `distritos`
--
ALTER TABLE `distritos`
  MODIFY `ID` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT de la tabla `empresa`
--
ALTER TABLE `empresa`
  MODIFY `idEmpresa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `imagen`
--
ALTER TABLE `imagen`
  MODIFY `idImagen` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `ofertas`
--
ALTER TABLE `ofertas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `ofertas_detalles`
--
ALTER TABLE `ofertas_detalles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `politicas_internas`
--
ALTER TABLE `politicas_internas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `red_social`
--
ALTER TABLE `red_social`
  MODIFY `idRed_Social` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;

--
-- AUTO_INCREMENT de la tabla `registro_usuarios`
--
ALTER TABLE `registro_usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `slider`
--
ALTER TABLE `slider`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `sucursales`
--
ALTER TABLE `sucursales`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `video`
--
ALTER TABLE `video`
  MODIFY `idVideo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `colorv`
--
ALTER TABLE `colorv`
  ADD CONSTRAINT `colorv_ibfk_1` FOREIGN KEY (`idEmpresa`) REFERENCES `empresa` (`idEmpresa`) ON DELETE CASCADE;

--
-- Filtros para la tabla `imagen`
--
ALTER TABLE `imagen`
  ADD CONSTRAINT `imagen_ibfk_1` FOREIGN KEY (`idEmpresa`) REFERENCES `empresa` (`idEmpresa`) ON DELETE CASCADE;

--
-- Filtros para la tabla `ofertas_detalles`
--
ALTER TABLE `ofertas_detalles`
  ADD CONSTRAINT `fk_ofertas_detalles_detalle` FOREIGN KEY (`id_detalle`) REFERENCES `detalles` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_ofertas_detalles_oferta` FOREIGN KEY (`id_oferta`) REFERENCES `ofertas` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `red_social`
--
ALTER TABLE `red_social`
  ADD CONSTRAINT `red_social_ibfk_1` FOREIGN KEY (`idEmpresa`) REFERENCES `empresa` (`idEmpresa`) ON DELETE CASCADE;

--
-- Filtros para la tabla `sucursales`
--
ALTER TABLE `sucursales`
  ADD CONSTRAINT `sucursales_ibfk_1` FOREIGN KEY (`id_negocio`) REFERENCES `negocios` (`id`);

--
-- Filtros para la tabla `video`
--
ALTER TABLE `video`
  ADD CONSTRAINT `video_ibfk_1` FOREIGN KEY (`idEmpresa`) REFERENCES `empresa` (`idEmpresa`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
