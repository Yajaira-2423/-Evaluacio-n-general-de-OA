import csv
import json
import os
import time
import random

# --- FASE I: GENERACIÓN DE DATOS MASIVOS (OPTIMIZADA) ---
NOMBRES = ["Ana Lopez", "Carlos Ruiz", "Juan Perez", "Maria Gomez", "Luis Hernandez", "Sofia Diaz"]
MEDICAMENTOS = ["Paracetamol", "Ibuprofeno", "Metformina", "Amoxicilina", "Losartan"]
ESPECIALIDADES = ["Cardiologia", "Pediatria", "Urgencias", "Medicina General", "Ginecologia"]

def generar_registro_base(idx):
    edad = random.randint(1, 90)
    temp = round(random.uniform(36.0, 39.5), 1)
    presion = f"{random.randint(110, 140)}/{random.randint(70, 95)}"
    return {
        "id": idx,
        "nombre": random.choice(NOMBRES),
        "edad": edad,
        "temperatura": temp,
        "presion": presion,
        "medicamento": random.choice(MEDICAMENTOS),
        "especialidad": random.choice(ESPECIALIDADES)
    }

def construir_archivos_experimento(volumen):
    print(f"\nGenerando archivos para volumen de {volumen} registros...")
    archivo_csv = f"hospital_{volumen}.csv"
    archivo_json = f"hospital_{volumen}.json"
    
    # Escritura en CSV (Rápida y línea por línea)
    inicio = time.time()
    with open(archivo_csv, mode='w', encoding='utf-8', newline='') as f:
        columnas = ["id", "nombre", "edad", "temperatura", "presion", "medicamento", "especialidad"]
        escritor = csv.DictWriter(f, fieldnames=columnas)
        escritor.writeheader()
        for i in range(1, volumen + 1):
            escritor.writerow(generar_registro_base(i))
    tiempo_w_csv = time.time() - inicio
    
    # Escritura en JSON (Simulando formato jerárquico requerido por la rúbrica)
    inicio = time.time()
    with open(archivo_json, mode='w', encoding='utf-8') as f:
        f.write('{"pacientes": [\n')
        for i in range(1, volumen + 1):
            reg = generar_registro_base(i)
            # Construimos la estructura anidada del ejemplo del profesor
            obj_json = {
                "id": reg["id"],
                "nombre": reg["nombre"],
                "edad": reg["edad"],
                "consulta": {
                    "temperatura": reg["temperatura"],
                    "presion": reg["presion"],
                    "medicamento": reg["medicamento"],
                    "especialidad": reg["especialidad"]
                }
            }
            linea = json.dumps(obj_json)
            if i < volumen:
                f.write(f"  {linea},\n")
            else:
                f.write(f"  {linea}\n")
        f.write(']}')
    tiempo_w_json = time.time() - inicio
    
    return tiempo_w_csv, tiempo_w_json

# --- FASE II Y III: MEDICIONES Y SISTEMA ---
def medir_lectura(volumen):
    archivo_csv = f"hospital_{volumen}.csv"
    archivo_json = f"hospital_{volumen}.json"
    
    # Medir Lectura CSV
    t_in = time.time()
    with open(archivo_csv, mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        _ = [fila for fila in lector] # Carga completa a memoria
    t_read_csv = time.time() - t_in
    
    # Medir Lectura JSON
    t_in = time.time()
    with open(archivo_json, mode='r', encoding='utf-8') as f:
        _ = json.load(f) # Carga completa a memoria
    t_read_json = time.time() - t_in
    
    return t_read_csv, t_read_json
if __name__ == "__main__":
    # Ajusta el volumen para tus pruebas oficiales (1M, 10M, 20M)
    volumen_prueba = 1000000 
    
    tw_csv, tw_json = construir_archivos_experimento(volumen_prueba)
    tr_csv, tr_json = medir_lectura(volumen_prueba)
    
    print("\n" + "="*70)
    print(" FASE III. EXPERIMENTACIÓN - TABLA DE RESULTADOS GENERALES")
    print("="*70)
    print(f"{'Métrica':<35} | {'CSV':<15} | {'JSON':<15}")
    print("-"*70)
    print(f"{'Tiempo de lectura':<35} | {tr_csv:.4f} s | {tr_json:.4f} s")
    print(f"{'Tiempo de escritura':<35} | {tw_csv:.4f} s | {tw_json:.4f} s")
    print(f"{'Tamaño del archivo':<35} | {os.path.getsize(f'hospital_{volumen_prueba}.csv')/(1024*1024):.2f} MB | {os.path.getsize(f'hospital_{volumen_prueba}.json')/(1024*1024):.2f} MB")
    print(f"{'Facilidad de procesamiento':<35} | Alta (Arreglos) | Media (Objetos)")
    print(f"{'Facilidad de visualización':<35} | Excelente     | Compleja")
    print(f"{'Flexibilidad (Info. Compleja)':<35} | Baja (Plana)    | Alta (Anidada)")
    print("="*70)

# --- MENÚ DE PRUEBAS ---
if __name__ == "__main__":
    # NOTA: Para probar rápido en tu computadora usa 10000. 
    # Para la entrega oficial cambia este número a 1000000 (1 Millón)
    volumen_prueba =  1000000
    
    tw_csv, tw_json = construir_archivos_experimento(volumen_prueba)
    tr_csv, tr_json = medir_lectura(volumen_prueba)
    
    print("\n======== TABLA DE RESULTADOS EXPERIMENTALES ========")
    print(f"Métrica\t\t\t\tCSV\t\tJSON")
    print(f"Tiempo Escritura:\t\t{tw_csv:.4f}s\t\t{tw_json:.4f}s")
    print(f"Tiempo Lectura:\t\t\t{tr_csv:.4f}s\t\t{tr_json:.4f}s")
    print(f"Tamaño Archivo (Disk):\t\t{os.path.getsize(f'hospital_{volumen_prueba}.csv')/(1024*1024):.2f}MB\t"
          f"{os.path.getsize(f'hospital_{volumen_prueba}.json')/(1024*1024):.2f}MB")