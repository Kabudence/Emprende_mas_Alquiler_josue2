from app import create_app, db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Rubro, TipoCategoria, Categoria, CategoriaFeedback, Color, Producto, Tamanio, ProductoDetalle, Usuario, Negocio, Servicio, Feedback, Venta, PoliticaInterna,Slider
from app.models import colorv,Imagen,RedSocial, Video, Empresa 
from config import Config

app = create_app()

# Crear o recrear la base de datos usando variables globales
with app.app_context():
    # Conexión sin base de datos para eliminarla primero
    engine = create_engine(f"mysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}")

    # Eliminar y crear la base de datos
    conn = engine.raw_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {Config.MYSQL_DB}")
        cursor.execute(f"CREATE DATABASE {Config.MYSQL_DB}")
        conn.commit()
        print(f"Base de datos '{Config.MYSQL_DB}' eliminada y creada con éxito.")
    finally:
        conn.close()

    # Conectarse a la nueva base de datos
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear tablas a partir de los modelos de SQLAlchemy
    db.create_all()
    print("Tablas creadas con éxito.")

    # Insertar datos en la base de datos
    try:
        # Insertar rubros
        rubros = [
            Rubro(id=1, nombre='Tecnología'),
            Rubro(id=2, nombre='Electrodomésticos'),
            Rubro(id=3, nombre='Ropa y moda')
        ]
        session.add_all(rubros)

        # Insertar tipos de categoría
        tipos_categoria = [
            TipoCategoria(id=1, nombre='Producto'),
            TipoCategoria(id=2, nombre='Servicio')
        ]
        session.add_all(tipos_categoria)

        # Insertar categorías
        categorias = [
            Categoria(id=1, nombre='Laptops', rubro_id=1, tipo_id=1),
            Categoria(id=2, nombre='Soporte Técnico', rubro_id=1, tipo_id=2),
            Categoria(id=3, nombre='Refrigeradores', rubro_id=2, tipo_id=1),
            Categoria(id=4, nombre='Instalación de Electrodomésticos', rubro_id=2, tipo_id=2),
            Categoria(id=5, nombre='Ropa de Mujer', rubro_id=3, tipo_id=1),
            Categoria(id=6, nombre='Asesoría de Estilo', rubro_id=3, tipo_id=2),
            Categoria(id=7, nombre='Celular', rubro_id=1, tipo_id=1),
            Categoria(id=8, nombre='Reparación de laptop', rubro_id=1, tipo_id=2)
        ]
        session.add_all(categorias)

        # Insertar categorías de feedback
        categorias_feedback = [
            CategoriaFeedback(id=1, nombre='comentario'),
            CategoriaFeedback(id=2, nombre='reconocimiento')
        ]
        session.add_all(categorias_feedback)

        # Insertar colores
        colores = [
            Color(id=1, nombre='Rojo', hexadecimal='#FF0000'),
            Color(id=2, nombre='Azul', hexadecimal='#0000FF'),
            Color(id=3, nombre='Verde', hexadecimal='#00FF00'),
            Color(id=4, nombre='Negro', hexadecimal='#000000'),
            Color(id=5, nombre='Blanco', hexadecimal='#FFFFFF'),
            Color(id=6, nombre='Amarillo', hexadecimal='#FFFF00'),
            Color(id=7, nombre='Lila', hexadecimal='#E04CE0')
        ]
        session.add_all(colores)

        # Insertar productos
        productos = [
            Producto(id=2, nombre='Galaxy A55', descripcion='El Samsung Galaxy A55 8GB RAM 256GB es un smartphone de alto rendimiento diseñado para ofrecer una experiencia fluida y potente. Equipado con el procesador Exynos 1480 octa-core, con velocidades de hasta 2.75 GHz, y 8GB de RAM, este dispositivo asegura un rendimiento superior para todas tus tareas. Su pantalla de 6.6 pulgadas te permite disfrutar de imágenes nítidas y vibrantes, mientras que la cámara frontal de 32 MP captura selfies de alta calidad. Con una batería de 5000 mAh, podrás usar tu teléfono durante todo el día sin problemas. Además, cuenta con lector de huella, GPS integrado y sistema operativo Android. Disponible en un elegante color lila.', categoria_id=7)
        ]
        session.add_all(productos)

        # Insertar tamaños
        tamanios = [
            Tamanio(id=1, nombre='Pequeño', categoria_id=1),
            Tamanio(id=2, nombre='Mediano', categoria_id=1),
            Tamanio(id=3, nombre='Grande', categoria_id=1),
            Tamanio(id=4, nombre='Chico', categoria_id=2),
            Tamanio(id=5, nombre='Mediano', categoria_id=2),
            Tamanio(id=6, nombre='Grande', categoria_id=2),
            Tamanio(id=7, nombre='S', categoria_id=3),
            Tamanio(id=8, nombre='M', categoria_id=3),
            Tamanio(id=9, nombre='L', categoria_id=3),
            Tamanio(id=10, nombre='6 pulgadas', categoria_id=7)
        ]
        session.add_all(tamanios)

        # Insertar detalles del producto
        detalles = [
            ProductoDetalle(id=2, color_id=4, producto_id=2, tamanio_id=10, stock=50, imagen='ddb211d9ec6b468c85ebb88be89845df_galaxy_negro.png', precio=600.00, capacidad='64gb de almacenamiento'),
            ProductoDetalle(id=3, color_id=7, producto_id=2, tamanio_id=10, stock=40, imagen='6c1dc4c14d4942b98f4aee49bdfb4f2e_galaxy_lila.png', precio=700.00, capacidad='128gb de almacenamiento')
        ]
        session.add_all(detalles)

        # Insertar usuarios
        usuarios = [
            Usuario(id=1, nombre='Juan Pérez', username='juanperez', email='juan@correo.com', password='hashed_password_here', tipo_usuario='business_owner'),
            Usuario(id=2, nombre='Carlos García', username='carlosgarcia', email='carlos@correo.com', password='hashed_password_here', tipo_usuario='cliente'),
            Usuario(id=3, nombre='Ana Martínez', username='anamartinez', email='ana@correo.com', password='hashed_password_here', tipo_usuario='cliente')
        ]
        session.add_all(usuarios)

        # Insertar negocios
        negocios = [
            Negocio(id=1, nombre='ElectroStore', ruc='12345678901', razon_social='ElectroStore S.A.C.', direccion='Av. Siempre Viva 123', telefono='999999999', departamento='Lima', provincia='Lima', distrito='Miraflores', rubro_id=1, usuario_id=1)
        ]
        session.add_all(negocios)

        # Insertar servicios
        servicios = [
            Servicio(id=1, nombre='Reparación de Celulares', descripcion='Servicio completo de reparación de celulares que incluye cambio de pantalla, batería, y resolución de problemas de software.', precio=150.00, precio_oferta=120.00, imagen='c39244182d864813903d45ab7ae3934c_reparacion_de_celular.jpg', telefono='922574309', correo='miguel@mail.com', categoria_id=2),
            Servicio(id=2, nombre='Reparación de Laptops', descripcion='Servicio especializado en reparación de laptops, incluyendo reemplazo de pantalla, teclado, y solución de problemas de hardware y software.', precio=200.00, precio_oferta=150.00, imagen='4b379ba53247427195f9ae5a6cf20e44_reparacion_de_laptops.jpg', telefono='922574309', correo='carlos.huaman@gmail.com', categoria_id=8)
        ]
        session.add_all(servicios)

        # Insertar feedbacks
        feedbacks = [
            Feedback(id=1, asunto='Producto llegó tarde', descripcion='El producto llegó mucho más tarde de lo esperado, lo cual causó inconvenientes.', imagen1='pantalla_rota.jpg', imagen2='producto_dañado.jpg', categoria_id=2, usuario_id=2)
        ]
        session.add_all(feedbacks)

        # Insertar ventas
        ventas = [
            Venta(id=1, usuario_id=1, fecha='2024-12-16 09:00:00', total=850.00)
        ]
        politicas_internas = [
            PoliticaInterna(id=1, fecha_creacion = '2024-11-01', fecha_implementacion='2024-12-01', nombre_politica = 'Politica Interna A', descripcion = 'Detalle de politica A'),
            PoliticaInterna(id=2, fecha_creacion = '2024-11-15', fecha_implementacion='2024-12-20', nombre_politica = 'Politica Interna B', descripcion = 'Detalle de politica B')
        ]
        session.add_all(politicas_internas)
        slider = [
            Slider(id = 9,imagen = '../img/677bd329b81127.13251022.jpg',titulo = 'Instagram', estado = 'Activo')
        ]
        session.add_all(slider)
        
        Colorv = [
            colorv(idColor = 19, nombre_principal = '#264ff2',nombre_hexadecimal_principal = '#264FF2', idEmpresa = 15, nombre_secundario = '#ef1f72', nombre_hexadecimal_secundario = '#EF1F72')
        ]
        session.add_all(Colorv)
        Imagenes = [
            
            Imagen(idImagen = 17, tipo_imagen = 'Logo', filename = 'images.jpeg', idEmpresa = 15),
            Imagen(idImagen = 18, tipo_imagen = 'Icono',filename = 'images.jpeg', idEmpresa = 15)
        ]
        session.add_all(Imagenes)
        redsocial =  [
            RedSocial(idRed_Social = 49, nombre_red = 'Facebook', url_red = 'https://www.facebook.com/melbetpe/', idEmpresa = 15),
            RedSocial(idRed_Social = 50, nombre_red = 'Instagram', url_red = 'https://www.instagram.com/melbet_peru/', idEmpresa = 15)
        ]
        session.add_all(redsocial)
        video = [
            Video(idVideo = 15, idEmpresa = 15 , tipo = 'Youtube', url = 'https://www.youtube.com/watch?v=HKp05QW6OAY'),
            Video(idVideo = 16, idEmpresa = 15 , tipo = 'Youtube', url = 'https://www.youtube.com/watch?v=jgU-QSuTJek')
        ]
        session.add_all(video)
        empresa = [
            Empresa(idEmpresa = 15, nombre = 'ConsigueVentas ', mision = ' Conseguir muchas ventas para navidad', vision = 'A', objetivos = 'A')
            
        ]
        session.add_all(empresa)
        
        
        session.commit()
        print("Datos insertados con éxito.")
    except Exception as e:
        session.rollback()
        print(f"Error insertando los datos: {e}")
    finally:
        session.close()
