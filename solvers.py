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

def multipasos(f, x0, y0, h, x_final):
    x_actual = x0
    y_actual = y0

    # Almacenar los resultados
    x_valores = [x0]
    y_valores = [y0]
    y_rk4 = []

    for i in range(4):
        # Llamar a rk4 para UN SOLO PASO (x_final = x_actual + h)
        x_temp, y_temp = rk4(f, x_actual, y_actual, h, x_actual + h)
        # rk4 retorna listas, tomar el último valor
        x_siguiente = x_temp[-1]
        y_siguiente = y_temp[-1]

        y_rk4.append(y_siguiente)

        if(i == 3):
            break

        # Guardar
        x_valores.append(x_siguiente)
        y_valores.append(y_siguiente)
        x_actual = x_siguiente
        y_actual = y_siguiente

    f_hist = [f(x_valores[i], y_valores[i]) for i in range(4)]
    
    # Bucle principal: Predictor-Corrector
    while x_actual < x_final:
        # Predictor: Adams-Bashforth
        y_pred = y_actual + (h/24) * (55*f_hist[3] - 59*f_hist[2] + 37*f_hist[1] - 9*f_hist[0])
        x_siguiente = x_actual + h
        f_pred = f(x_siguiente, y_pred)
        # Corrector: Adams-Moulton
        y_corr = y_actual + (h/24) * (9*f_pred + 19*f_hist[3] - 5*f_hist[2] + f_hist[1])
        
        # Guardar y actualizar
        x_valores.append(x_siguiente)
        y_valores.append(y_corr)
        
        x_actual = x_siguiente
        y_actual = y_corr
        
        # Actualizar historial
        f_hist.pop(0)
        f_hist.append(f(x_actual, y_actual))
    print(f"Valores RK4 iniciales para h={h}: {y_rk4} para x = {[round(x,4) for x in x_valores[:4]]} y para y = {[round(y,4) for y in y_valores[:4]]}")
    return x_valores, y_valores, y_rk4
