# Modelo de datos para los eventos.
# Se define una tabla "evento" con los campos requeridos.

from datetime import datetime
from app import sql

class Evento(sql.Model):
    """Representa un evento en el calendario."""

    __tablename__ = 'evento'

    id = sql.Column(sql.Integer, primary_key=True)
    titulo = sql.Column(sql.String(200), nullable=False)
    descripcion = sql.Column(sql.Text, default='')
    fecha_inicio = sql.Column(sql.DateTime, nullable=False)
    fecha_fin = sql.Column(sql.DateTime, nullable=False)
    color = sql.Column(sql.String(20), default='#3788d8')  # Default blue

    def to_dict(self):
        """Serializa el objeto a un diccionario JSON."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio.isoformat(),
            'fecha_fin': self.fecha_fin.isoformat(),
            'color': self.color
        }
