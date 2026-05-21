import cv2
import numpy as np
import time
from pymycobot.mycobot import MyCobot

# =====================================================================
# ### MÓDULO 1: CONFIGURACIÓN E INICIALIZACIÓN DEL SISTEMA (CONTROL)
# =====================================================================
# Se establece la conexión física con el MyCobot a través del puerto serie
mc = MyCobot('/dev/ttyUSB0', 1000000)
mc.power_on()
time.sleep(1)

# =====================================================================
# ### MÓDULO 2: CINEMÁTICA (DEFINICIÓN DE ESPACIO DE TRABAJO Y POSE)
# =====================================================================
# Matrices de configuración de articulaciones calibradas en el laboratorio
POSE_DETECCION = [18.19, -7.64, -62.05, -18.98, 0.7, -44.91]
POSE_AGARRE    = [18.36, -49.83, -43.41, -7.03, 5.27, -41.83]

# Diccionario que actúa como base de datos geométrica para la descarga
ZONAS_DESCARGA = {
    "azul":     [116.27, -70.57, 0.35, -37.79, 0.7, -44.91],
    "verde":    [102.04, -69.16, 0.35, -37.88, 0.35, -44.91],
    "rojo":     [84.9, -69.16, 0.35, -37.88, 0.52, -45.61],
    "amarillo": [68.64, -70.22, -3.51, -22.58, 0.52, -67.23]
}

# =====================================================================
# ### MÓDULO 3: VISIÓN ARTIFICIAL (PROCESAMIENTO DE IMAGEN HSV)
# =====================================================================
def detectar_color_objeto():
    
    cap = cv2.VideoCapture(0) 
    if not cap.isOpened():
        cap = cv2.VideoCapture(1) 
        
    time.sleep(1) 
    ret, frame = cap.read()
    cap.release() 
    
    # Manejo de error: si la cámara se desconecta físicamente
    if not ret:
        print("[VISIÓN] Error: No se pudo obtener imagen de la cámara.")
        return "desconocido"
    
    # Segmentación del área central de la mesa de trabajo
    h, w, _ = frame.shape
    centro = frame[int(h*0.3):int(h*0.7), int(w*0.3):int(w*0.7)]
    
    # Transformación al espacio de color HSV para estabilidad lumínica
    hsv = cv2.cvtColor(centro, cv2.COLOR_BGR2HSV)
    
    # Umbrales HSV definidos para el entorno del laboratorio
    rangos = {
        "rojo": ([0, 100, 100], [10, 255, 255]),
        "azul": ([100, 150, 50], [140, 255, 255]),
        "verde": ([40, 70, 70], [80, 255, 255]),
        "amarillo": ([20, 100, 100], [30, 255, 255])
    }
    
    color_ganador = "desconocido"
    max_pixeles = 0
    
    # Algoritmo de decisión por conteo de densidad de píxeles
    for color, (bajo, alto) in rangos.items():
        mascara = cv2.inRange(hsv, np.array(bajo), np.array(alto))
        conteo = cv2.countNonZero(mascara)
        # Filtro de ruido: Requiere un mínimo de 500 píxeles activos
        if conteo > max_pixeles and conteo > 500: 
            max_pixeles = conteo
            color_ganador = color
            
    print(f"[VISIÓN] Color dominante detectado: {color_ganador.upper()}")
    return color_ganador

# =====================================================================
# ### MÓDULO 4: CONTROL DE ACTUADORES
# =====================================================================
def ejecutar_ciclo_completo_autonomo():
   
    for ciclo in range(1, 6):
        print(f"\n==========================================")
        print(f" >>> INICIANDO CICLO AUTÓNOMO {ciclo}/5 <<<")
        print(f"==========================================")
        
        # ESTADO: IDLE 
        print("Llevando a punto de cámara...")
        mc.send_angles(POSE_DETECCION, 40)
        time.sleep(4)
        
        # ESTADO: DETECTAR
        color = detectar_color_objeto()
        
        # MANEJO DE ERRORES: Salto seguro si la mesa está vacía
        if color == "desconocido":
            print("No hay objeto en la zona o color no identificado. Saltando ciclo.")
            continue
            
        # ESTADO: AGARRAR
        print("Bajando a posición de agarre...")
        mc.send_angles(POSE_AGARRE, 40)
        time.sleep(4)
        
        print("Cerrando pinzas...")
        mc.set_gripper_value(1, 60) 
        time.sleep(2)
        
        # CONTROL DE SEGURIDAD: Elevación del eje 2 para evitar arrastres físicos
        print("Elevando carga...")
        mc.send_angle(2, -15, 30) 
        time.sleep(2)
        
        # ESTADO: CALC_IK 
        destino = ZONAS_DESCARGA[color]
        print(f"Trasladando hacia zona {color.upper()}...")
        mc.send_angles(destino, 40)
        time.sleep(5)
        
        print("Abriendo pinzas...")
        # Envío de comandos redundantes para asegurar la apertura en J6
        mc.set_gripper_value(0, 60) 
        mc.set_gripper_state(0, 60)
        time.sleep(2)
        
        # CONTROL DE SEGURIDAD: Retiro vertical
        print("Elevando brazo libre hacia arriba...")
        mc.send_angle(2, -20, 30)
        time.sleep(2.5)
        
    # Fin de la rutina autónoma: Retorno a pose segura final
    print("\n[SISTEMA] Rutina finalizada. Regresando a pose segura.")
    mc.send_angles(POSE_DETECCION, 40)
    time.sleep(4)

# =====================================================================
# ### EJECUCIÓN CENTRAL DEL PROGRAMA INTEGRADO
# =====================================================================
ejecutar_ciclo_completo_autonomo()
