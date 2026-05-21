# Trabajo Parcial - Robótica 

# Sobre el proyecto

Este proyecto fue desarrollado como parte del curso de Robótica y tiene como objetivo crear un sistema capaz de detectar objetos mediante una cámara y moverlos automáticamente utilizando un brazo robótico MyCobot.

La idea principal es que el robot pueda identificar un objeto, calcular cómo debe moverse y finalmente agarrarlo y colocarlo en otra posición de manera automática.

Durante el desarrollo del proyecto se trabajará con visión por computadora, control del robot y cálculos matemáticos para el movimiento del brazo robótico.

---

# ¿Qué hace el proyecto?

El sistema realiza el siguiente proceso:

1. La cámara detecta un objeto.
2. Se calcula la posición del objeto.
3. El brazo robótico calcula cómo debe moverse.
4. El robot se desplaza hacia el objeto.
5. La pinza lo agarra.
6. Finalmente el objeto es colocado en otra ubicación.

---

# Tecnologías utilizadas

- Python
- OpenCV
- NumPy
- MyCobot
- GitHub

---

# Organización del proyecto

```text
TrabajoParcial_Robotica/
│
├── cinematica/
│   └── cinematica.py
│
├── control/
│   └── control.py
│
├── vision/
│   └── vision.py
│
├── main/
│   └── main.py
│
└── README.md

Integrantes:
Maria flor de liz Elias Carbajal
Jose Eduardo Pillco Rozas
Jose Anyelo Huaman Loza
Gabriela Sofia Marin Soto

Funcionalidades principales
-Detección de objetos mediante cámara
-Movimiento automático del brazo robótico
-Cálculo de posiciones y movimientos
-Agarre y traslado de objetos
-Integración completa del sistema

Estado del proyecto
Actualmente el proyecto se encuentra en desarrollo y seguirá mejorando progresivamente durante el curso.

Objetivo final
Lograr que el robot pueda interactuar automáticamente con objetos reales utilizando visión artificial y movimientos precisos del brazo robótico.
