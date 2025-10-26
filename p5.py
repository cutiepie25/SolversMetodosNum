"""
TAREA 5: Movimiento del péndulo en la Tierra vs Luna

Un péndulo de longitud l oscila más rápido en la Tierra o en la Luna?

a) Tome l = 3 y g = 32 para la aceleración de la gravedad en la Tierra. 
   Use algún método numérico para generar una curva de solución numérica 
   para el modelo no lineal del péndulo:

   d²θ/dt² + (g/l)sen(θ) = 0  
   
   Condiciones iniciales: θ(0) = 1, θ'(0) = 2

   Repita usando los mismos valores pero utilice 0.165g para la Luna.

b) De las gráficas determine: 
   - ¿Qué péndulo oscila más rápido?
   - ¿Qué péndulo tiene mayor amplitud?

CONVERSIÓN A SISTEMA DE PRIMER ORDEN:
--------------------------------------
La ecuación de segundo orden d²θ/dt² + (g/l)sen(θ) = 0 se convierte en:

Variables:
  y₁ = θ        (posición angular en radianes)
  y₂ = θ' = dθ/dt   (velocidad angular en rad/s)

Sistema equivalente:
  dy₁/dt = y₂                    (la derivada de la posición es la velocidad)
  dy₂/dt = -(g/l)sen(y₁)         (la derivada de la velocidad es la aceleración)

Condiciones iniciales:
  y₁(0) = 1 rad
  y₂(0) = 2 rad/s
"""

import math
import matplotlib.pyplot as plt
from solvers import rk4_sistema

# ============================================
# PARÁMETROS DEL PROBLEMA
# ============================================

# Parámetros físicos
L = 3.0                    # Longitud del péndulo (metros)
G_TIERRA = 32.0           # Aceleración en la Tierra (m/s²)
G_LUNA = 0.165 * G_TIERRA # Aceleración en la Luna (m/s²)

# Condiciones iniciales
THETA_0 = 1.0  # Ángulo inicial (radianes) ≈ 57.3°
OMEGA_0 = 2.0  # Velocidad angular inicial (rad/s)

# Parámetros numéricos
T_INICIAL = 0.0
T_FINAL = 10.0   # Simular 10 segundos
H = 0.01         # Paso pequeño para buena precisión


# ============================================
# DEFINICIÓN DEL SISTEMA DE ECUACIONES
# ============================================

def sistema_pendulo(t, y, g, l):
    """
    Sistema de ecuaciones para el péndulo no lineal.
    
    Parámetros:
    -----------
    t : float
        Tiempo actual (no se usa en este caso, pero RK4 lo requiere)
    y : list [y₁, y₂]
        y₁ = θ (ángulo)
        y₂ = θ' (velocidad angular)
    g : float
        Aceleración de la gravedad
    l : float
        Longitud del péndulo
    
    Retorna:
    --------
    [dy₁/dt, dy₂/dt] : list
        dy₁/dt = y₂
        dy₂/dt = -(g/l)sen(y₁)
    
    EXPLICACIÓN FÍSICA:
    -------------------
    - dy₁/dt = y₂: La tasa de cambio del ángulo es la velocidad angular
    - dy₂/dt = -(g/l)sen(y₁): La aceleración angular viene de la componente
      tangencial de la gravedad: a = -g*sen(θ)/l (con l normalizado)
    """
    theta = y[0]      # y₁ = θ (posición angular)
    omega = y[1]      # y₂ = ω = dθ/dt (velocidad angular)
    
    # Derivadas
    dtheta_dt = omega                    # dy₁/dt = y₂
    domega_dt = -(g/l) * math.sin(theta) # dy₂/dt = -(g/l)sen(y₁)
    
    return [dtheta_dt, domega_dt]


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def crear_funcion_pendulo(g, l):
    """
    Crea una función del sistema de péndulo con g y l fijos.
    Esto es necesario porque rk4_sistema espera f(t, y) pero
    nuestro sistema también depende de g y l.
    """
    def f(t, y):
        return sistema_pendulo(t, y, g, l)
    return f


def calcular_periodo_aproximado(t_vals, theta_vals):
    """
    Calcula el periodo aproximado del péndulo detectando los cruces por cero.
    
    Un periodo completo ocurre cuando el péndulo vuelve a la misma posición
    con la misma dirección de movimiento.
    """
    cruces = []
    
    # Detectar cruces por cero (cuando θ cambia de signo)
    for i in range(1, len(theta_vals)):
        if theta_vals[i-1] * theta_vals[i] < 0:  # Cambio de signo
            # Interpolación lineal para encontrar el tiempo exacto del cruce
            t_cruce = t_vals[i-1] + (t_vals[i] - t_vals[i-1]) * abs(theta_vals[i-1]) / (abs(theta_vals[i-1]) + abs(theta_vals[i]))
            cruces.append(t_cruce)
    
    if len(cruces) >= 2:
        # El periodo es el doble del tiempo entre dos cruces consecutivos
        # (un cruce es media oscilación)
        periodo = 2 * (cruces[1] - cruces[0])
        return periodo
    
    return None


def calcular_amplitud(theta_vals):
    """
    Calcula la amplitud máxima del movimiento.
    La amplitud es el valor máximo absoluto de θ.
    """
    return max(abs(min(theta_vals)), abs(max(theta_vals)))


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def main():
    """
    Simula el movimiento del péndulo en la Tierra y en la Luna,
    genera gráficas comparativas y analiza el comportamiento.
    """
    
    print("=" * 70)
    print("🌍🌙 SIMULACIÓN: PÉNDULO EN LA TIERRA VS LUNA")
    print("=" * 70)
    print(f"\nParámetros del péndulo:")
    print(f"  • Longitud: l = {L} m")
    print(f"  • Ángulo inicial: θ(0) = {THETA_0} rad ({math.degrees(THETA_0):.1f}°)")
    print(f"  • Velocidad inicial: θ'(0) = {OMEGA_0} rad/s")
    print(f"\nAceleraciones:")
    print(f"  • Tierra: g = {G_TIERRA} m/s²")
    print(f"  • Luna:   g = {G_LUNA:.2f} m/s² (0.165 × g_Tierra)")
    print(f"\nMétodo numérico: RK4 para sistemas")
    print(f"Paso de integración: h = {H} s")
    print(f"Tiempo de simulación: [0, {T_FINAL}] s")
    print("=" * 70)
    
    # ========== SIMULACIÓN EN LA TIERRA ==========
    print("\n🌍 Resolviendo para la Tierra...")
    y0 = [THETA_0, OMEGA_0]  # Condiciones iniciales: [θ(0), θ'(0)]
    f_tierra = crear_funcion_pendulo(G_TIERRA, L)
    
    t_tierra, y_tierra = rk4_sistema(f_tierra, T_INICIAL, y0, H, T_FINAL)
    
    # Extraer θ(t) y ω(t)
    theta_tierra = [y[0] for y in y_tierra]  # Posición angular
    omega_tierra = [y[1] for y in y_tierra]  # Velocidad angular
    
    # ========== SIMULACIÓN EN LA LUNA ==========
    print("🌙 Resolviendo para la Luna...")
    f_luna = crear_funcion_pendulo(G_LUNA, L)
    
    t_luna, y_luna = rk4_sistema(f_luna, T_INICIAL, y0, H, T_FINAL)
    
    # Extraer θ(t) y ω(t)
    theta_luna = [y[0] for y in y_luna]
    omega_luna = [y[1] for y in y_luna]
    
    # ========== ANÁLISIS DE RESULTADOS ==========
    print("\n" + "=" * 70)
    print("📊 ANÁLISIS DE RESULTADOS")
    print("=" * 70)
    
    # Calcular periodos
    periodo_tierra = calcular_periodo_aproximado(t_tierra, theta_tierra)
    periodo_luna = calcular_periodo_aproximado(t_luna, theta_luna)
    
    # Calcular amplitudes
    amp_tierra = calcular_amplitud(theta_tierra)
    amp_luna = calcular_amplitud(theta_luna)
    
    # Mostrar resultados
    print(f"\n🌍 TIERRA:")
    if periodo_tierra:
        print(f"  • Periodo aproximado: T ≈ {periodo_tierra:.3f} s")
        print(f"  • Frecuencia: f ≈ {1/periodo_tierra:.3f} Hz")
    print(f"  • Amplitud máxima: {amp_tierra:.3f} rad ({math.degrees(amp_tierra):.1f}°)")
    
    print(f"\n🌙 LUNA:")
    if periodo_luna:
        print(f"  • Periodo aproximado: T ≈ {periodo_luna:.3f} s")
        print(f"  • Frecuencia: f ≈ {1/periodo_luna:.3f} Hz")
    print(f"  • Amplitud máxima: {amp_luna:.3f} rad ({math.degrees(amp_luna):.1f}°)")
    
    # Comparación
    print(f"\n📈 COMPARACIÓN:")
    if periodo_tierra and periodo_luna:
        ratio_periodo = periodo_luna / periodo_tierra
        print(f"  • El péndulo en la Luna oscila {ratio_periodo:.2f}× más lento")
        print(f"  • El péndulo en la Tierra es {1/ratio_periodo:.2f}× más rápido")
    
    ratio_amp = amp_luna / amp_tierra
    print(f"  • Amplitud Luna / Amplitud Tierra = {ratio_amp:.3f}")
    
    # Conclusiones
    print(f"\n🎯 CONCLUSIONES:")
    print(f"  • ¿Cuál oscila más rápido? → {'TIERRA' if periodo_tierra and periodo_luna and periodo_tierra < periodo_luna else 'LUNA'}")
    print(f"  • ¿Cuál tiene mayor amplitud? → {'TIERRA' if amp_tierra > amp_luna else 'LUNA'}")
    print("=" * 70)
    
    # ========== GRÁFICAS ==========
    print("\n📊 Generando gráficas...")
    
    # Crear figura con 3 subplots
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle('Movimiento del Péndulo: Tierra vs Luna', fontsize=16, fontweight='bold')
    
    # --- Gráfica 1: Posición angular θ(t) ---
    ax1 = axes[0]
    ax1.plot(t_tierra, theta_tierra, 'b-', label='Tierra', linewidth=1.5)
    ax1.plot(t_luna, theta_luna, 'r-', label='Luna', linewidth=1.5)
    ax1.set_ylabel('θ(t) [radianes]', fontsize=11)
    ax1.set_title('a) Posición Angular θ(t)', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right')
    ax1.axhline(y=0, color='k', linestyle='--', linewidth=0.5, alpha=0.5)
    
    # --- Gráfica 2: Velocidad angular ω(t) ---
    ax2 = axes[1]
    ax2.plot(t_tierra, omega_tierra, 'b-', label='Tierra', linewidth=1.5)
    ax2.plot(t_luna, omega_luna, 'r-', label='Luna', linewidth=1.5)
    ax2.set_ylabel('ω(t) [rad/s]', fontsize=11)
    ax2.set_title('b) Velocidad Angular ω(t) = dθ/dt', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper right')
    ax2.axhline(y=0, color='k', linestyle='--', linewidth=0.5, alpha=0.5)
    
    # --- Gráfica 3: Retrato de fase (ω vs θ) ---
    ax3 = axes[2]
    ax3.plot(theta_tierra, omega_tierra, 'b-', label='Tierra', linewidth=1.5, alpha=0.7)
    ax3.plot(theta_luna, omega_luna, 'r-', label='Luna', linewidth=1.5, alpha=0.7)
    ax3.set_xlabel('θ [radianes]', fontsize=11)
    ax3.set_ylabel('ω [rad/s]', fontsize=11)
    ax3.set_title('c) Retrato de Fase (Espacio de estados)', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc='upper right')
    ax3.axhline(y=0, color='k', linestyle='--', linewidth=0.5, alpha=0.5)
    ax3.axvline(x=0, color='k', linestyle='--', linewidth=0.5, alpha=0.5)
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Gráficas generadas exitosamente")
    print("\n🎉 ¡Simulación completada!\n")


if __name__ == "__main__":
    main()