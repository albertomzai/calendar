from . import db

class Evento(db.Model):
    """Modelo SQLAlchemy que representa un evento del calendario."""

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, default='')
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    color = db.Column(db.String(20), default='#FFFFFF')

    def to_dict(self):
        """Serializa el objeto a un diccionario."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio.isoformat(),
            'fecha_fin': self.fecha_fin.isoformat(),
            'color': self.color
        }