import math
from solvers import euler, euler_mejorado

"""
Considere el problema con valores iniciales  
y' = (x + y - 1)^2, y(0) = 2  

Use el Método de Euler y el Método de Euler Mejorado ambos con h = 0.1 y h = 0.05 para obtener una aproximación de cuatro decimales de la solución en x = 0.5. En cada paso compare el valor aproximado con el valor real si la solución analítica es:  
y(x) = tan(x + π/4) - x + 1  

Para h = 0.1 y h = 0.05 reporte los resultados de cada paso en una tabla
xn ynEuler ynEulerMejorado ValorReal ErrorAbsoluto %deErrorRelativo
"""

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

def generar_tabla(x_vals, y_euler, y_euler_mej, decimales=4, precision_porcentaje=6):
    tabla = []
    for i, x in enumerate(x_vals):
        y_e = y_euler[i]
        y_em = y_euler_mej[i]
        y_true = y_analitica(x)

        # Calcular errores absolutos
        err_e = abs(y_true - y_e)
        err_em = abs(y_true - y_em)

        # Calcular errores relativos (porcentaje)
        # Evitar división por cero
        if abs(y_true) > 1e-15:
            pct_e = (err_e / abs(y_true)) * 100.0
            pct_em = (err_em / abs(y_true)) * 100.0
        else:
            pct_e = float('inf') if err_e != 0 else 0.0
            pct_em = float('inf') if err_em != 0 else 0.0

        # Crear fila con redondeo apropiado
        fila = (
            round(x, 8),                           # xn
            round(y_e, decimales),                 # ynEuler
            round(y_em, decimales),                # ynEulerMejorado
            round(y_true, decimales),              # ValorReal
            round(err_e, decimales),               # ErrAbs_Euler
            round(pct_e, precision_porcentaje),    # %ErrRel_Euler
            round(err_em, decimales),              # ErrAbs_EulerMej
            round(pct_em, precision_porcentaje)    # %ErrRel_EulerMej
        )
        tabla.append(fila)
    return tabla

def imprimir_tabla(tabla, h):
    encabezado = ("xn", "ynEuler", "ynEulerMejorado", "ValorReal",
                  "ErrAbs_Euler", "%ErrRel_Euler", "ErrAbs_EulerMej", "%ErrRel_EulerMej")
    
    print(f"\n{'='*80}")
    print(f"RESULTADOS PARA h = {h}")
    print(f"{'='*80}")
    
    # Imprimir encabezado
    print("{:<8} {:<12} {:<16} {:<12} {:<12} {:<14} {:<14} {:<14}".format(*encabezado))
    print("-" * 80)
    
    # Imprimir datos
    for fila in tabla:
        print("{:<8.4f} {:<12.4f} {:<16.4f} {:<12.4f} {:<12.4f} {:<14.6f} {:<14.4f} {:<14.6f}".format(*fila))
    

""" def _imprimir_resumen(tabla, h):
    #Imprime un resumen estadístico de los resultados.
    if not tabla:
        return
    
    # Extraer errores para estadísticas
    errores_euler = [fila[4] for fila in tabla[1:]]  # Saltar el primer punto (x=0)
    errores_euler_mej = [fila[6] for fila in tabla[1:]]
    porcentajes_euler = [fila[5] for fila in tabla[1:]]
    porcentajes_euler_mej = [fila[7] for fila in tabla[1:]]
    
    print(f"\n--- RESUMEN ESTADÍSTICO (h = {h}) ---")
    print(f"Método de Euler:")
    print(f"  Error absoluto máximo: {max(errores_euler):.6f}")
    print(f"  Error absoluto promedio: {sum(errores_euler)/len(errores_euler):.6f}")
    print(f"  Error relativo máximo: {max(porcentajes_euler):.4f}%")
    print(f"  Error relativo promedio: {sum(porcentajes_euler)/len(porcentajes_euler):.4f}%")
    
    print(f"\nMétodo de Euler Mejorado:")
    print(f"  Error absoluto máximo: {max(errores_euler_mej):.6f}")
    print(f"  Error absoluto promedio: {sum(errores_euler_mej)/len(errores_euler_mej):.6f}")
    print(f"  Error relativo máximo: {max(porcentajes_euler_mej):.4f}%")
    print(f"  Error relativo promedio: {sum(porcentajes_euler_mej)/len(porcentajes_euler_mej):.4f}%")
    
    # Comparación final
    valor_final = tabla[-1]
    print(f"\n--- COMPARACIÓN EN x = {valor_final[0]:.4f} ---")
    print(f"Valor real: {valor_final[3]:.6f}")
    print(f"Euler: {valor_final[1]:.6f} (error: {valor_final[4]:.6f}, {valor_final[5]:.4f}%)")
    print(f"Euler Mejorado: {valor_final[2]:.6f} (error: {valor_final[6]:.6f}, {valor_final[7]:.4f}%)") """

def main():
    """
    Función principal que ejecuta los métodos numéricos y genera reportes.
    """
    print("🔬 MÉTODOS NUMÉRICOS PARA ECUACIONES DIFERENCIALES")
    print("=" * 60)
    print("Problema: y' = (x + y - 1)², y(0) = 2")
    print("Solución analítica: y(x) = tan(x + π/4) - x + 1")
    print("Métodos: Euler y Euler Mejorado")
    print("=" * 60)
    
    # Parámetros del problema
    x0 = 0.0
    y0 = 2.0
    x_final = 0.5
    hs = [0.1, 0.05]

    for h in hs:
        print(f"\nProcesando con h = {h}...")
        
        # Aplicar métodos numéricos
        x_euler, y_euler = euler(f, x0, y0, h, x_final)
        x_em, y_em = euler_mejorado(f, x0, y0, h, x_final)
        x_vals = x_euler

        # Generar tabla con parámetros mejorados
        tabla = generar_tabla(x_vals, y_euler, y_em, decimales=4, precision_porcentaje=6)

        # Imprimir resultados con resumen estadístico
        imprimir_tabla(tabla, h)
    
    print(f"\n🎉 ¡Análisis completado!")

if __name__ == "__main__":
    main()