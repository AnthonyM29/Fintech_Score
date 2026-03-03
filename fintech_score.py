import math

data_base = []

def solicitar_float(mensaje):
    while True:
        try:
            entrada = input(mensaje)
            valor = float(entrada)
            if valor < 0:
                print("Por favor, ingrese un número positivo.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número válido.")
            
def calcular_indicadores(usuario):
    I = usuario["ingresos"]
    G = usuario["gastos"]
    
    usuario["capacidad_pago"] = I - G
    # Evitamos error si el ingreso es 0
    usuario["DTI"] = (G / I) * 100 if I > 0 else 0
    
def mostrar_estadisticas_grupo():
    if not data_base:
        print("No hay usuarios registrados.")
        return
    
    suma_ingresos = 0.0
    contador = 0
    
    print("\n" + "="*30)
    print("ESTADÍSTICAS DEL GRUPO")
    print("="*30)
    
    for usuario in data_base:
        suma_ingresos += usuario["ingresos"]
        contador += 1
        # Llamamos a la función para actualizar los datos del usuario antes de mostrar
        calcular_indicadores(usuario)
        
    promedio = suma_ingresos / contador
    print(f"Usuarios registrados: {contador}")
    print(f"Promedio de ingresos: ${promedio:,.2f}")
            
def registrar_usuario():
    print("\n--- Registro de Usuario ---")
    
    while True:
        nombre = input("Ingrese su nombre: ").strip()
        if nombre:
            break
        print("El nombre no puede estar vacío.")

    ingresos = solicitar_float("Ingrese sus ingresos mensuales: ")
    gastos = solicitar_float("Ingrese sus gastos mensuales: ")
    monto = solicitar_float("Ingrese el monto solicitado: ")
    
    nuevo_usuario = {
        "nombre": nombre,
        "ingresos": ingresos,
        "gastos": gastos,
        "monto": monto,
        "capacidad_pago": 0.0,
        "DTI": 0.0
    }
    
    data_base.append(nuevo_usuario)
    print(f"\n¡Usuario {nombre} registrado con éxito!")
    
def simular_cuota_mensual(monto, tasa_anual=24, meses=12):
    """Calcula la cuota mensual fija usando el sistema de amortización francés."""
    tasa_mensual = (tasa_anual / 100) / 12
    cuota = (monto * tasa_mensual) / (1 - math.pow(1 + tasa_mensual, -meses))
    return cuota

def modulo_busqueda_interactivo():
    """
    Módulo de expansión: Permite consultar usuarios específicos 
    por nombre y muestra su simulación de cuotas.
    """
    print("\n" + "="*30)
    print("MÓDULO DE CONSULTA RÁPIDA")
    print("="*30)

    while True:
        opcion = input("\n¿Desea buscar a un solicitante específico? (s/n): ").lower()
        
        if opcion == 'n':
            print("Saliendo del buscador...")
            break
        elif opcion == 's':
            nombre_buscado = input("Ingrese el nombre del usuario a consultar: ").strip().lower()
            encontrado = False
            
            for usuario in data_base:
                if usuario["nombre"].lower() == nombre_buscado:
                    encontrado = True
                    print("\n" + "-"*40)
                    print(f"EXPEDIENTE: {usuario['nombre'].upper()}")
                    print(f"ESTADO ACTUAL: {usuario['estado']}")
                    
                    if usuario['estado'] == "APROBADO":
                        # LLAMADA A TU FUNCIÓN ORIGINAL
                        # Usamos los valores por defecto (24% anual, 12 meses)
                        cuota = simular_cuota_mensual(usuario['monto'])
                        
                        print(f"Monto solicitado: ${usuario['monto']:,.2f}")
                        print(f"CUOTA MENSUAL SUGERIDA: ${cuota:,.2f} (a 12 meses)")
                    
                    elif usuario['estado'] == "PENDIENTE" or usuario['estado'] == "EN REVISIÓN":
                        print(f"Monto en evaluación: ${usuario['monto']:,.2f}")
                        print("AVISO: No se pueden generar cuotas para perfiles en revisión.")
                    
                    else: # Caso RECHAZADO
                        print("⚠️ ALERTA DE RIESGO: CRÉDITO NO DISPONIBLE")
                        print(f"Motivo: DTI del {usuario['DTI']:.2f}% excede el límite permitido.")
                        print("Sugerencia: Revisar capacidad de endeudamiento del cliente.")
                    
                    print("-" * 40)
                    break
            
            if not encontrado:
                print(f"Lo sentimos, no existe un registro para '{nombre_buscado}'.")
        else:
            print("Por favor, ingrese 's' para buscar o 'n' para finalizar.")
    
def clsificar_riesgo(usuario):
    DTI = usuario["DTI"]
    
    if DTI > 60:
        usuario["estado"] = "RECHAZADO"
        return ""
    elif DTI < 35 :
        usuario["estado"] = "APROBADO"
    else:
       usuario["estado"] = "PENDIENTE"

def ordenar_burbuja():
    n = len(data_base)
    for i in range(n):
        for j in range(0, n-i-1):
            usuario_actual = data_base[j]
            usuario_siguiente = data_base[j+1]
            if usuario_actual["DTI"] > usuario_siguiente["DTI"]:
                aux = data_base[j]
                data_base[j] = data_base[j+1]
                data_base[j+1] = aux
                
def guardar_reporte_csv():
    nombre_archivo = "reporte_fintech.csv"
    
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write("Nombre,Ingresos,Gastos,Monto Solicitado,Capacidad de Pago,DTI (%),Estado\n")
            for usuario in data_base:
                linea = f"{usuario['nombre']},{usuario['ingresos']},{usuario['gastos']},{usuario['monto']},{usuario['capacidad_pago']},{usuario['DTI']},{usuario.get('estado', '')}\n"
                archivo.write(linea)
                
                print(f" Exito: Reporte guardado con el nombre '{nombre_archivo}'.")
    
    except Exception as e:
        print(f"Error al guardar el reporte: {e}")

def main():
    print("SISTEMA DE REGISTRO DE CRÉDITOS")
    
    continuar = True
    
    while continuar:
        registrar_usuario()
        
        opcion = input("\n¿Desea registrar otro usuario? (s/n): ").lower()
        if opcion != "s":
            continuar = False
    
    mostrar_estadisticas_grupo()
    
    for usuario in data_base:
        clsificar_riesgo(usuario)
    
    ordenar_burbuja()
    print("Usuarios ordenados por capacidad de pago (DTI).")
    
    # Resumen final
    print("\n" + "="*45)
    print("RESUMEN DE SOLICITANTES")
    print("="*45)
    
    print(f"{'Nombre':<15} | {'DTI (%)':<10} | {'Capacidad Pago':<15} | {'Estado':<12}")
    print("-" * 45)
    
    for p in data_base:
        # Se asegura de que los indicadores estén calculados
        print(f"{p['nombre']:<15} | {p['DTI']:<10.2f}% | ${p['capacidad_pago']:>13,.2f} | {p['estado']:<15}\n")
        
    print("\n--- HERRAMIENTAS AVANZADAS ---")
    
    guardar_reporte_csv()
    
    modulo_busqueda_interactivo()
    
    print("\nGracias por usar el sistema.")

if __name__ == "__main__":
    main()