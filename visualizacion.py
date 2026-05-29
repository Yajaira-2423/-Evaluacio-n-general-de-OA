import pandas as pd
import matplotlib.pyplot as plt

# =====================================================================
# --- FASE IV: VISUALIZACIÓN DE DATOS (Y FASE VI: ANÁLISIS) ---
# =====================================================================
def generar_analisis_grafico(archivo_csv, tiempo_csv=0.15, tiempo_json=0.45):
    """Carga los datos mediante Pandas y genera las visualizaciones requeridas por la rúbrica."""
    print(f"\n[Fase IV] Procesando análisis visual del archivo: {archivo_csv}...")
    df = pd.read_csv(archivo_csv)
    
    # --- Fase VI: Análisis Descriptivo ---
    print("\n--- ESTADÍSTICAS DESCRIPTIVAS DE TEMPERATURA (Signos Vitales) ---")
    print(f"Promedio: {df['temperatura'].mean():.2f}°C")
    print(f"Máximo:   {df['temperatura'].max()}°C")
    print(f"Mínimo:   {df['temperatura'].min()}°C")
    
    # Crear un panel maestro de visualización (2 filas x 2 columnas)
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    
    # Gráfica 1: Barras - Rangos de Edad de Pacientes
    df['Rango_Edad'] = pd.cut(df['edad'], bins=[0, 18, 40, 60, 90], 
                              labels=['Niños/Adolescentes', 'Adulto Joven', 'Adulto', 'Adulto Mayor'])
    df['Rango_Edad'].value_counts().plot(kind='bar', ax=axs[0, 0], color='skyblue', edgecolor='black')
    axs[0, 0].set_title('Pacientes por Rango de Edad (Barras)')
    axs[0, 0].set_ylabel('Cantidad de Pacientes')
    axs[0, 0].tick_params(axis='x', rotation=15)
    
    # Gráfica 2: Pastel / Circular - Distribución por Especialidades
    df['especialidad'].value_counts().plot(kind='pie', ax=axs[0, 1], autopct='%1.1f%%', startangle=90, shadow=True)
    axs[0, 1].set_title('Distribución por Especialidades Médicas (Circular)')
    axs[0, 1].set_ylabel('')  # Eliminar etiqueta innecesaria
    
    # Gráfica 3: Histograma - Frecuencia de Signos Vitales (Temperatura)
    df['temperatura'].plot(kind='hist', bins=15, ax=axs[1, 0], color='salmon', edgecolor='black')
    axs[1, 0].set_title('Histograma de Signos Vitales (Temperatura)')
    axs[1, 0].set_xlabel('Temperatura (°C)')
    axs[1, 0].set_ylabel('Frecuencia')
    
    # Gráfica 4: Líneas - Tiempos del Experimento Reales
    formatos = ['CSV', 'JSON']
    tiempos = [tiempo_csv, tiempo_json]
    axs[1, 1].plot(formatos, tiempos, marker='o', linestyle='-', color='purple', linewidth=2.5, markersize=8)
    axs[1, 1].set_title('Comparación de Tendencia en Tiempos de Carga (Líneas)')
    axs[1, 1].set_ylabel('Segundos')
    axs[1, 1].grid(True, linestyle='--', alpha=0.6)

    # Ajustar espaciado y guardar imagen automáticamente
    plt.tight_layout()
    plt.savefig('reporte_grafico_hospital.png')
    print("\nPanel gráfico exportado con éxito como 'reporte_grafico_hospital.png'")
    plt.show()

# --- Bloque de Ejecución Gráfica ---
if __name__ == "__main__":
    # Ejecuta el análisis gráfico usando el archivo CSV de un millón generado previamente
    # Nota: Puedes actualizar los argumentos numéricos con tus tiempos exactos del primer script
    generar_analisis_grafico("hospital_1000000.csv", tiempo_csv=0.1245, tiempo_json=0.5892)