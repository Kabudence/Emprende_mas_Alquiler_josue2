from datetime import datetime
from enum import Enum

from flask_login import UserMixin
from sqlalchemy import CheckConstraint

from app.database import db

servicio_local = db.Table(
    'servicio_local',
    db.Column('servicio_id', db.Integer, db.ForeignKey('servicio_completo.id'), primary_key=True),
    db.Column('local_id', db.Integer, db.ForeignKey('locales.id'), primary_key=True)
)


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    id_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id'), nullable=False)
    dni = db.Column(db.String(8), unique=True, nullable=False)
    foto_dni_frontal = db.Column(db.String(255), nullable=True)
    foto_dni_posterior = db.Column(db.String(255), nullable=True)
    celular = db.Column(db.String(15), nullable=True)
    user_inviter = db.Column(db.Integer, nullable=True)
    role = db.Column(db.String(20), nullable=False, default="COMPRADOR")

    __table_args__ = (
        CheckConstraint(
            "role IN ('AFILIADO', 'COMPRADOR')",
            name="ck_usuario_role_valido"
        ),
    )

    tipo_usuario = db.relationship('TipoUsuario', back_populates='usuarios')
    feedbacks = db.relationship('Feedback', backref='usuario', lazy=True)
    negocios = db.relationship('Negocio', backref='usuario', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())



from app import db


class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(255), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=True)
    correo = db.Column(db.String(100), nullable=False)
    departamento = db.Column(db.String(100), nullable=True)
    provincia = db.Column(db.String(100), nullable=True)
    distrito = db.Column(db.String(100), nullable=True)
    direccion = db.Column(db.Text, nullable=True)
    referencia = db.Column(db.Text, nullable=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    foto = db.Column(db.String(255), nullable=True)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    estado = db.Column(db.Enum('Activo', 'Inactivo'), nullable=False, default='Activo')

    # Relación con TipoCliente
    tipo_cliente_id = db.Column(db.Integer, db.ForeignKey('tipo_cliente.id'), nullable=True)
    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)


class TipoCliente(db.Model):
    __tablename__ = 'tipo_cliente'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(50), nullable=False, unique=True)

    clientes = db.relationship('Cliente', backref='tipo_cliente', lazy=True)


class Publicacion(db.Model):
    __tablename__ = 'publicaciones'

    id = db.Column(db.Integer, primary_key=True)
    fecha_publicacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_compra = db.Column(db.Date, nullable=False)
    nombre_publicacion = db.Column(db.String(255), nullable=False)
    nombre_cliente = db.Column(db.String(255), nullable=False)  # NUEVO
    productos = db.Column(db.Text, nullable=True)
    foto_uno = db.Column(db.String(255), nullable=False)
    foto_dos = db.Column(db.String(255), nullable=True)
    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)
    negocio = db.relationship('Negocio', backref='publicaciones_negocio')


class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.String(255), nullable=False)
    usuarios = db.relationship('Usuario', back_populates='tipo_usuario')


class Rubro(db.Model):
    __tablename__ = 'rubros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    estado = db.Column(db.String(10), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    negocios = db.relationship('Negocio', backref='rubro', lazy=True)
    categorias = db.relationship('Categoria', backref='rubro', lazy=True)
    descripcion = db.Column(db.Text, default='Sin descripción')


class Negocio(db.Model):
    __tablename__ = 'negocios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    ruc = db.Column(db.String(11), unique=True, nullable=False)
    razon_social = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    departamento = db.Column(db.String(50), nullable=False)
    provincia = db.Column(db.String(50), nullable=False)
    distrito = db.Column(db.String(50), nullable=False)
    rubro_id = db.Column(db.Integer, db.ForeignKey('rubros.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    empresa = db.relationship('Empresa', back_populates='negocio', uselist=False)
    imagenes = db.relationship('Imagen', backref='negocio', lazy=True)
    colorv = db.relationship('colorv', back_populates='negocio', uselist=False)
    redes_sociales = db.relationship('RedSocial', backref='negocio', lazy=True)
    videos = db.relationship('Video', backref='negocio', lazy=True)
    tipo_modelo_id = db.Column(db.Integer, db.ForeignKey('tipo_modelo.id'))
    membresia_id = db.Column(db.Integer, db.ForeignKey('tipo_membresia.id'))
    fecha_registro = db.Column(db.DateTime)
    fecha_fin_alquiler = db.Column(db.DateTime)
    bloqueado = db.Column(db.Boolean, default=False)
    tipo_modelo = db.relationship('TipoModelo', backref='negocios')
    membresia = db.relationship('TipoMembresia', backref='negocios')
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    categoria = db.relationship('Categoria', back_populates='negocios', lazy=True)


class TipoCategoria(db.Model):
    __tablename__ = 'tipos_categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    categorias = db.relationship('Categoria', backref='tipo_categorias', lazy=True)


class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    rubro_id = db.Column(db.Integer, db.ForeignKey('rubros.id'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_categoria.id'), nullable=False)
    productos = db.relationship('Producto', backref='categoria', lazy=True)
    tamanios = db.relationship('Tamanio', backref='categoria', lazy=True)
    servicios = db.relationship('Servicio', backref='categoria', lazy=True)
    negocios = db.relationship('Negocio', back_populates='categoria', lazy=True)
    id_negocio = db.Column(db.Integer, nullable=False)  # <--- AGREGA ESTA LÍNEA


class Tamanio(db.Model):
    __tablename__ = 'tamanios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    detalles = db.relationship('ProductoDetalle', back_populates='tamanio')


class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    marca = db.Column(db.String(100), nullable=True)
    modelo = db.Column(db.String(100), nullable=True)
    dimensiones = db.Column(db.String(100), nullable=True)
    contenido_caja = db.Column(db.Text, nullable=True)
    garantia = db.Column(db.Integer, nullable=True)  # Puedes ajustarlo según sea necesario (meses o años)
    pais_origen_procedencia = db.Column(db.String(100))
    condicion_producto = db.Column(db.String(100))
    link_producto = db.Column(db.String(255), nullable=True)
    video1 = db.Column(db.String(255), nullable=True)
    video2 = db.Column(db.String(255), nullable=True)
    detalles = db.relationship('ProductoDetalle', backref='producto', lazy=True)
    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)


class Color(db.Model):
    __tablename__ = 'colores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    hexadecimal = db.Column(db.String(7), nullable=False, unique=True)
    detalles = db.relationship('ProductoDetalle', back_populates='color')
    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)
    negocio = db.relationship('Negocio', backref='colores')
    __table_args__ = (
        db.UniqueConstraint('nombre', 'id_negocio', name='uq_color_negocio'),
    )


class ProductoDetalle(db.Model):
    __tablename__ = 'detalles'
    id = db.Column(db.Integer, primary_key=True)
    color_id = db.Column(db.Integer, db.ForeignKey('colores.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    tamanio_id = db.Column(db.Integer, db.ForeignKey('tamanios.id'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    capacidad = db.Column(db.String(100), nullable=True)
    tamanio = db.relationship('Tamanio', back_populates='detalles')

    tamanio = db.relationship('Tamanio', back_populates='detalles')
    color = db.relationship('Color', back_populates='detalles')


class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)
    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)
    negocio = db.relationship('Negocio', backref='ventas_negocio')


class DetalleVenta(db.Model):
    __tablename__ = 'detalles_venta'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)
    negocio = db.relationship('Negocio', backref='detalles_venta_negocio')


class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    asunto = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    imagen1 = db.Column(db.String(255), nullable=True)
    imagen2 = db.Column(db.String(255), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias_feedback.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_negocio = db.Column(db.Integer, db.ForeignKey('negocio.id'))


class CategoriaFeedback(db.Model):
    __tablename__ = 'categorias_feedback'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    feedbacks = db.relationship('Feedback', backref='categoria_feedback', lazy=True)


class Servicio(db.Model):
    __tablename__ = 'servicios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    precio_oferta = db.Column(db.Numeric(10, 2), nullable=True)
    imagen = db.Column(db.String(255), nullable=True)
    video = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    correo = db.Column(db.String(255), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)
    tipo_servicio_id = db.Column(db.Integer, db.ForeignKey('tipo_servicio.id_tipo_servicio'), nullable=True)
    negocio = db.relationship('Negocio', backref='servicios_negocio')
    tipo_servicio = db.relationship('TipoServicio', backref=db.backref('servicios', lazy='dynamic'))


class PoliticaInterna(db.Model):
    __tablename__ = 'politicas_internas'
    id = db.Column(db.Integer, primary_key=True)
    fecha_creacion = db.Column(db.Date, nullable=False)
    fecha_implementacion = db.Column(db.Date, nullable=False)
    nombre_politica = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)
    negocio = db.relationship('Negocio', backref='politicas_negocio')


class Slider(db.Model):
    __tablename__ = 'slider'
    id = db.Column(db.Integer, primary_key=True)
    imagen = db.Column(db.String(255), nullable=True)
    titulo = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Enum('Activo', 'Inactivo', name='estado_enum'),
                       nullable=False, default='Activo')
    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)
    negocio = db.relationship('Negocio', backref='sliders_negocio')


class colorv(db.Model):
    __tablename__ = 'colorv'
    idColor = db.Column(db.Integer, primary_key=True)
    Nombre_principal = db.Column(db.String(45))
    Nombre_hexadecimal_principal = db.Column(db.String(7))
    Nombre_secundario = db.Column(db.String(45))
    Nombre_hexadecimal_secundario = db.Column(db.String(7))
    idNegocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=True)
    negocio = db.relationship('Negocio', back_populates='colorv', overlaps="colores,empresa_color")


# Modelo para imagen
class Imagen(db.Model):
    __tablename__ = 'imagen'
    idImagen = db.Column(db.Integer, primary_key=True)
    tipo_imagen = db.Column(db.Enum('logo', 'icono'))
    filename = db.Column(db.String(255))
    idNegocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=True)


# Modelo para red social
class RedSocial(db.Model):
    __tablename__ = 'red_social'
    idRed_Social = db.Column(db.Integer, primary_key=True)
    nombre_red = db.Column(db.Enum('Instagram', 'Facebook'), nullable=True)
    url_red = db.Column(db.String(255), nullable=False)
    idNegocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=True)


# Modelo para video
class Video(db.Model):
    __tablename__ = 'video'
    idVideo = db.Column(db.Integer, primary_key=True)
    idNegocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=True)
    tipo = db.Column(db.Enum('YouTube', 'Vimeo'), default='YouTube', nullable=False)
    url = db.Column(db.String(255), nullable=True)


class Empresa(db.Model):
    __tablename__ = 'empresa'
    idEmpresa = db.Column(db.Integer, primary_key=True)
    Mision = db.Column(db.Text, nullable=True)  # Cambiado a Text y nullable
    Vision = db.Column(db.Text, nullable=True)
    Objetivos = db.Column(db.Text)
    idNegocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)

    # Relaciones usando nombres de clase como strings
    negocio = db.relationship('Negocio', back_populates='empresa')
    imagenes = db.relationship(
        'Imagen',
        primaryjoin='Empresa.idNegocio == foreign(Imagen.idNegocio)',
        viewonly=True,  # Si solo quieres lectura
        lazy=True
    )
    colores = db.relationship('colorv',
                              backref='empresa_color',
                              foreign_keys='colorv.idNegocio',
                              primaryjoin='Empresa.idNegocio == colorv.idNegocio',
                              uselist=False,
                              overlaps="colorv,negocio")

    redes_sociales = db.relationship(
        'RedSocial',
        secondary='negocios',  # Tabla intermedia
        primaryjoin='Empresa.idNegocio == Negocio.id',
        secondaryjoin='Negocio.id == RedSocial.idNegocio',
        viewonly=True,
        lazy=True
    )

    videos = db.relationship(
        'Video',
        primaryjoin="and_(Empresa.idNegocio==Video.idNegocio, "
                    "foreign(Video.idNegocio)==Empresa.idNegocio)",
        viewonly=True,
        lazy=True
    )


class Departamento(db.Model):
    __tablename__ = 'departamentos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    # Relación con envíos, usando back_populates
    envios = db.relationship('Envio', back_populates='departamento', lazy=True)


class Provincia(db.Model):
    __tablename__ = 'provincias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=False)

    # Relación con envíos
    envios = db.relationship('Envio', back_populates='provincia', lazy=True)


class Envio(db.Model):
    __tablename__ = 'envios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    sucursal_id = db.Column(db.Integer, db.ForeignKey('sucursales.ID'), nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=False)
    provincia_id = db.Column(db.Integer, db.ForeignKey('provincias.id'), nullable=False)
    distrito_id = db.Column(db.BigInteger, db.ForeignKey('distritos.ID'), nullable=False)
    costo = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.String(10), nullable=False, default='activo')

    # Relaciones definidas con back_populates para evitar conflictos
    departamento = db.relationship('Departamento', back_populates='envios', lazy=True)
    provincia = db.relationship('Provincia', back_populates='envios', lazy=True)
    distrito = db.relationship('Distrito', back_populates='envios', lazy=True)
    sucursal = db.relationship('Sucursal', back_populates='envios', lazy=True)

    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)
    negocio = db.relationship('Negocio', backref='envios')


class Distrito(db.Model):
    __tablename__ = 'distritos'
    ID = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(255), nullable=False)
    provincia_id = db.Column(db.Integer, nullable=False)  # Asegúrate de que este campo sea el correcto

    # Relación con envíos
    envios = db.relationship('Envio', back_populates='distrito', lazy=True)


class Sucursal(db.Model):
    __tablename__ = "sucursales"

    ID = db.Column("ID", db.Integer, primary_key=True)  # Coincide con `ID` en la DB
    id_negocio = db.Column("id_negocio", db.Integer, db.ForeignKey("negocios.id"))  # Clave foránea
    NombreSucursal = db.Column("NombreSucursal", db.String(255))  # PascalCase
    Distrito = db.Column("Distrito", db.String(255))
    Direccion = db.Column("Direccion", db.String(255))
    Correo = db.Column("Correo", db.String(255))
    Celular = db.Column("Celular", db.String(20))
    Latitud = db.Column("Latitud", db.Numeric(10, 8))
    Longitud = db.Column("Longitud", db.Numeric(11, 8))
    Estado = db.Column("Estado", db.Enum("Activo", "Inactivo"))
    envios = db.relationship("Envio", back_populates="sucursal")


class OrdenProducto(db.Model):
    __tablename__ = 'orden_producto'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('ordenes.id'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    tamaño = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    orden = db.relationship('Orden', backref=db.backref('productos', lazy=True))

    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)
    negocio = db.relationship('Negocio', backref='ordenes_producto_negocio')

    @db.validates('precio', 'cantidad')
    def validate_total(self, key, value):
        """ Valida el precio y cantidad, y actualiza el total. """
        if key in ['precio', 'cantidad']:
            if key == 'precio' and value < 0:
                raise ValueError("El precio no puede ser negativo")
            if key == 'cantidad' and value <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")

            # Si ambos valores están disponibles, recalcular total
            if self.precio is not None and self.cantidad is not None:
                self.total = self.precio * self.cantidad
        return value


class Orden(db.Model):
    __tablename__ = 'ordenes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orden_client_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    forma_pago = db.Column(db.Enum('Tarjeta', 'Yape', 'En Local'), nullable=False)
    estado = db.Column(db.Enum('Pagado', 'Pendiente', 'Por pagar'), nullable=False)
    costo_envio = db.Column(db.Numeric(10, 2), nullable=True)
    comision_culqui = db.Column(db.Numeric(10, 2), nullable=True)
    subtotal = db.Column(db.Numeric(10, 2), nullable=True)
    total = db.Column(db.Numeric(10, 2), nullable=True)
    sucursal_id = db.Column(db.Integer, db.ForeignKey('sucursales.ID'), nullable=False)
    distrito = db.Column(db.String(255), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    cliente = db.relationship('Cliente', backref='ordenes', lazy=True)
    sucursal = db.relationship('Sucursal', backref='ordenes', lazy=True)
    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)
    negocio = db.relationship('Negocio', backref='ordenes_negocio')


class TipoMembresia(db.Model):
    __tablename__ = 'tipo_membresia'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)
    cant_dias = db.Column(db.Integer)


class TipoModelo(db.Model):
    __tablename__ = 'tipo_modelo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)

class TipoOfertaEnum(str, Enum):
    dos_por_uno = '2x1'
    descuento  = 'Descuento'
    oferta     = 'Oferta'

class ServicioCompleto(db.Model):
    __tablename__ = 'servicio_completo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo_publicacion = db.Column(db.String(150), nullable=False)
    estado = db.Column(db.Enum('Activo', 'Inactivo', name='estado_enum'), nullable=False, default='Activo')
    imagen = db.Column(db.String(255), nullable=True)

    subtitulo1 = db.Column(db.Text, nullable=True)
    descripcion1 = db.Column(db.Text, nullable=True)
    subtitulo2 = db.Column(db.Text, nullable=True)
    descripcion2 = db.Column(db.Text, nullable=True)
    subtitulo3 = db.Column(db.Text, nullable=True)
    descripcion3 = db.Column(db.Text, nullable=True)

    media1 = db.Column(db.String(255), nullable=True)
    media2 = db.Column(db.String(255), nullable=True)

    precio = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    precio_oferta = db.Column(db.Numeric(10, 2), nullable=True)

    tipo_oferta = db.Column(
        db.Enum(*[e.value for e in TipoOfertaEnum], name='tipo_oferta_enum'),
        nullable=False,
        default=TipoOfertaEnum.oferta.value
    )
    en_venta = db.Column(db.Boolean, nullable=False, default=True)

    tipo_servicio_id = db.Column(db.Integer, db.ForeignKey('tipo_servicio.id_tipo_servicio'), nullable=True)
    tipo_servicio = db.relationship('TipoServicio', backref=db.backref('servicios_completos', lazy='dynamic'))

    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)
    negocio = db.relationship('Negocio', backref='servicios_completos')
    precio_promocion = db.Column(db.Integer, nullable=True)
    tiempo_duracion = db.Column(db.String(50), nullable=True)

    locales = db.relationship(
        'Local',
        secondary=servicio_local,
        backref=db.backref('servicios_completos', lazy='dynamic')
    )


class TipoServicio(db.Model):
    __tablename__ = 'tipo_servicio'

    id_tipo_servicio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_servicio = db.Column(db.String(50), nullable=False)


class Local(db.Model):
    __tablename__ = 'locales'

    id = db.Column(db.Integer, primary_key=True)
    latitud = db.Column(db.String(50), nullable=False)
    longitud = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuario = db.relationship('Usuario', backref='locales')


ofertas_detalles = db.Table(
    'ofertas_detalles',
    db.Column('id_oferta', db.Integer, db.ForeignKey('ofertas.id'), primary_key=True),
    db.Column('id_detalle', db.Integer, db.ForeignKey('detalles.id'), primary_key=True)
)


class Oferta(db.Model):
    __tablename__ = 'ofertas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer)
    estado = db.Column(db.String(10), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'))
    precio_oferta = db.Column(db.Numeric(10, 2))
    precio_2x1 = db.Column(db.Numeric(10, 2))
    descuento = db.Column(db.Numeric(5, 2))
    precio_desc = db.Column(db.Numeric(10, 2))
    cantidad = db.Column(db.Integer)
    precio_paquete = db.Column(db.Numeric(10, 2))
    precio_seg = db.Column(db.Numeric(10, 2))
    foto_producto = db.Column(db.String(255))
    id_negocio = db.Column(db.Integer, db.ForeignKey('negocios.id'), nullable=False)

    detalles = db.relationship('ProductoDetalle', secondary=ofertas_detalles, backref='ofertas')





