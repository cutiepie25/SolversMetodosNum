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
    # Inicialización con RK4 para obtener y0, y1, y2, y3
    
    x_valores, y_valores = rk4(f, x0, y0, h, x0 + 3*h)
    
   
    f_valores = [f(x_valores[i], y_valores[i]) for i in range(4)]
    
    x_actual = x_valores[-1]  # Último x calculado con RK4
    
    # Continuar desde x₃ hasta x_final
    while x_actual < x_final - h/2:
        
        y_predicho = y_valores[-1] + (h/24) * (
            55 * f_valores[-1]   # f_n (más reciente)
            - 59 * f_valores[-2]  # f_{n-1}
            + 37 * f_valores[-3]  # f_{n-2}
            - 9 * f_valores[-4]   # f_{n-3}
        )
        
        x_siguiente = x_actual + h
        
        # Calcular f en el punto predicho
        f_predicho = f(x_siguiente, y_predicho)
        
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


def rk4_sistema(f_sistema, t0, y0_vector, h, t_final):
    """
    Método RK4 adaptado para sistemas de ecuaciones diferenciales.
    
    PROBLEMA QUE RESUELVE:
    ----------------------
    Los métodos anteriores (euler, rk4, etc.) resuelven ecuaciones de la forma:
        dy/dt = f(t, y)  donde y es un ESCALAR (un solo valor)
    
    Este método resuelve SISTEMAS de ecuaciones de la forma:
        dy₁/dt = f₁(t, y₁, y₂, ..., yₙ)
        dy₂/dt = f₂(t, y₁, y₂, ..., yₙ)
        ...
        dyₙ/dt = fₙ(t, y₁, y₂, ..., yₙ)
    
    donde Y = [y₁, y₂, ..., yₙ] es un VECTOR (lista de valores)
    
    EJEMPLO DE USO - PÉNDULO:
    --------------------------
    Ecuación original (segundo orden):
        d²θ/dt² + (g/l)sen(θ) = 0
    
    Se convierte en sistema (primer orden):
        y₁ = θ           (posición angular)
        y₂ = dθ/dt       (velocidad angular)
        
        dy₁/dt = y₂
        dy₂/dt = -(g/l)sen(y₁)
    
    Uso:
        def f(t, y):
            return [y[1], -(g/l)*sin(y[0])]
        
        t, y = rk4_sistema(f, 0, [1.0, 2.0], 0.01, 10)
        theta = [y[i][0] for i in range(len(y))]  # Extraer θ(t)
        omega = [y[i][1] for i in range(len(y))]  # Extraer ω(t)
    
    PARÁMETROS:
    -----------
    f_sistema : función
        Función que retorna una LISTA con las derivadas
        f_sistema(t, [y₁, y₂, ...]) -> [dy₁/dt, dy₂/dt, ...]
    
    t0 : float
        Tiempo inicial
    
    y0_vector : list
        Vector de condiciones iniciales [y₁(0), y₂(0), ...]
        Ejemplo: [1.0, 2.0] significa y₁(0)=1.0, y₂(0)=2.0
    
    h : float
        Tamaño del paso temporal
    
    t_final : float
        Tiempo final de integración
    
    RETORNA:
    --------
    t_valores : list
        Lista de tiempos [t₀, t₁, t₂, ...]
    
    y_valores : list de listas
        y_valores[i] = [y₁(tᵢ), y₂(tᵢ), ...]
        Ejemplo: y_valores[0] = [1.0, 2.0] (condición inicial)
                 y_valores[1] = [1.02, 1.95] (primer paso)
    
    ALGORITMO RK4 PARA SISTEMAS:
    -----------------------------
    El algoritmo es idéntico al RK4 escalar, pero cada operación
    se hace componente por componente:
    
    Para cada paso:
        k₁ = h * f(tₙ, Yₙ)
        k₂ = h * f(tₙ + h/2, Yₙ + k₁/2)
        k₃ = h * f(tₙ + h/2, Yₙ + k₂/2)
        k₄ = h * f(tₙ + h, Yₙ + k₃)
        
        Yₙ₊₁ = Yₙ + (k₁ + 2k₂ + 2k₃ + k₄)/6
    
    Donde cada k es un VECTOR [k₁_y₁, k₁_y₂, ...] y las operaciones
    como Yₙ + k₁/2 se hacen componente por componente.
    """
    
    t_actual = t0
    y_actual = y0_vector[:]  # Copiar el vector inicial
    
    # Almacenar resultados
    t_valores = [t0]
    y_valores = [y0_vector[:]]  # Guardar copia del vector inicial
    
    # Número de ecuaciones en el sistema
    n = len(y0_vector)
    
    # Iterar hasta alcanzar t_final
    while t_actual < t_final - h/2:  # Tolerancia para errores de redondeo
        
        # ========== K1 = h * f(t, Y) ==========
        f_actual = f_sistema(t_actual, y_actual)
        k1 = [h * f_actual[i] for i in range(n)]
        
        # ========== K2 = h * f(t + h/2, Y + k1/2) ==========
        y_temp = [y_actual[i] + k1[i]/2 for i in range(n)]
        f_temp = f_sistema(t_actual + h/2, y_temp)
        k2 = [h * f_temp[i] for i in range(n)]
        
        # ========== K3 = h * f(t + h/2, Y + k2/2) ==========
        y_temp = [y_actual[i] + k2[i]/2 for i in range(n)]
        f_temp = f_sistema(t_actual + h/2, y_temp)
        k3 = [h * f_temp[i] for i in range(n)]
        
        # ========== K4 = h * f(t + h, Y + k3) ==========
        y_temp = [y_actual[i] + k3[i] for i in range(n)]
        f_temp = f_sistema(t_actual + h, y_temp)
        k4 = [h * f_temp[i] for i in range(n)]
        
        # ========== Y_nuevo = Y + (k1 + 2k2 + 2k3 + k4)/6 ==========
        y_siguiente = [
            y_actual[i] + (k1[i] + 2*k2[i] + 2*k3[i] + k4[i])/6
            for i in range(n)
        ]
        
        t_actual += h
        y_actual = y_siguiente
        
        # Guardar resultados
        t_valores.append(round(t_actual, 3))
        y_valores.append(y_actual[:])
    
    return t_valores, y_valores