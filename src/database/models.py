"""Modelos de datos para la aplicación."""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class EstadoConciliacion(enum.Enum):
    """Estados posibles de una conciliación."""
    PENDIENTE = "pendiente"
    CONCILIADA = "conciliada"
    PARCIAL = "parcial"
    DISCREPANCIA = "discrepancia"
    MANUAL = "manual"


class EstadoPago(enum.Enum):
    """Estados posibles de un pago."""
    PENDIENTE = "pendiente"
    PROCESADO = "procesado"
    CONFIRMADO = "confirmado"
    RECHAZADO = "rechazado"
    DEVUELTO = "devuelto"


class TransaccionBancaria(Base):
    """Modelo de transacción bancaria."""
    __tablename__ = "transacciones_bancarias"
    
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    monto = Column(Float)
    concepto = Column(String(500))
    tipo = Column(String(50))  # Débito/Crédito
    referencia = Column(String(100))
    numero_transaccion = Column(String(100), unique=True)
    banco = Column(String(100))
    cuenta = Column(String(100))
    fecha_procesamiento = Column(DateTime, default=datetime.now)
    estado = Column(Enum(EstadoConciliacion), default=EstadoConciliacion.PENDIENTE)
    
    # Relaciones
    conciliaciones = relationship("Conciliacion", back_populates="transaccion_bancaria")
    pagos = relationship("Pago", back_populates="transaccion")
    
    def __repr__(self):
        return f"<TransaccionBancaria {self.numero_transaccion}: {self.monto}>"


class RegistroSII(Base):
    """Modelo de registro del SII."""
    __tablename__ = "registros_sii"
    
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    rut = Column(String(20))
    razon_social = Column(String(200))
    tipo_documento = Column(String(50))
    numero_documento = Column(String(100))
    monto_neto = Column(Float)
    monto_iva = Column(Float)
    monto_total = Column(Float)
    tipo = Column(String(50))  # Compra/Venta
    descripcion = Column(Text)
    fecha_registro = Column(DateTime, default=datetime.now)
    
    # Relaciones
    conciliaciones = relationship("Conciliacion", back_populates="registro_sii")
    
    def __repr__(self):
        return f"<RegistroSII {self.numero_documento}: {self.monto_total}>"


class Conciliacion(Base):
    """Modelo de conciliación."""
    __tablename__ = "conciliaciones"
    
    id = Column(Integer, primary_key=True)
    id_transaccion = Column(Integer, ForeignKey("transacciones_bancarias.id"))
    id_registro_sii = Column(Integer, ForeignKey("registros_sii.id"))
    fecha_conciliacion = Column(DateTime, default=datetime.now)
    puntuacion_matching = Column(Float)
    estado = Column(Enum(EstadoConciliacion), default=EstadoConciliacion.PENDIENTE)
    notas = Column(Text)
    usuario = Column(String(100))
    
    # Relaciones
    transaccion_bancaria = relationship("TransaccionBancaria", back_populates="conciliaciones")
    registro_sii = relationship("RegistroSII", back_populates="conciliaciones")
    
    def __repr__(self):
        return f"<Conciliacion {self.id}: {self.estado}>"


class Pago(Base):
    """Modelo de pago a cliente o proveedor."""
    __tablename__ = "pagos"
    
    id = Column(Integer, primary_key=True)
    id_transaccion = Column(Integer, ForeignKey("transacciones_bancarias.id"))
    tipo_beneficiario = Column(String(50))  # Cliente/Proveedor
    rut_beneficiario = Column(String(20))
    nombre_beneficiario = Column(String(200))
    monto = Column(Float)
    fecha_pago = Column(DateTime)
    fecha_confirmacion = Column(DateTime)
    estado = Column(Enum(EstadoPago), default=EstadoPago.PENDIENTE)
    numero_comprobante = Column(String(100))
    banco_origen = Column(String(100))
    banco_destino = Column(String(100))
    cuenta_destino = Column(String(100))
    notas = Column(Text)
    
    # Relaciones
    transaccion = relationship("TransaccionBancaria", back_populates="pagos")
    
    def __repr__(self):
        return f"<Pago {self.numero_comprobante}: {self.monto}>"


class Auditoria(Base):
    """Modelo de auditoría de cambios."""
    __tablename__ = "auditoria"
    
    id = Column(Integer, primary_key=True)
    fecha_cambio = Column(DateTime, default=datetime.now)
    tabla_afectada = Column(String(100))
    id_registro = Column(Integer)
    tipo_cambio = Column(String(50))  # CREATE/UPDATE/DELETE
    usuario = Column(String(100))
    descripcion = Column(Text)
    valores_anteriores = Column(Text)
    valores_nuevos = Column(Text)
    
    def __repr__(self):
        return f"<Auditoria {self.tabla_afectada}: {self.tipo_cambio}>"
