# Análisis Exploratorio del Mercado de Videojuegos

Proyecto de análisis de datos en Python utilizando `pandas`, `numpy`, `matplotlib` y `seaborn` sobre tendencias de la industria de los videojuegos (`gaming_industry_trends.csv`).

## Integrantes
* **Juan Diego Hernández Pérez** (Ítems 1, 3, 5, 7 y 9)
* **Andrés Joel Cantor Acosta** (Ítems 2, 4, 6 y 8)

## Estructura del Repositorio
```text
Proyecto-/
├── README.md
├── analisis.py                        # Script unificado con celdas interactivas (# %%)
├── datos/
│   └── gaming_industry_trends.csv     # Dataset principal (1,000 registros, 11 variables)
└── cuadernos/
    ├── exploracion_juan.ipynb         # Cuaderno individual Juan Diego
    └── exploracion_joel.ipynb         # Cuaderno individual Andrés Joel

```

## Documentación y Estructura de los Datos
El archivo `datos/gaming_industry_trends.csv` contiene **1,000 filas (registros de videojuegos)** y **11 columnas originales** (sin valores nulos ni registros duplicados), complementadas con **2 variables derivadas** durante el análisis (`Revenue_per_Player` y `Engagement_Ratio`):

### Diccionario de la Base de Datos

| Variable | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `Game Title` | Texto (`str`) | Nombre o título del videojuego analizado (50 títulos únicos). |
| `Genre` | Texto (`str`) | Género principal del videojuego (`Action`, `Adventure`, `Fighting`, `Horror`, `Puzzle`, `RPG`, `Racing`, `Shooter`, `Simulation`, `Strategy`). |
| `Platform` | Texto (`str`) | Plataforma tecnológica de lanzamiento (`PlayStation`, `PC`, `Cross-Platform`, `Xbox`, `Mobile`, `Nintendo Switch`). |
| `Release Year` | Numérico (`int`) | Año de lanzamiento del videojuego. |
| `Developer` | Texto (`str`) | Estudio o empresa desarrolladora del título (10 desarrolladores principales como `Sony`, `Activision`, `Rockstar`, `Microsoft`, `Ubisoft`, entre otros). |
| `Revenue (Millions $)` | Numérico (`float`) | Ingresos totales generados por el título expresados en millones de dólares (USD). |
| `Players (Millions)` | Numérico (`float`) | Base total de jugadores registrados o activos en millones. |
| `Peak Concurrent Players` | Numérico (`float`) | Máximo histórico de jugadores conectados simultáneamente (expresado en miles). |
| `Metacritic Score` | Numérico (`float`) | Calificación promedio otorgada por la crítica especializada en Metacritic (escala de 0 a 100). |
| `Esports Popularity` | Numérico (`float` / `int`) | Índice o nivel de popularidad del título en competencias de deportes electrónicos (Esports). |
| `Trending Status` | Texto (`str`) | Estado actual de tendencia del juego en el mercado (`Rising`, `Stable`, `Declining`). |
| `Revenue_per_Player` *(creada)* | Numérico (`float`) | Ingreso promedio en dólares generado por cada jugador (`Revenue / Players`). |
| `Engagement_Ratio` *(creada)* | Numérico (`float`) | Porcentaje de la base total de jugadores que coincide simultáneamente en horas pico. |

## Ejecución del Análisis
1. Abrir `analisis.py` en Visual Studio Code con las extensiones **Python** y **Jupyter** habilitadas.
2. Hacer clic en **Ejecutar a continuación** (*Run Below*) en la primera celda (`# %% [markdown]`) para ejecutar todo el flujo de análisis de arriba abajo.

## Principales Hallazgos
1. **Integridad de los Datos:** La base cuenta con 1,000 registros completos (0 nulos y 0 duplicados) y categorías consistentes en todas las columnas textuales.
2. **Casos Atípicos Validados:** Se detectaron dos valores atípicos superiores en `Peak Concurrent Players` (*Legends of Valor 5* con 96.62 mil y *Warzone Chronicles 1* con 96.26 mil, por encima del límite IQR de 95.60 mil), conservados por representar éxitos reales de *Sports* y *Fighting*.
3. **Rentabilidad por Género:** *Action* lidera los ingresos acumulados ($\$291,375.92\text{ M}$ USD), mientras que *RPG* obtiene el mejor ingreso promedio por título ($\$2,716.13\text{ M}$ USD) y *Fighting* logra la mayor monetización por usuario ($\$194.36$ USD/jugador).
4. **Equilibrio del Mercado:** El catálogo se divide prácticamente en tercios iguales entre juegos estables (`Stable`: 33.9 %), en crecimiento (`Rising`: 33.5 %) y en declive (`Declining`: 32.6 %), con distribución homogénea entre plataformas y desarrolladores.

Mejorar el manejo del iloc
