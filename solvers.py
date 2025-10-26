def euler(f, x0, y0, h, x_final):
    x_actual = x0
    y_actual = y0

    # Almacenar los resultados
    x_valores = [x0]
    y_valores = [y0]

    #Lógica
    while x_actual < x_final:
        pendiente = f(x_actual, y_actual)
        y_siguiente = y_actual + h * pendiente
        x_siguiente = x_actual + h

        x_actual = round(x_siguiente, 4)
        y_actual = y_siguiente

        x_valores.append(x_actual)
        y_valores.append(y_actual)
    return x_valores, y_valores

def euler_mejorado(f, x0, y0, h, x_final):
    x_actual = x0
    y_actual = y0

    # Almacenar los resultados
    x_valores = [x0]
    y_valores = [y0]

    #Lógica
    while x_actual < x_final:
        #Cálculos con K1
        k1 = f(x_actual, y_actual)
        y_asterisco = y_actual + h * k1
        x_siguiente = x_actual + h

        k2 = f(x_siguiente,y_asterisco)
        y_siguiente = y_actual + h/2 *(k1+k2)

        x_actual = round(x_siguiente, 4)
        y_actual = y_siguiente

        x_valores.append(x_actual)
        y_valores.append(y_actual)
    return x_valores, y_valores

def rk4(f, x0, y0, h, x_final):
    x_actual = x0
    y_actual = y0

    # Almacenar los resultados
    x_valores = [x0]
    y_valores = [y0]

    #Lógica
    while x_actual < x_final:
        #Cálculos con K1
        k1 = f(x_actual, y_actual)

        #Cálculos con K2

        y_asterisco = y_actual + h/2 * k1
        k2 = f(x_actual + h/2,y_asterisco)

        #Cálculos con K3
        y_asterisco = y_actual + h/2 * k2
        k3 = f(x_actual + h/2,y_asterisco)

        #Cálculos con K4
        y_asterisco = y_actual + h * k3
        k4 = f(x_actual + h,y_asterisco)

        y_siguiente = y_actual + h/6 *(k1+2*k2+2*k3+k4)

        x_actual += h
        y_actual = y_siguiente

        x_valores.append(x_actual)
        y_valores.append(y_actual)
    return x_valores, y_valores


def adams_bashforth_moulton(f, x0, y0, h, x_final):
    """
    Método Multipasos de Adams-Bashforth-Moulton de orden 4
    
    Este es un método PREDICTOR-CORRECTOR que combina:
    - Adams-Bashforth (predictor): método explícito
    - Adams-Moulton (corrector): método implícito
    
    Parámetros:
    -----------
    f : función
        La derivada dy/dx = f(x, y)
    x0, y0 : float
        Condición inicial y(x0) = y0
    h : float
        Tamaño del paso
    x_final : float
        Valor final de x donde queremos llegar
    
    Retorna:
    --------
    x_valores, y_valores : listas
        Los valores de x y y en cada paso
    
    CÓMO FUNCIONA:
    --------------
    1. INICIALIZACIÓN (con RK4):
       Necesitamos 4 valores iniciales: y₀, y₁, y₂, y₃
       Usamos el método RK4 existente para calcular y₁, y₂, y₃ con alta precisión
    
    2. PASO PREDICTOR (Adams-Bashforth de 4 pasos):
       Usa los últimos 4 valores conocidos para PREDECIR el siguiente
       
       y_{n+1}^P = y_n + (h/24)[55f_n - 59f_{n-1} + 37f_{n-2} - 9f_{n-3}]
       
       Los coeficientes (55, -59, 37, -9) vienen de interpolación polinomial
    
    3. PASO CORRECTOR (Adams-Moulton de 3 pasos):
       Usa la predicción para CORREGIR y obtener un valor más preciso
       
       y_{n+1}^C = y_n + (h/24)[9f_{n+1}^P + 19f_n - 5f_{n-1} + f_{n-2}]
       
       Los coeficientes (9, 19, -5, 1) también vienen de interpolación
    
    4. ITERACIÓN:
       Repetimos predictor-corrector hasta llegar a x_final
    """
    
    # ========== FASE 1: INICIALIZACIÓN CON RK4 ==========
    # Necesitamos 4 puntos para comenzar el método multipasos
    # Reutilizamos el método rk4() que ya tenemos implementado
    print("🔧 Inicializando con RK4 para obtener y₁, y₂, y₃...")
    
    # Calcular hasta x0 + 3h para obtener los primeros 4 puntos (y₀, y₁, y₂, y₃)
    x_valores, y_valores = rk4(f, x0, y0, h, x0 + 3*h)
    
    # ========== FASE 2: MÉTODO MULTIPASOS ABM ==========
    print("🚀 Aplicando Adams-Bashforth-Moulton...")
    
    # Necesitamos mantener los últimos 4 valores de f(x,y)
    # Calculamos f para los 4 primeros puntos
    f_valores = [f(x_valores[i], y_valores[i]) for i in range(4)]
    
    x_actual = x_valores[-1]  # Último x calculado con RK4
    
    # Continuar desde x₃ hasta x_final
    while x_actual < x_final - h/2:  # Pequeña tolerancia para errores de redondeo
        # --- PASO PREDICTOR (Adams-Bashforth de 4 pasos) ---
        # Fórmula: y_{n+1}^P = y_n + (h/24)[55f_n - 59f_{n-1} + 37f_{n-2} - 9f_{n-3}]
        
        y_predicho = y_valores[-1] + (h/24) * (
            55 * f_valores[-1]   # f_n (más reciente)
            - 59 * f_valores[-2]  # f_{n-1}
            + 37 * f_valores[-3]  # f_{n-2}
            - 9 * f_valores[-4]   # f_{n-3}
        )
        
        x_siguiente = x_actual + h
        
        # Calcular f en el punto predicho
        f_predicho = f(x_siguiente, y_predicho)
        
        # --- PASO CORRECTOR (Adams-Moulton de 3 pasos) ---
        # Fórmula: y_{n+1}^C = y_n + (h/24)[9f_{n+1}^P + 19f_n - 5f_{n-1} + f_{n-2}]
        
        y_corregido = y_valores[-1] + (h/24) * (
            9 * f_predicho        # f_{n+1} usando y predicho
            + 19 * f_valores[-1]  # f_n
            - 5 * f_valores[-2]   # f_{n-1}
            + f_valores[-3]       # f_{n-2}
        )
        
        # Guardar los nuevos valores
        x_valores.append(x_siguiente)
        y_valores.append(y_corregido)
        
        # Actualizar f_valores: eliminar el más antiguo y agregar el nuevo
        f_nuevo = f(x_siguiente, y_corregido)
        f_valores.pop(0)  # Eliminar f_{n-3}
        f_valores.append(f_nuevo)  # Agregar f_{n+1}
        
        x_actual = x_siguiente
    
    return x_valores, y_valores