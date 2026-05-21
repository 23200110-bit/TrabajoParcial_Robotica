import time

POSE_ORIGINAL_ANGULOS = [0, 0, 0, 0, 0, 0]
Z_MINIMO_SEGURO = 80.0     # Límite absoluto antes de chocar con la mesa 
Z_TRANSITO_SEGURO = 160.0  # Altura de vuelo sobre las cajas/cámara 

def ejecutar_movimiento_seguro(mc, coords_destino, velocidad=35):
    """
    Verifica que la coordenada Z destino no sea menor al umbral seguro.
    Si hay peligro, el robot aborta y regresa a su pose original. [cite: 1312, 1314]
    """
    x, y, z, rx, ry, rz = coords_destino
    print(f"\n[PROCESANDO] Evaluando trayectoria a Z={z}mm")
    
    if z < Z_MINIMO_SEGURO: 
        print(f"[¡ALERTA P4!] El destino Z ({z}mm) es menor al límite seguro ({Z_MINIMO_SEGURO}mm).") 
        print("-> [INICIANDO MANIOBRA DE EVASIÓN REACTIVA]") 
        
        # Amago de movimiento hasta el límite y freno
        z_limite_permitido = Z_MINIMO_SEGURO + 10.0
        mc.send_coords([x, y, z_limite_permitido, rx, ry, rz], velocidad, 1) 
        time.sleep(2.0) 
        
        # Retorno de emergencia 
        mc.stop() 
        time.sleep(0.2) 
        mc.send_angles(POSE_ORIGINAL_ANGULOS, 50) 
        time.sleep(3.5) 
        print("[SISTEMA PROTEGIDO] El robot ha regresado a salvo.") 
        return False
        
    else:
        mc.send_coords(coords_destino, velocidad, 1) 
        time.sleep(3.5) 
        return True 

def ejecutar_movimiento_anti_entorno(mc, coords_destino, velocidad=35):
    """
    Genera una trayectoria en forma de 'U' invertida (Herradura) 
    para no golpear las cajas al moverse en diagonal. 
    """
    x_dest, y_dest, z_dest, rx, ry, rz = coords_destino 
    
    pos_actual = mc.get_coords() 
    if not pos_actual: return False 
    x_act, y_act, z_act = pos_actual[0], pos_actual[1], pos_actual[2] 

    print("[PREVENCIÓN ACTIVADA] Evitando trayectoria diagonal contra cajas.") 
    # FASE A: Elevación vertical pura (Ganar Clearance) 
    mc.send_coords([x_act, y_act, Z_TRANSITO_SEGURO, rx, ry, rz], velocidad, 1) 
    time.sleep(2.5) 
    # FASE B: Traslación horizontal (Vuelo sobre obstáculos) 
    mc.send_coords([x_dest, y_dest, Z_TRANSITO_SEGURO, rx, ry, rz], velocidad, 1) 
    time.sleep(2.5) 
    # FASE C: Descenso vertical final [cite: 1452]
    mc.send_coords([x_dest, y_dest, z_dest, rx, ry, rz], velocidad, 1)
    time.sleep(2.5)
    
    print("[ÉXITO] Destino alcanzado de forma segura.")
    return True 
