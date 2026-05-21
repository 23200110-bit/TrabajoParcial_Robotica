import numpy as np
import time
from pymycobot.mycobot import MyCobot

def calcular_ik_analitica(x, y, z):
    
    d1 = 131.56
    a2 = 110.4
    a3 = 96.0
    
    # 1. Ángulo de la base (J1)
    theta1 = np.degrees(np.arctan2(y, x))
    
    # 2. Modelo planar simplificado para J2 y J3 
    r = np.sqrt(x**2 + y**2)
    vd = z - d1  # Altura neta desde el hombro
    
    
    D = (r**2 + vd**2 - a2**2 - a3**2) / (2 * a2 * a3)
   
    D = np.clip(D, -1.0, 1.0)
    
    # Ángulo del codo (J3) - Opción codo abajo
    theta3 = np.degrees(np.arctan2(np.sqrt(1 - D**2), D))
    
    # Ángulo del hombro (J2)
    theta2 = np.degrees(np.arctan2(vd, r)) - np.degrees(np.arctan2(a3 * np.sin(np.radians(theta3)), a2 + a3 * np.cos(np.radians(theta3))))
    
   
    return [theta1, theta2, theta3, 0.0, 0.0, 0.0]



x_destino, y_destino, z_destino = 50.0, -65.0, 410.0
print(f"--- COORDENADA OBJETIVO: X={x_destino}, Y={y_destino}, Z={z_destino} ---")


angulos_analiticos = calcular_ik_analitica(x_destino, y_destino, z_destino)
print(f"Ángulos calculados (Analítica): J1={angulos_analiticos[0]:.2f}°, J2={angulos_analiticos[1]:.2f}°, J3={angulos_analiticos[2]:.2f}°")

# Conectar al robot real y pedirle su solución vía API
try:
    mc = MyCobot('/dev/ttyUSB0', 1000000)
    mc.power_on()
    time.sleep(1)
    
    # Enviamos al robot a esa coordenada (Modo 1 = Coordenadas lineales)
    print("\nEnviando coordenadas al robot real")
    mc.send_coords([x_destino, y_destino, z_destino, -90, 0, -90], 30, 1)
    time.sleep(4) 
    
    # Leer los ángulos reales
    angulos_api = mc.get_angles()
    
    if angulos_api:
        print(f"Ángulos reales (API): J1={angulos_api[0]:.2f}°, J2={angulos_api[1]:.2f}°, J3={angulos_api[2]:.2f}°")
        
        # Calcular el error
        err_j1 = abs(angulos_analiticos[0] - angulos_api[0])
        err_j2 = abs(angulos_analiticos[1] - angulos_api[1])
        err_j3 = abs(angulos_analiticos[2] - angulos_api[2])
        
        print("\n=== ERROR EN GRADOS ===")
        print(f"Error J1 = {err_j1:.2f}°")
        print(f"Error J2 = {err_j2:.2f}°")
        print(f"Error J3 = {err_j3:.2f}°")
    else:
        print("Error: El API no pudo resolver o leer los ángulos para esta posición.")
        
except Exception as e:
    print(f"Error de conexión: {e}")