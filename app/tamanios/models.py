class Tamanio(db.Model):
    __tablename__ = 'tamanios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

    categoria = db.relationship('Categoria', backref='tamanios')
