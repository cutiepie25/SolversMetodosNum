"""
Considere el problema con valores iniciales

y' = 2x - 3y + 1, y(0) = 1

Use el Método Multipasos de Adams-Bashforth-Moulton para aproximar con cuatro decimales y(0.8). 
Utilice h = 0.2 y el Método RK4 para calcular y₁, y₂, y₃. 
Reporte en una tabla los valores de RK4 obtenidos y después el valor del método Multipasos para y(0.8).
"""

import math
from solvers import rk4, adams_bashforth_moulton

# ============================================
# CONFIGURACIÓN DEL PROBLEMA
# ============================================
x0 = 0.0
y0 = 1.0
x_final = 0.8
h = 0.2

def f(x, y):
    """
    Ecuación diferencial: y' = 2x - 3y + 1
    """
    return 2*x - 3*y + 1

def y_analitica(x: float) -> float:
    """
    Solución analítica del problema:
    y' = 2x - 3y + 1, y(0) = 1
    
    Solución: y(x) = (2/3)x - (7/9) + (16/9)e^(-3x)
    
    Esta solución se obtiene resolviendo la EDO lineal de primer orden.
    """
    return (2/3)*x - (7/9) + (16/9)*math.exp(-3*x)


# ============================================
# FUNCIONES DE PRESENTACIÓN
# ============================================

def imprimir_tabla_rk4(x_vals, y_vals):
    """
    Imprime la tabla con los valores iniciales calculados por RK4
    """
    print("\n" + "="*60)
    print("VALORES INICIALES CALCULADOS CON RK4 (h = 0.2)")
    print("="*60)
    print(f"{'Paso':<6} {'xₙ':<10} {'yₙ (RK4)':<15} {'Valor Real':<15} {'Error Abs':<12}")
    print("-"*60)
    
    for i in range(min(4, len(x_vals))):  # Solo mostrar los primeros 4 valores
        x = x_vals[i]
        y_num = y_vals[i]
        y_real = y_analitica(x)
        error = abs(y_real - y_num)
        
        print(f"{i:<6} {x:<10.4f} {y_num:<15.6f} {y_real:<15.6f} {error:<12.8f}")


def imprimir_tabla_completa(x_vals, y_vals):
    """
    Imprime la tabla completa incluyendo los valores del método ABM
    """
    print("\n" + "="*70)
    print("TABLA COMPLETA: RK4 (inicialización) + ABM (método multipasos)")
    print("="*70)
    print(f"{'Paso':<6} {'xₙ':<10} {'yₙ':<15} {'Valor Real':<15} {'Error Abs':<12} {'Método':<10}")
    print("-"*70)
    
    for i, x in enumerate(x_vals):
        y_num = y_vals[i]
        y_real = y_analitica(x)
        error = abs(y_real - y_num)
        metodo = "RK4" if i < 4 else "ABM"
        
        print(f"{i:<6} {x:<10.4f} {y_num:<15.6f} {y_real:<15.6f} {error:<12.8f} {metodo:<10}")


def imprimir_resultado_final(x_vals, y_vals):
    """
    Imprime el resultado final en x = 0.8
    """
    x_final = x_vals[-1]
    y_final = y_vals[-1]
    y_real_final = y_analitica(x_final)
    error_abs = abs(y_real_final - y_final)
    error_rel = (error_abs / abs(y_real_final)) * 100 if abs(y_real_final) > 1e-15 else 0
    
    print("\n" + "="*60)
    print("📊 RESULTADO FINAL EN x = 0.8")
    print("="*60)
    print(f"Valor aproximado (ABM): {y_final:.6f}")
    print(f"Valor real (analítico):  {y_real_final:.6f}")
    print(f"Error absoluto:          {error_abs:.8f}")
    print(f"Error relativo:          {error_rel:.6f}%")
    print("="*60)


def imprimir_explicacion():
    """
    Imprime una explicación del método
    """
    print("\n" + "="*70)
    print("📚 EXPLICACIÓN DEL MÉTODO ADAMS-BASHFORTH-MOULTON")
    print("="*70)
    print("""
El método ABM es un método PREDICTOR-CORRECTOR que funciona en dos fases:

1️⃣  INICIALIZACIÓN (usando RK4):
   • El método multipasos necesita 4 valores previos para comenzar
   • Usamos RK4 para calcular y₁, y₂, y₃ con alta precisión
   • Estos valores sirven como "historial" para el método

2️⃣  FASE MULTIPASOS (ABM):
   
   🔮 PREDICTOR (Adams-Bashforth):
      Usa una extrapolación de los últimos 4 puntos:
      y_{n+1}^P = y_n + (h/24)[55f_n - 59f_{n-1} + 37f_{n-2} - 9f_{n-3}]
   
   ✅ CORRECTOR (Adams-Moulton):
      Refina la predicción usando el valor predicho:
      y_{n+1}^C = y_n + (h/24)[9f_{n+1}^P + 19f_n - 5f_{n-1} + f_{n-2}]

VENTAJAS:
• Mayor precisión que métodos de un solo paso
• Reutiliza información de pasos anteriores
• Eficiente computacionalmente (pocas evaluaciones de f)

DESVENTAJAS:
• Necesita inicialización con otro método
• No es auto-iniciante
• Requiere paso h constante
""")
    print("="*70)


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def main():
    """
    Función principal que ejecuta el método ABM
    """
    print("🔬 MÉTODO ADAMS-BASHFORTH-MOULTON")
    print("="*60)
    print("Problema: y' = 2x - 3y + 1, y(0) = 1")
    print("Objetivo: Aproximar y(0.8) con h = 0.2")
    print("Método: ABM de orden 4 (inicialización con RK4)")
    print("="*60)
    
    # ========== PASO 1: Calcular solo con RK4 para comparación ==========
    print("\n📍 PASO 1: Calculando valores iniciales con RK4...")
    x_rk4, y_rk4 = rk4(f, x0, y0, h, x0 + 3*h)  # Solo hasta y₃
    imprimir_tabla_rk4(x_rk4, y_rk4)
    
    # ========== PASO 2: Aplicar el método completo ABM ==========
    print("\n📍 PASO 2: Aplicando método completo ABM hasta x = 0.8...")
    x_abm, y_abm = adams_bashforth_moulton(f, x0, y0, h, x_final)
    
    # ========== PASO 3: Mostrar resultados ==========
    imprimir_tabla_completa(x_abm, y_abm)
    imprimir_resultado_final(x_abm, y_abm)
    
    # ========== PASO 4: Mostrar explicación ==========
    imprimir_explicacion()
    
    print("\n🎉 ¡Análisis completado!")
    print(f"\n💡 Respuesta final: y(0.8) ≈ {y_abm[-1]:.4f}")


if __name__ == "__main__":
    main()