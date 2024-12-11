from flask_login import UserMixin
from app.database import db

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False)
    feedbacks = db.relationship('Feedback', backref='usuario', lazy=True)
    negocios = db.relationship('Negocio', backref='usuario', lazy=True)

class Rubro(db.Model):
    __tablename__ = 'rubros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    negocios = db.relationship('Negocio', backref='rubro', lazy=True)
    categorias = db.relationship('Categoria', backref='rubro', lazy=True)

class Negocio(db.Model):
    __tablename__ = 'negocios'
    id = db.Column(db.Integer, primary_key=True)
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

class Tamanio(db.Model):
    __tablename__ = 'tamanios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    detalles = db.relationship('ProductoDetalle', backref='tamanio', lazy=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    detalles = db.relationship('ProductoDetalle', backref='producto', lazy=True)

class Color(db.Model):
    __tablename__ = 'colores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    hexadecimal = db.Column(db.String(7), nullable=False, unique=True)
    detalles = db.relationship('ProductoDetalle', backref='color', lazy=True)

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

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)

class DetalleVenta(db.Model):
    __tablename__ = 'detalles_venta'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    asunto = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    imagen1 = db.Column(db.String(255), nullable=True)
    imagen2 = db.Column(db.String(255), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias_feedback.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

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
    telefono = db.Column(db.String(20), nullable=True)
    correo = db.Column(db.String(255), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
