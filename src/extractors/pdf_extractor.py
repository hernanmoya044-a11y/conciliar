"""Extractor de datos desde archivos PDF."""

import pdfplumber
import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path
import re


class ExtractorPDF:
    """Extrae transacciones bancarias desde archivos PDF."""

    def __init__(self):
        self.datos_extraidos = []

    def extraer(self, ruta_archivo: str) -> List[Dict]:
        """Extrae transacciones de un PDF."""
        self.datos_extraidos = []
        
        try:
            with pdfplumber.open(ruta_archivo) as pdf:
                for numero_pagina, pagina in enumerate(pdf.pages):
                    texto = pagina.extract_text()
                    tablas = pagina.extract_tables()
                    
                    # Intentar extraer de tablas
                    if tablas:
                        for tabla in tablas:
                            self._procesar_tabla(tabla, numero_pagina)
                    
                    # Intentar extraer del texto
                    if texto:
                        self._procesar_texto(texto, numero_pagina)
            
            return self.datos_extraidos
        
        except Exception as e:
            print(f"Error extrayendo PDF: {str(e)}")
            return []

    def _procesar_tabla(self, tabla: List[List[str]], numero_pagina: int):
        """Procesa una tabla extraída del PDF."""
        if len(tabla) < 2:
            return
        
        encabezados = tabla[0]
        
        for fila in tabla[1:]:
            if all(celda is None or celda == "" for celda in fila):
                continue
            
            transaccion = {}
            for i, encabezado in enumerate(encabezados):
                if i < len(fila):
                    transaccion[encabezado] = fila[i]
            
            if self._validar_transaccion(transaccion):
                transaccion["pagina"] = numero_pagina
                self.datos_extraidos.append(transaccion)

    def _procesar_texto(self, texto: str, numero_pagina: int):
        """Procesa texto del PDF buscando patrones de transacciones."""
        # Patrón para detectar líneas de transacciones: fecha monto concepto
        patron = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+([\d.,]+)\s+(.+)"
        
        coincidencias = re.finditer(patron, texto)
        
        for coincidencia in coincidencias:
            try:
                fecha_str = coincidencia.group(1)
                monto_str = coincidencia.group(2)
                concepto = coincidencia.group(3)
                
                transaccion = {
                    "fecha": fecha_str,
                    "monto": monto_str,
                    "concepto": concepto,
                    "pagina": numero_pagina,
                    "fuente": "PDF"
                }
                
                if self._validar_transaccion(transaccion):
                    self.datos_extraidos.append(transaccion)
            
            except Exception:
                continue

    @staticmethod
    def _validar_transaccion(transaccion: Dict) -> bool:
        """Valida que una transacción tenga datos mínimos."""
        campos_requeridos = ["fecha", "monto"]
        return all(transaccion.get(campo) for campo in campos_requeridos)

    def obtener_dataframe(self) -> pd.DataFrame:
        """Retorna los datos extraídos como DataFrame."""
        return pd.DataFrame(self.datos_extraidos)
