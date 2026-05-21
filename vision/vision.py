"""
Módulo de Visión Artificial - MyCobot 280
Responsable: Ingeniera de Visión (P6)
"""
import cv2
import numpy as np

# =====================================================================
# 1. DICCIONARIO MULTICOLOR (Calibración HSV)
# =====================================================================
# Valores extraídos de la calibración en laboratorio para los 4 cubos
RANGOS_HSV = {
    "rojo":     {"lower": np.array([0, 100, 100]),   "upper": np.array([10, 255, 255])},
    "azul":     {"lower": np.array([100, 150, 50]),  "upper": np.array([140, 255, 255])},
    "verde":    {"lower": np.array([40, 70, 70]),    "upper": np.array([80, 255, 255])},
    "amarillo": {"lower": np.array([20, 100, 100]),  "upper": np.array([40, 255, 255])}
}

# =====================================================================
# 2. PARÁMETROS ESPACIALES (Transformación Píxel -> mm)
# =====================================================================
FACTOR_PIXEL_A_MM = 0.75
ORIGEN_ROBOT_X_PX = 320
ORIGEN_ROBOT_Y_PX = 480

# =====================================================================
# 3. FUNCIÓN PRINCIPAL DE DETECCIÓN ROBUSTA
# =====================================================================
def detectar_y_calcular_coordenadas(frame, color_objetivo):
    """
    Recibe un frame de video y un string con el color objetivo ('rojo', 'azul', etc.). 
    Aplica filtros morfológicos, halla el centroide y lo transforma a mm reales. # Filtro para borrar ruido visual
    Retorna: (x_mm, y_mm) o None si no encuentra el objeto.
    """
    if frame is None:
        return None
        
    if color_objetivo not in RANGOS_HSV:
        print(f"[ERROR] El color '{color_objetivo}' no está calibrado.")
        return None

    limites = RANGOS_HSV[color_objetivo]
    
    # 1. Filtro de luz y conversión
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, limites["lower"], limites["upper"])
    
    # 2. Filtros morfológicos para ruido
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # 3. Extracción de contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(max_contour)
        
        # Filtrado por área mínima (elimina reflejos pequeños)
        if area > 400: 
            M = cv2.moments(max_contour)
            if M["m00"] != 0:
                # Centroide en píxeles
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Transformación a milímetros reales
                x_mm = round((cy - ORIGEN_ROBOT_Y_PX) * FACTOR_PIXEL_A_MM * (-1), 2)
                y_mm = round((cx - ORIGEN_ROBOT_X_PX) * FACTOR_PIXEL_A_MM, 2)
                
                return x_mm, y_mm
                
    # Si no detecta nada o el área es muy pequeña
    return None

# =====================================================================
# BLOQUE DE PRUEBA INDEPENDIENTE (Solo se ejecuta si corres vision.py directo)
# =====================================================================
if __name__ == "__main__":
    print("Iniciando prueba de cámara para el módulo de Visión...")
    cap = cv2.VideoCapture(0)
    time.sleep(1) # Estabilizar cámara
    ret, frame_prueba = cap.read()
    cap.release()

    if ret:
        color_test = "amarillo" # Cambia esto para probar otros colores
        resultado = detectar_y_calcular_coordenadas(frame_prueba, color_test)
        if resultado:
            rx, ry = resultado
            print(f"ÉXITO: Cubo {color_test} detectado en X={rx} mm, Y={ry} mm")
        else:
            print(f"Cubo {color_test} no encontrado en la escena.")
    else:
        print("Error al acceder a la cámara.")
