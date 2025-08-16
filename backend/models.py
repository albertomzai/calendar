from datetime import datetime

from . import db

class Evento(db.Model):
    """Modelo que representa un evento en la base de datos."""

    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.Text)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    color = db.Column(db.String)

    def to_dict(self):
        """Serializa el objeto Evento a un diccionario JSON."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio.isoformat(),
            'fecha_fin': self.fecha_fin.isoformat(),
            'color': self.color
        }