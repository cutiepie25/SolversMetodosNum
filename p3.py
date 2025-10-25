from solvers import multipasos
"""Considere el problema con valores iniciales

y' = 2x - 3y + 1, y(0) = 1

Use el Método Multipasos de Adams-Bashforth-Moulton para aproximar con cuatro decimales y(0.8). Utilice h = 0.2 y el Método RK4 para calcular y₁, y₂, y₃. Reporte en una tabla los valores de RK4 obtenidos y después el valor del método Multipasos para y(0.8)."""

def f(x, y):
    y_prima = 2*x - 3*y + 1
    return y_prima

def generar_tabla(x_Vals, y_RK4, y_Vals, decimales=4):
    tabla = []
        
    for i in range(len(x_Vals)):
        y_vals = y_Vals[i]
        x_vals = x_Vals[i]
        # y_rk4 = y_RK4[i]

        if(len(x_Vals) <= len(y_RK4)):
            y_rk4 = y_RK4[i]
        else:
            y_rk4 = y_RK4[i-1]
        # Calcular errores absolutos


        # Calcular errores relativos (porcentaje)
        
        # Crear fila con redondeo apropiado
        fila = (                           # xn
            round(y_rk4, decimales),                 # ynRK4
            round(x_vals, decimales),               # ValorReal
            round(y_vals, decimales)
            # x,
            # y_rk4,
            # y_true,
            # err_rk4,
            # pct_rk4
        )
        tabla.append(fila)
    return tabla

def imprimir_tabla(tabla, h):
    encabezado = ("y_rk4", "x_Multi", "y_multi")
    
    print(f"\n{'='*80}")
    print(f"RESULTADOS PARA h = {h}")
    print(f"{'='*80}")
    
    # Imprimir encabezado
    print("{:<8} {:<12} {:<16}".format(*encabezado))
    print("-" * 80)
    
    # Imprimir datos
    for fila in tabla:
        print("{:<8.4f} {:<12.4f} {:<16.4f}".format(*fila))

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
    x0 = 0
    y0 = 1
    x_final = 0.8
    hs = [0.2]

    for h in hs:
        print(f"\nProcesando con h = {h}...")
        
        # Aplicar métodos numéricos
        x_multi, y_multi, y_rk4 = multipasos(f, x0, y0, h, x_final)
        

        # Generar tabla con parámetros mejorados
        tabla = generar_tabla(x_multi, y_rk4, y_multi, decimales=4)

        # Imprimir resultados con resumen estadístico
        imprimir_tabla(tabla, h)
    
    print(f"\n🎉 ¡Análisis completado!")

if __name__ == "__main__":
    main()