# SolversMetodosNum

Proyecto de **Métodos Numéricos**: implementación en Python de métodos para resolver **ecuaciones diferenciales ordinarias (EDO)** con valor inicial, aplicados a cinco problemas. Se comparan con la solución analítica cuando existe.

## Métodos (`solvers.py`)

| Función | Método |
|---------|--------|
| `euler(f, x0, y0, h, x_final)` | Método de Euler |
| `euler_mejorado(f, x0, y0, h, x_final)` | Euler mejorado (Heun) |
| `rk4(f, x0, y0, h, x_final)` | Runge-Kutta de orden 4 |
| `adams_bashforth_moulton(f, x0, y0, h, x_final)` | Predictor-corrector multipaso de Adams-Bashforth-Moulton (arranca con RK4) |
| `rk4_sistema(f_sistema, t0, y0_vector, h, t_final)` | RK4 para sistemas de EDO (vectorial) |

## Problemas

| Script | Problema |
|--------|----------|
| `p1.py` | $y' = (x + y - 1)^2,\ y(0) = 2$. Euler y Euler mejorado con $h = 0.1$ y $h = 0.05$ hasta $x = 0.5$; tabla con error absoluto y relativo frente a $y(x) = \tan(x + \pi/4) - x + 1$ |
| `p2.py` | El mismo problema de `p1.py`, resuelto con RK4 |
| `p3.py` | $y' = 2x - 3y + 1,\ y(0) = 1$. Adams-Bashforth-Moulton con $h = 0.2$ para $y(0.8)$, usando RK4 para $y_1, y_2, y_3$ |
| `p4.py` | Crecimiento de una colonia de bacterias $dA/dt = A(2.128 - 0.0432A),\ A(0) = 0.24$ en $[0, 10]$, con gráfica |
| `p5.py` | Péndulo no lineal $\theta'' + (g/l)\sin\theta = 0$ en la Tierra ($g = 32$) y en la Luna ($0.165g$), con $l = 3$, $\theta(0) = 1$, $\theta'(0) = 2$. Se pasa a un sistema de primer orden y se resuelve con `rk4_sistema`; compara periodo y amplitud |

El enunciado completo está en `Proyecto_MetodosNumericosA.pdf`.

## Uso

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt

python p1.py
python p2.py
python p3.py
python p4.py   # abre una gráfica
python p5.py   # abre gráficas Tierra vs Luna
```

## Tecnologías

Python 3, NumPy, pandas, Matplotlib.
