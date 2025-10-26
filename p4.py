"""Un modelo matemático para el área A (en centímetros cuadrados) que ocupa una colonia de bacterias en el tiempo t (dias) esta dada por:
dA/dt = A(2.128 - 0.0432A)
Suponga que el área inicial es 0.24 centímetros cuadrados o sea A(0) = 0.24. 
Utilice algún método numérico para calcular la solución del problema en múltiples puntos del intervalo de tiempo [0,10]. 
Trace la gráfica de la solución en ese intervalo."""

import math
from solvers import rk4
import matplotlib.pyplot as plt

def f(t, A):
    a_prima = A*(2.128 - 0.0432*A)
    return a_prima

def y_analitica(x: float) -> float:
    """
    Solución analítica del problema:
    y' = 2x - 3y + 1, y(0) = 1
    
    Solución: y(x) = (2/3)x - (7/9) + (16/9)e^(-3x)
    
    Esta solución se obtiene resolviendo la EDO lineal de primer orden.
    """
    return (49.25925925925926)/ (1+204.2469135802469*math.exp(-2.128*x))


def generar_tabla(x_vals, y_RK4, decimales=4, precision_porcentaje=4):
    tabla = []
    for i, x in enumerate(x_vals):
        y_rk4 = y_RK4[i]
        y_true = y_analitica(x)

        # Calcular errores absolutos
        err_rk4 = abs(y_true - y_rk4)

        # Calcular errores relativos (porcentaje)
        # Evitar división por cero
        if abs(y_true) > 1e-15:
            pct_rk4 = (err_rk4 / abs(y_true)) * 100.0
        else:
            pct_rk4 = float('inf') if err_rk4 != 0 else 0.0

        # Crear fila con redondeo apropiado
        fila = (
            round(x, 1),                           # xn
            round(y_rk4, decimales),                 # ynRK4
            round(y_true, decimales),              # ValorReal
            round(err_rk4, decimales),               # ErrAbs_RK4
            round(pct_rk4, precision_porcentaje),    # %ErrRel_RK4
            # x,
            # y_rk4,
            # y_true,
            # err_rk4,
            # pct_rk4
        )
        tabla.append(fila)
    return tabla

def imprimir_tabla(tabla, h):
    encabezado = ("xn", "yn_RK4", "ValorReal","ErrAbs_RK4", "%ErrRel_RK4")
    
    print(f"\n{'='*80}")
    print(f"RESULTADOS PARA h = {h}")
    print(f"{'='*80}")
    
    # Imprimir encabezado
    print("{:<6} {:<12} {:<16} {:<12} {:<12}".format(*encabezado))
    print("-" * 80)
    
    # Imprimir datos
    for fila in tabla:
        print("{:<6} {:<12.4f} {:<16.4f} {:<12.4f} {:<12.4f}".format(*fila))

def main():
    """
    Función principal que ejecuta los métodos numéricos y genera reportes.
    """
    print("🔬 MÉTODOS NUMÉRICOS PARA ECUACIONES DIFERENCIALES")
    print("=" * 60)
    print("Problema: dA/dt = A(2.128 -0.0432A), A(0) = 0.24")
    print("Solución analítica: A(t) = (49.25925925925926)/ (1+204.2469135802469*math.exp(-2.128*t))")
    print("Métodos: RK4")
    print("=" * 60)
    
    # Parámetros del problema
    # Parámetros del problema
    A = 0.24
    t_inicial = 0.0
    t_final = 10
    hs = [0.5]

    for h in hs:
        print(f"\nProcesando con h = {h}...")
        
        # Aplicar métodos numéricos
        x_rk4, y_rk4 = rk4(f,t_inicial, A, h, t_final)
        x_vals = x_rk4

        # Generar tabla con parámetros mejorados
        tabla = generar_tabla(x_vals, y_rk4, decimales=4, precision_porcentaje=6)

        # Imprimir resultados con resumen estadístico
        imprimir_tabla(tabla, h)

        # ---- GRAFICAR RESULTADOS ----
        # Crear listas para la solución analítica
        y_real = [y_analitica(x) for x in x_vals]

        # Crear la figura
        plt.figure(figsize=(8, 5))
        plt.plot(x_vals, y_rk4, 'o-', label='RK4', color='blue')
        plt.plot(x_vals, y_real, '-', label='Analítica', color='red')
        plt.title(f'Crecimiento de colonia bacteriana (h={h})')
        plt.xlabel('t (días)')
        plt.ylabel('A (cm²)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    
    print("\n🎉 ¡Análisis completado!")

if __name__ == "__main__":
    main()

# print(rk4(f,t_inicial, A, h, t_final))
# print("Ahora analitica")
print(y_analitica(10))