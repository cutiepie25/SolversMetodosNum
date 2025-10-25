import math
from solvers import rk4

# Parámetros del problema
x0 = 0.0
y0 = 2.0
x_final = 0.5

def f(x, y):
    y_prima = (x+y-1)**2
    return y_prima

def y_analitica(x: float) -> float:
    # Solución analítica: y(x) = tan(x + pi/4) - x + 1
    return math.tan(x + math.pi/4) - x + 1

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
    print("Problema: y' = (x + y - 1)², y(0) = 2")
    print("Solución analítica: y(x) = tan(x + π/4) - x + 1")
    print("Métodos: RK4")
    print("=" * 60)
    
    # Parámetros del problema
    x0 = 0.0
    y0 = 2.0
    x_final = 0.5
    hs = [0.1]

    for h in hs:
        print(f"\nProcesando con h = {h}...")
        
        # Aplicar métodos numéricos
        x_rk4, y_rk4 = rk4(f, x0, y0, h, x_final)
        x_vals = x_rk4

        # Generar tabla con parámetros mejorados
        tabla = generar_tabla(x_vals, y_rk4, decimales=4, precision_porcentaje=6)

        # Imprimir resultados con resumen estadístico
        imprimir_tabla(tabla, h)
    
    print(f"\n🎉 ¡Análisis completado!")

if __name__ == "__main__":
    main()