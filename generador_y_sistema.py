import csv
import json
import os
import time
import random
import tracemalloc
import pandas as pd

# ============================================================
# DATOS BASE
# ============================================================

NOMBRES = ["Ana Lopez", "Carlos Ruiz", "Juan Perez", "Maria Gomez", "Luis Hernandez", "Sofia Diaz"]
MEDICAMENTOS = ["Paracetamol", "Ibuprofeno", "Metformina", "Amoxicilina", "Losartan"]
ESPECIALIDADES = ["Cardiologia", "Pediatria", "Urgencias", "Medicina General", "Ginecologia"]

# ============================================================
# GENERADOR
# ============================================================

def generar_registro(idx):
    return {
        "id": idx,
        "nombre": random.choice(NOMBRES),
        "edad": random.randint(1, 90),
        "temperatura": round(random.uniform(36.0, 39.5), 1),
        "presion": f"{random.randint(110,140)}/{random.randint(70,95)}",
        "medicamento": random.choice(MEDICAMENTOS),
        "especialidad": random.choice(ESPECIALIDADES)
    }

# ============================================================
# FASE I - ARCHIVOS
# ============================================================

def construir_archivos(volumen):
    print(f"\nGenerando {volumen} registros...")

    csv_file = f"hospital_{volumen}.csv"
    json_file = f"hospital_{volumen}.json"

    # -------- CSV --------
    t0 = time.time()

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=generar_registro(1).keys())
        writer.writeheader()

        for i in range(1, volumen + 1):
            writer.writerow(generar_registro(i))

    t_csv = time.time() - t0

    # -------- JSON --------
    t0 = time.time()

    with open(json_file, "w", encoding="utf-8") as f:
        f.write('{"pacientes":[\n')

        for i in range(1, volumen + 1):
            r = generar_registro(i)

            obj = {
                "id": r["id"],
                "nombre": r["nombre"],
                "edad": r["edad"],
                "consulta": {
                    "temperatura": r["temperatura"],
                    "presion": r["presion"],
                    "medicamento": r["medicamento"],
                    "especialidad": r["especialidad"]
                }
            }

            line = json.dumps(obj)

            if i < volumen:
                f.write(line + ",\n")
            else:
                f.write(line + "\n")

        f.write("]}")

    t_json = time.time() - t0

    return t_csv, t_json


# ============================================================
# FASE II - SISTEMA
# ============================================================

def buscar_por_id(archivo, id_buscar):
    with open(archivo, "r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for row in lector:
            if row["id"] == str(id_buscar):
                return row
    return None


def buscar_por_nombre(archivo, nombre):
    resultados = []

    with open(archivo, "r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for row in lector:
            if nombre.lower() in row["nombre"].lower():
                resultados.append(row)

    return resultados


def registrar_paciente(archivo, datos):
    with open(archivo, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=datos.keys())
        writer.writerow(datos)


# ============================================================
# FASE III - EXPERIMENTO
# ============================================================

def medir_lectura(volumen):
    csv_file = f"hospital_{volumen}.csv"
    json_file = f"hospital_{volumen}.json"

    # CSV
    tracemalloc.start()
    t0 = time.time()

    with open(csv_file, "r", encoding="utf-8") as f:
        for _ in csv.DictReader(f):
            pass

    t_csv = time.time() - t0
    mem_csv = tracemalloc.get_traced_memory()[1] / 1024 / 1024
    tracemalloc.stop()

    # JSON
    tracemalloc.start()
    t0 = time.time()

    with open(json_file, "r", encoding="utf-8") as f:
        json.load(f)

    t_json = time.time() - t0
    mem_json = tracemalloc.get_traced_memory()[1] / 1024 / 1024
    tracemalloc.stop()

    return t_csv, t_json, mem_csv, mem_json


def tabla_resultados(volumen, tw_csv, tw_json, tr_csv, tr_json, mem_csv, mem_json):

    import os

    size_csv = os.path.getsize(f"hospital_{volumen}.csv") / (1024 * 1024)
    size_json = os.path.getsize(f"hospital_{volumen}.json") / (1024 * 1024)

    print("\n" + "="*80)
    print("FASE III. EXPERIMENTACIÓN - TABLA DE RESULTADOS GENERALES")
    print("="*80)

    print(f"{'Métrica':40} | {'CSV':20} | {'JSON':20}")
    print("-"*80)

    print(f"{'Tiempo de lectura':40} | {tr_csv:.4f} s | {tr_json:.4f} s")
    print(f"{'Tiempo de escritura':40} | {tw_csv:.4f} s | {tw_json:.4f} s")
    print(f"{'Tamaño del archivo':40} | {size_csv:.2f} MB | {size_json:.2f} MB")
    print(f"{'Memoria RAM usada':40} | {mem_csv:.2f} MB | {mem_json:.2f} MB")

    print(f"{'Facilidad de procesamiento':40} | Alta (Arreglos) | Media (Objetos)")
    print(f"{'Facilidad de visualización':40} | Alta | Media")
    print(f"{'Flexibilidad para info compleja':40} | Baja | Alta")

    print("="*80)
    print("\nINTERPRETACIÓN:")
print("- CSV es más eficiente en rendimiento bruto.")
print("- JSON es superior para datos hospitalarios complejos.")
print("- El costo de flexibilidad en JSON es mayor uso de memoria.")

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    volumen = 10000000

    tw_csv, tw_json = construir_archivos(volumen)

    nuevo = {
        "id": volumen + 1,
        "nombre": "Valeria Vargas",
        "edad": 21,
        "temperatura": 36.5,
        "presion": "120/80",
        "medicamento": "Paracetamol",
        "especialidad": "Urgencias"
    }

    registrar_paciente(f"hospital_{volumen}.csv", nuevo)

    tr_csv, tr_json, mem_csv, mem_json = medir_lectura(volumen)

    tabla_resultados(volumen, tw_csv, tw_json, tr_csv, tr_json, mem_csv, mem_json)
    size_csv = os.path.getsize(f"hospital_{volumen}.csv") / (1024 * 1024)
    size_json = os.path.getsize(f"hospital_{volumen}.json") / (1024 * 1024)

# ============================================================
# FASE V - EVALUACIÓN DEL SISTEMA
# ============================================================

def evaluacion_sistema(size_csv, size_json, tr_csv, tr_json):

    print("\n" + "="*80)
    print("FASE V. EVALUACIÓN DEL SISTEMA")
    print("="*80)

    # 1
    print("\n1) ¿Qué organización fue más eficiente?")
    
    if tr_csv < tr_json:
        print("CSV fue más eficiente debido a que tuvo menor tiempo de lectura y procesamiento.")
    else:
        print("JSON fue más eficiente en las pruebas realizadas.")

    # 2
    print("\n2) ¿Cuál fue más flexible?")
    print("JSON fue más flexible porque permite manejar estructuras complejas y jerárquicas.")

    # 3
    print("\n3) ¿Cuál facilita más el análisis de datos?")
    print("CSV facilita más el análisis debido a que Pandas y otras herramientas trabajan directamente con tablas.")

    # 4
    print("\n4) ¿Cuál consume menos almacenamiento?")

    if size_csv < size_json:
        print("CSV consume menos almacenamiento.")
    else:
        print("JSON consume menos almacenamiento.")

    # 5
    print("\n5) ¿Qué formato recomendarían para hospitales reales?")
    print("Se recomienda JSON para hospitales reales porque permite almacenar expedientes médicos complejos, consultas, tratamientos y múltiples relaciones entre datos.")
    # ============================================================
# FASE VI - INTERPRETACIÓN DE DATOS
# ============================================================

def interpretacion_datos(archivo_csv):

    print("\n" + "="*80)
    print("FASE VI. INTERPRETACIÓN DE DATOS")
    print("="*80)

    df = pd.read_csv(archivo_csv)

    # Tendencia encontrada
    especialidad_frecuente = df["especialidad"].value_counts().idxmax()

    print("\n• Tendencia encontrada:")
    print(f"La especialidad con más consultas fue: {especialidad_frecuente}")

    # Patrones de consultas
    promedio_temp = df["temperatura"].mean()

    print("\n• Patrones de consultas:")
    print(f"La temperatura promedio registrada fue de {promedio_temp:.2f}°C.")

    altas_temp = len(df[df["temperatura"] > 38])

    print(f"Se detectaron {altas_temp} pacientes con temperatura mayor a 38°C.")

    # Distribución de pacientes
    print("\n• Distribución de pacientes:")

    edades = pd.cut(
        df["edad"],
        bins=[0, 18, 40, 60, 90],
        labels=["Niños", "Adultos Jóvenes", "Adultos", "Adultos Mayores"]
    )

    distribucion = edades.value_counts()

    for categoria, cantidad in distribucion.items():
        print(f"{categoria}: {cantidad} pacientes")