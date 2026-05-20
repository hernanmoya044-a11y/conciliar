"""Aplicación principal con Streamlit."""

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# Importar módulos de la aplicación
from config import STREAMLIT_CONFIG, CONCILIACION_CONFIG
from src.extractors.pdf_extractor import ExtractorPDF
from src.extractors.excel_extractor import ExtractorExcel
from src.extractors.sii_extractor import ExtractorSII
from src.reconciliation.reconciler import Conciliador
from src.reconciliation.comparator import Comparador
from src.reports.generator import GeneradorReportes
from src.reports.exporters import ExportadorReportes
from src.utils.validators import ValidadorDatos


# Configurar página
st.set_page_config(**STREAMLIT_CONFIG)

# Estilos CSS
st.markdown("""
    <style>
    .header-main {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar estado de sesión
if "conciliador" not in st.session_state:
    st.session_state.conciliador = Conciliador(
        tolerancia_dias=CONCILIACION_CONFIG["tolerance_dias"],
        tolerancia_monto=CONCILIACION_CONFIG["tolerance_monto"],
        min_fuzzy_score=CONCILIACION_CONFIG["min_fuzzy_score"],
    )

if "datos_cargados" not in st.session_state:
    st.session_state.datos_cargados = False


def main():
    """Función principal de la aplicación."""
    
    # Header
    st.markdown("""
        <div class="header-main">
            <h1>💰 Sistema de Conciliación Bancaria</h1>
            <p>Conciliación automática de transacciones bancarias con registros SII</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Barra lateral
    with st.sidebar:
        st.title("🎯 Menú Principal")
        seccion = st.radio(
            "Selecciona una sección:",
            ["📊 Dashboard", "📁 Cargar Datos", "🔄 Conciliación", "👥 Gestión de Pagos", "📈 Reportes", "⚙️ Configuración"]
        )
    
    # Secciones principales
    if seccion == "📊 Dashboard":
        mostrar_dashboard()
    
    elif seccion == "📁 Cargar Datos":
        mostrar_carga_datos()
    
    elif seccion == "🔄 Conciliación":
        mostrar_conciliacion()
    
    elif seccion == "👥 Gestión de Pagos":
        mostrar_pagos()
    
    elif seccion == "📈 Reportes":
        mostrar_reportes()
    
    elif seccion == "⚙️ Configuración":
        mostrar_configuracion()


def mostrar_dashboard():
    """Muestra el dashboard principal."""
    st.title("📊 Dashboard")
    
    if not st.session_state.datos_cargados:
        st.info("ℹ️ Carga datos en la sección 'Cargar Datos' para comenzar.")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Estado", "Listo", "✓")
    
    with col2:
        st.metric("Última actualización", datetime.now().strftime("%H:%M:%S"))
    
    with col3:
        st.metric("Tasa de Conciliación", "--", "%")


def mostrar_carga_datos():
    """Muestra la sección de carga de datos."""
    st.title("📁 Cargar Datos")
    
    tab1, tab2, tab3 = st.tabs(["📄 Extracto Bancario", "📊 Registros SII", "Ver Datos Cargados"])
    
    with tab1:
        st.subheader("Cargar Extracto Bancario")
        
        archivo_tipo = st.radio("Formato del archivo:", ["PDF", "Excel"])
        
        archivo = st.file_uploader(
            f"Sube un archivo {archivo_tipo}",
            type=["pdf"] if archivo_tipo == "PDF" else ["xlsx", "xls", "csv"]
        )
        
        if archivo is not None:
            with st.spinner("Procesando archivo..."):
                try:
                    if archivo_tipo == "PDF":
                        extractor = ExtractorPDF()
                    else:
                        extractor = ExtractorExcel()
                    
                    # Guardar archivo temporalmente
                    ruta_temp = Path("data/uploads") / archivo.name
                    ruta_temp.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(ruta_temp, "wb") as f:
                        f.write(archivo.getbuffer())
                    
                    # Extraer datos
                    datos = extractor.extraer(str(ruta_temp))
                    
                    if datos:
                        st.session_state.datos_bancarios = pd.DataFrame(datos)
                        st.session_state.datos_cargados = True
                        st.success(f"✓ {len(datos)} transacciones cargadas correctamente")
                    else:
                        st.error("No se pudieron extraer datos del archivo")
                
                except Exception as e:
                    st.error(f"Error procesando archivo: {str(e)}")
    
    with tab2:
        st.subheader("Cargar Registros SII")
        
        tipo_registro = st.selectbox("Tipo de registro:", ["Compras", "Ventas"])
        
        archivo_sii = st.file_uploader(
            "Sube archivo Excel con registros del SII",
            type=["xlsx", "xls"],
            key="sii_upload"
        )
        
        if archivo_sii is not None:
            with st.spinner("Procesando archivo SII..."):
                try:
                    extractor_sii = ExtractorSII()
                    
                    ruta_temp = Path("data/uploads") / archivo_sii.name
                    ruta_temp.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(ruta_temp, "wb") as f:
                        f.write(archivo_sii.getbuffer())
                    
                    tipo_lowercase = tipo_registro.lower()
                    datos_sii = extractor_sii.extraer(str(ruta_temp), tipo_lowercase)
                    
                    if datos_sii:
                        st.session_state.registros_sii = pd.DataFrame(datos_sii)
                        st.success(f"✓ {len(datos_sii)} registros SII cargados correctamente")
                    else:
                        st.error("No se pudieron extraer datos del SII")
                
                except Exception as e:
                    st.error(f"Error procesando SII: {str(e)}")
    
    with tab3:
        st.subheader("Datos Cargados")
        
        if hasattr(st.session_state, "datos_bancarios"):
            st.write("**Transacciones Bancarias:**")
            st.dataframe(st.session_state.datos_bancarios.head(10))
        
        if hasattr(st.session_state, "registros_sii"):
            st.write("**Registros SII:**")
            st.dataframe(st.session_state.registros_sii.head(10))


def mostrar_conciliacion():
    """Muestra la sección de conciliación."""
    st.title("🔄 Conciliación Automática")
    
    if not st.session_state.datos_cargados:
        st.warning("⚠️ Carga los datos primero en la sección 'Cargar Datos'")
        return
    
    if st.button("Ejecutar Conciliación", use_container_width=True, type="primary"):
        with st.spinner("Ejecutando conciliación automática..."):
            try:
                # Cargar datos
                st.session_state.conciliador.cargar_datos(
                    st.session_state.datos_bancarios,
                    st.session_state.registros_sii
                )
                
                # Ejecutar conciliación
                resumen = st.session_state.conciliador.conciliar_automaticamente()
                
                # Mostrar resultados
                st.success("✓ Conciliación completada")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Conciliaciones",
                        resumen["conciliaciones_exitosas"],
                        f"{resumen['tasa_conciliacion']:.1f}%"
                    )
                
                with col2:
                    st.metric(
                        "OK",
                        resumen["conciliadas_ok"]
                    )
                
                with col3:
                    st.metric(
                        "Parcial",
                        resumen["conciliadas_parcial"]
                    )
                
                with col4:
                    st.metric(
                        "Discrepancias",
                        resumen["discrepancias"]
                    )
                
                st.session_state.resumen_conciliacion = resumen
                st.session_state.conciliacion_ejecutada = True
            
            except Exception as e:
                st.error(f"Error en conciliación: {str(e)}")
    
    if hasattr(st.session_state, "conciliacion_ejecutada") and st.session_state.conciliacion_ejecutada:
        st.divider()
        
        tab1, tab2 = st.tabs(["Conciliaciones", "Discrepancias"])
        
        with tab1:
            st.subheader("Transacciones Conciliadas")
            df_conciliaciones = st.session_state.conciliador.obtener_conciliaciones()
            if not df_conciliaciones.empty:
                st.dataframe(df_conciliaciones, use_container_width=True)
            else:
                st.info("No hay conciliaciones")
        
        with tab2:
            st.subheader("Discrepancias Detectadas")
            df_discrepancias = st.session_state.conciliador.obtener_discrepancias()
            if not df_discrepancias.empty:
                st.dataframe(df_discrepancias, use_container_width=True)
            else:
                st.success("✓ Sin discrepancias")


def mostrar_pagos():
    """Muestra la sección de gestión de pagos."""
    st.title("👥 Gestión de Pagos")
    
    tab1, tab2 = st.tabs(["Pagos a Clientes", "Pagos a Proveedores"])
    
    with tab1:
        st.subheader("Pagos a Clientes")
        st.info("Funcionalidad de pagos a clientes")
    
    with tab2:
        st.subheader("Pagos a Proveedores")
        st.info("Funcionalidad de pagos a proveedores")


def mostrar_reportes():
    """Muestra la sección de reportes."""
    st.title("📈 Reportes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Exportar Reporte")
        
        if st.button("Generar Reporte Excel", use_container_width=True):
            if hasattr(st.session_state, "conciliacion_ejecutada"):
                with st.spinner("Generando reporte..."):
                    reporte = GeneradorReportes.generar_reporte_conciliacion(
                        st.session_state.resumen_conciliacion,
                        st.session_state.conciliador.conciliaciones,
                        st.session_state.conciliador.discrepancias
                    )
                    
                    nombre_archivo = ExportadorReportes.generar_nombre_archivo("conciliacion")
                    ruta_salida = Path("data/reportes") / nombre_archivo
                    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
                    
                    exito, mensaje = ExportadorReportes.exportar_excel(reporte, str(ruta_salida))
                    
                    if exito:
                        st.success(f"✓ {mensaje}")
                        with open(ruta_salida, "rb") as f:
                            st.download_button(
                                label="Descargar Reporte",
                                data=f.read(),
                                file_name=nombre_archivo,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                    else:
                        st.error(f"✗ {mensaje}")
            else:
                st.warning("Ejecuta una conciliación primero")
    
    with col2:
        st.subheader("Cuadre SII")
        
        if st.button("Generar Cuadre", use_container_width=True):
            if hasattr(st.session_state, "datos_bancarios") and hasattr(st.session_state, "registros_sii"):
                cuadre = GeneradorReportes.generar_reporte_cuadre_sii(
                    st.session_state.datos_bancarios,
                    st.session_state.registros_sii
                )
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Total Banco", f"$ {cuadre['total_banco']:,.0f}")
                with col_b:
                    st.metric("Total SII", f"$ {cuadre['total_sii']:,.0f}")
                
                col_c, col_d = st.columns(2)
                with col_c:
                    st.metric("Diferencia", f"$ {cuadre['diferencia']:,.0f}")
                with col_d:
                    st.metric("Estado", cuadre["estado_cuadre"])
            else:
                st.warning("Carga los datos primero")


def mostrar_configuracion():
    """Muestra la sección de configuración."""
    st.title("⚙️ Configuración")
    
    with st.expander("Configuración de Conciliación"):
        st.write("**Parámetros de Conciliación:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dias = st.number_input(
                "Tolerancia de días:",
                min_value=1,
                max_value=30,
                value=CONCILIACION_CONFIG["tolerance_dias"]
            )
        
        with col2:
            monto = st.number_input(
                "Tolerancia de monto:",
                min_value=0.0,
                max_value=1000.0,
                value=CONCILIACION_CONFIG["tolerance_monto"],
                step=0.1
            )
        
        with col3:
            fuzzy = st.number_input(
                "Score fuzzy mínimo:",
                min_value=0,
                max_value=100,
                value=CONCILIACION_CONFIG["min_fuzzy_score"]
            )
        
        if st.button("Guardar Configuración"):
            st.session_state.conciliador.matcher.tolerancia_dias = dias
            st.session_state.conciliador.matcher.tolerancia_monto = monto
            st.session_state.conciliador.matcher.min_fuzzy_score = fuzzy
            st.success("✓ Configuración guardada")
    
    with st.expander("Información del Sistema"):
        st.write(f"**Versión:** 1.0.0")
        st.write(f"**Última actualización:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Base de Datos:** SQLite")


if __name__ == "__main__":
    main()
