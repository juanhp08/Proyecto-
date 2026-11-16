# %% [markdown]
# # Proyecto Programación II: Análisis del Mercado de Videojuegos
# Integrantes: Juan Diego Hernández Pérez y Andrés Joel Cantor Acosta

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("datos/gaming_industry_trends.csv")

# %% [markdown]
# ## 1. Carga e inspección inicial de los datos (Integrante A)

# %%
print("--- 1. TAMAÑO DEL CONJUNTO ---")
print(df.shape)

print("\n--- 2. TIPOS DE VARIABLES Y ESTRUCTURA ---")
df.info()

print("\n--- 3. DESCRIPCIÓN ESTADÍSTICA ---")
display(df.describe())

# %% [markdown]
# **Conclusión (Ítem 1):** El conjunto de datos contiene exactamente 1,000 registros (filas) y 11 variables (columnas): 5 de tipo texto/categórico (`Game Title`, `Genre`, `Platform`, `Developer`, `Trending Status`) y 6 numéricas (`Release Year`, `Revenue (Millions $)`, `Players (Millions)`, `Peak Concurrent Players`, `Metacritic Score`, `Esports Popularity`), sin pérdida de registros en su estructura inicial.

# %% [markdown]
# ## 2. Manejo de datos faltantes (Integrante B)

# %%
print("2. Valores faltantes por columna:")
print(df.isnull().sum())

print("\nTotal de celdas vacías en el dataset:", df.isnull().sum().sum())

print(" Visualización de datos faltantes con un mapa de calor")
plt.figure(figsize=(12, 6))
sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
plt.title("Mapa de calor de datos faltantes - gaming_industry_trends.csv")
plt.xlabel("Variables del dataset")
plt.ylabel("Registros (filas)")
plt.show()

print("Valores nulos después del tratamiento:")
print(df.isnull().sum().sum())

# %% [markdown]
# **Conclusión (Ítem 2):** Al realizar la inspección cuantitativa y el mapa de calor de valores faltantes, se encontró que el conjunto de datos `gaming_industry_trends.csv` cuenta con un total de **0 datos faltantes** en todas sus variables y registros. Dado que la integridad del dataset es completa (100 % de los datos presentes), no es necesario aplicar técnicas de imputación ni eliminar filas o columnas, manteniendo intactas las observaciones originales.

# %% [markdown]
# ## 3. Identificación de outliers (Integrante A)

# %%
columnas_numericas = [
    'Revenue (Millions $)',
    'Players (Millions)',
    'Peak Concurrent Players',
    'Metacritic Score'
]

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for i, col in enumerate(columnas_numericas):
    sns.boxplot(y=df[col], ax=axes[i], color='skyblue')
    axes[i].set_title(f'Boxplot de {col}')
    axes[i].set_ylabel('')

plt.tight_layout()
plt.show()

q1 = df['Peak Concurrent Players'].quantile(0.25)
q3 = df['Peak Concurrent Players'].quantile(0.75)
iqr = q3 - q1

limite_superior = q3 + 1.5 * iqr

outliers_peak = df[df['Peak Concurrent Players'] > limite_superior]

print(f"Límite superior calculado: {limite_superior:.2f}")
print("--- JUEGO(S) CON VALORES ATÍPICOS EN JUGADORES SIMULTÁNEOS ---")
display(outliers_peak[['Game Title', 'Genre', 'Platform', 'Peak Concurrent Players']])

# %% [markdown]
# **Conclusión (Ítem 3):** Mediante los diagramas de caja y el criterio del rango intercuartílico ($Q_3 + 1.5 \times IQR = 95.60$ mil), se detectaron únicamente 2 valores atípicos superiores en la variable `Peak Concurrent Players`: *Legends of Valor 5* (96.62 mil) y *Warzone Chronicles 1* (96.26 mil). Se decidió conservarlos en el `DataFrame` porque corresponden a éxitos comerciales reales de los géneros *Sports* y *Fighting* y no a errores de captura.

# %% [markdown]
# ## 4. Valores inconsistentes y duplicados (Integrante B)

# %%
print("4. Valores inconsistentes y duplicados")

duplicados_totales = df.duplicated().sum()
print(f"Cantidad de registros duplicados encontrados: {duplicados_totales}")
if duplicados_totales > 0:
    df = df.drop_duplicates()
    print("¡Registros duplicados eliminados exitosamente!")
else:
    print("No se encontraron registros duplicados en el dataset.")

columnas_texto = df.select_dtypes(include=['object', 'string']).columns

resumen_texto = pd.DataFrame({
    'Columna': columnas_texto,
    'Valores Únicos': [df[col].nunique() for col in columnas_texto],
    'Ejemplos de Categorías': [", ".join(df[col].unique()[:6]) for col in columnas_texto]
})

print("\n--- Resumen de columnas de texto en el dataset ---")
display(resumen_texto)
# %% [markdown]
# **Conclusión (Ítem 4):** Se verificó que existen **0 filas duplicadas** en el dataset. Asimismo, mediante la inspección de valores únicos en las columnas categóricas (`Game Title`, `Genre`, `Platform`, `Developer` y `Trending Status`), se comprobó que las categorías están debidamente estandarizadas, sin errores tipográficos ni duplicidades por variaciones de mayúsculas o espacios sobrantes.

# %% [markdown]
# ## 5. Creación de variables (Integrante A)

# %%
df['Revenue_per_Player'] = df['Revenue (Millions $)'] / df['Players (Millions)']

df['Engagement_Ratio'] = ((df['Peak Concurrent Players'] / 1000) / df['Players (Millions)']) * 100

display(df[['Game Title', 'Genre', 'Revenue (Millions $)', 'Players (Millions)', 'Revenue_per_Player', 'Engagement_Ratio']].head())

# %% [markdown]
# **Conclusión (Ítem 5):** Se incorporaron dos métricas derivadas al `DataFrame`: `Revenue_per_Player` (ingreso promedio en USD generado por cada jugador activo) y `Engagement_Ratio` (porcentaje de la base total de jugadores que se conecta de forma simultánea en horas pico), permitiendo evaluar la rentabilidad y fidelidad por título más allá de los volúmenes brutos.

# %% [markdown]
# ## 6. Filtrado y condiciones en pandas (Integrante B)

# %%
print("6. Filtrado y selección condicional de datos")

filtro_rising = df[df['Trending Status'] == 'Rising']
print(f"1. Juegos con tendencia 'Rising': {len(filtro_rising)}")

filtro_pc = df[df['Platform'] == 'PC']
print(f"2. Juegos en la plataforma PC: {len(filtro_pc)}")

filtro_strategy = df[df['Genre'] == 'Strategy']
print(f"3. Juegos del género Strategy: {len(filtro_strategy)}")

filtro_microsoft = df[df['Developer'] == 'Microsoft']
print(f"4. Juegos desarrollados por Microsoft: {len(filtro_microsoft)}")

filtro_stable = df[df['Trending Status'] == 'Stable']
print(f"5. Juegos con tendencia 'Stable': {len(filtro_stable)}")

# %% [markdown]
# **Conclusión (Ítem 6):** Se aplicaron 5 filtros condicionales sobre el `DataFrame` para aislar segmentos clave del mercado: 335 juegos en tendencia `Rising`, 174 en plataforma `PC`, 116 del género `Strategy`, 106 desarrollados por `Microsoft` y 339 con tendencia `Stable`, facilitando consultas puntuales sobre cada categoría.

# %% [markdown]
# ## 7. Agrupación con groupby (Integrante A)

# %%
print("--- 1. Ingresos Totales (Millones $) por Género ---")
display(df.groupby('Genre')['Revenue (Millions $)'].agg(['sum', 'mean']).rename(columns={'sum': 'Ingreso Total', 'mean': 'Ingreso Promedio'}))

print("\n--- 2. Mediana de Calificación Metacritic por Plataforma ---")
display(df.groupby('Platform')['Metacritic Score'].median().reset_index())

print("\n--- 3. Monetización Promedio (USD/Jugador) por Género ---")
display(df.groupby('Genre')['Revenue_per_Player'].mean().reset_index().sort_values(by='Revenue_per_Player', ascending=False))

print("\n--- 4. Tasa de Enganche Promedio (%) por Plataforma ---")
display(df.groupby('Platform')['Engagement_Ratio'].mean().reset_index())

print("\n--- 5. Máximo Pico de Jugadores Simultáneos (Miles) por Género ---")
display(df.groupby('Genre')['Peak Concurrent Players'].max().reset_index().sort_values(by='Peak Concurrent Players', ascending=False))

# %% [markdown]
# **Conclusión (Ítem 7):** Las agrupaciones revelan que, aunque *Action* lidera los ingresos totales acumulados ($\$291,375.92\text{ M}$ USD), *RPG* obtiene el mejor ingreso promedio por título ($\$2,716.13\text{ M}$ USD) y *Fighting* logra la mayor monetización por usuario ($\$194.36$ USD/jugador). Por plataforma, el enganche simultáneo es homogéneo, destacando *Mobile* y *PC* en las mejores medianas de calificación Metacritic.

# %% [markdown]
# ## 8. Visualizaciones (Integrante B)

# %%
print("8. Visualizaciones")

print("Gráfico 1: Distribución de juegos por Género (Gráfico de Barras)")
plt.figure(figsize=(10, 4))
sns.countplot(data=df, x='Genre', palette='viridis', order=df['Genre'].value_counts().index)
plt.title("Gráfico 1: Cantidad de juegos por Género")
plt.xlabel("Género")
plt.ylabel("Cantidad")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %% [markdown]
# **Conclusión (Gráfico 1):** El diagrama de barras muestra claramente cuáles son los géneros con mayor representación en el mercado de videojuegos, permitiendo identificar las preferencias de desarrollo, lideradas por *Action* (122 títulos) frente a nichos como *RPG* (78 títulos).

# %%
print("Gráfico 2: Distribución de juegos por Plataforma (Gráfico de Conteo)")

plt.figure(figsize=(10, 4))
sns.countplot(data=df, x='Platform', palette='magma', order=df['Platform'].value_counts().index)
plt.title("Gráfico 2: Distribución de juegos por Plataforma")
plt.xlabel("Plataforma")
plt.ylabel("Cantidad de Registros")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %% [markdown]
# **Conclusión (Gráfico 2):** Este gráfico permite visualizar qué plataformas tecnológicas albergan la mayor cantidad de títulos, evidenciando el alcance equilibrado de cada una de ellas (*PlayStation*, *PC*, *Cross-Platform*, *Xbox*, *Mobile* y *Nintendo Switch*).

# %%
print("Gráfico 3:Proporción del Estado de Tendencia (Gráfico Circular / Pie Chart)")

plt.figure(figsize=(6, 6))
conteo_status = df['Trending Status'].value_counts()

plt.pie(
    conteo_status,
    labels=conteo_status.index,
    autopct='%1.1f%%',
    colors=sns.color_palette('pastel'),
    startangle=140
)
plt.title("Gráfico 3: Proporción por Estado de Tendencia")
plt.tight_layout()
plt.show()

# %% [markdown]
# **Conclusión (Gráfico 3):** La visualización expone el comportamiento general del mercado (cuántos títulos se encuentran estables, en ascenso o declive), repartido prácticamente en tercios iguales (*Stable*: 33.9 %, *Rising*: 33.5 % y *Declining*: 32.6 %).

# %%
print("Gráfico 4: Cantidad de juegos por Desarrollador Principal")

plt.figure(figsize=(12, 5))
sns.countplot(data=df, y='Developer', palette='coolwarm', order=df['Developer'].value_counts().index[:10])
plt.title("Gráfico 4: Top Desarrolladores en el Dataset")
plt.xlabel("Cantidad de Juegos")
plt.ylabel("Desarrollador")
plt.tight_layout()
plt.show()

# %% [markdown]
# **Conclusión (Gráfico 4):** El gráfico de barras horizontales muestra los principales estudios o casas desarrolladoras con mayor presencia en el conjunto de datos (*Sony*, *Activision*, *Rockstar*, *Microsoft*, *Ubisoft*, entre otros).

# %%
print("Gráfico 5: Relación entre Género y Estado de Tendencia")

plt.figure(figsize=(12, 5))
sns.countplot(data=df, x='Genre', hue='Trending Status', palette='Set2')
plt.title("Gráfico 5: Estado de Tendencia por cada Género de Videojuego")
plt.xlabel("Género")
plt.ylabel("Cantidad de Registros")
plt.xticks(rotation=45)
plt.legend(title="Trending Status")
plt.tight_layout()
plt.show()

# %% [markdown]
# **Conclusión (Gráfico 5):** Al cruzar cada género con su estado de tendencia, se confirma que todas las categorías mantienen una proporción equilibrada de títulos en ascenso, estables y en declive, sin que ningún género concentre exclusivamente caídas de mercado.

# %% [markdown]
# ## 9. Conclusiones finales (Integrante A)
#
# 1. **Integridad y Calidad Estructural de los Datos:** Mediante la inspección inicial (Ítem 1), el mapa de calor de nulos (Ítem 2) y la revisión de duplicados y categorías (Ítem 4), comprobamos que los 1,000 registros vienen completos y bien estandarizados. Como no hubo que borrar filas ni rellenar datos vacíos, los cálculos se mantuvieron fieles a la base original.
# 2. **Validación de Casos Atípicos como Éxitos de Mercado:** Con los diagramas de caja y el rango intercuartílico (Ítem 3) encontramos dos valores que se salían de lo normal en el pico de jugadores simultáneos (*Legends of Valor 5* con 96.62 mil y *Warzone Chronicles 1* con 96.26 mil). Decidimos no eliminarlos porque al cruzarlos en el Ítem 7 vimos que corresponden a los picos máximos reales de *Sports* y *Fighting*, por lo que representan juegos muy exitosos y no errores de registro.
# 3. **Volumen de Oferta frente a Rentabilidad Individual:** Aunque *Action* es el género con más juegos en el catálogo (122 títulos, Gráfico 1) y el que más dinero suma en total ($\$291,375.92\text{ M}$ USD, Ítem 7), los juegos de tipo *RPG* logran el mejor promedio de ingresos por título ($\$2,716.13\text{ M}$ USD) aun siendo el género con menos lanzamientos (78). Además, las nuevas variables del Ítem 5 mostraron que *Fighting* es el género que más dinero saca por cada jugador ($\$194.36$ USD).
# 4. **Equilibrio en la Dinámica de Mercado y Plataformas:** Tanto los filtros del Ítem 6 como el gráfico circular (Gráfico 3) muestran que el mercado está repartido casi en tercios iguales entre juegos estables (*Stable*: 33.9 %, 339 juegos), en subida (*Rising*: 33.5 %, 335 juegos) y en bajada (*Declining*: 32.6 %). Algo parecido pasa con las plataformas: todas tienen una cantidad similar de juegos (Gráfico 2) y una tasa de enganche (`Engagement_Ratio`, Ítem 7) muy pareja, aunque *Mobile* y *PC* se llevan las mejores notas en Metacritic.
# 5. **Concentración de la Industria y Comportamiento por Género:** La producción de los juegos del dataset se reparte de manera balanceada entre los distintos estudios desarrolladores (Gráfico 4) y, al cruzar cada género con su estado de tendencia (Gráfico 5), se confirma que ninguna categoría sufre caídas exclusivas; el crecimiento y el declive ocurren de forma transversal en toda la industria.