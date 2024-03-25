# -*- coding: utf-8 -*-
# Ashley Dafne Aguilar Salinas
#Mario Alberto Martinez Oliveros

"""Proyecto_Estadistica.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1V1iC28S-DQp4ZCl_lzk4jEReTpBJYmx7

"""

"""# Librerías
"""
!pip install factor_analyzer

# Commented out IPython magic to ensure Python compatibility.
import random
import numpy as np
import pandas as pd
from pandas import Series
import scipy.stats as sts
from numpy.linalg import det, inv

# %matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d


from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances_argmin_min

import factor_analyzer
from factor_analyzer.factor_analyzer import FactorAnalyzer

"""# Datos

## Carga y visualización
"""

from google.colab import drive
drive.mount('/content/drive')

#Cargamos los datos
# y los visualizamos

dataset = pd.read_csv('/content/drive/MyDrive/Proyectos/Estadistica_multivariada/Cancer_Data.csv'); dataset

# Obtenemos informacion general
# del conjunto de datos
dataset.info()

dataset.describe()

"""## Limpieza de los datos"""

# Creamoos una copia del conjunto
# de datos original para no modificarlo
# directamente
df = dataset.copy()

# Obtenemos en numero de los datos nulos
# que existen en el conjunto de
# datos
df.isnull().sum()

# Obtenemos el tipo de datos con
# los que estamos trabajando en el
#conjunto de datos
df.dtypes

"""### Modificaciones al conjunto de datos

1. Se eliminará la columna ***id***, pues no se considera información importante
"""

# Eliminamos la columna id del
# conjunto de datos
df.drop('id', axis = 1, inplace = True)

"""2. Eliminaremos la columna ***Unnamed: 32*** por falta de datos."""

# Eliminamos la columna Unnamed: 32 del
# conjunto de datos
df.drop('Unnamed: 32', axis = 1, inplace = True)

"""3. Eliminamos la columna **diagnosis**, variable cualitativa que nos dice el tipo de cáncer que es (Maligno o Benigno)"""

# Guardamos la informacion de diagnosis
# en una variable y Eliminamos la columna
#diagnosis del conjunto de datos
diagnosis = df.diagnosis
df.drop('diagnosis', axis = 1, inplace = True)

# Obtenemos el numero de
# filas y columnas despues de
# las modificaciones
df.shape

df

"""### Estadarizar
Se decide estandarizar los datos para que los datos tengan el mismo formato y evitar errores como que los datos estén en diferentes unidades de medida.

"""

# Seleccionamos nuestro escalador
scaler = StandardScaler()

# Escalamos las columnas del conjunto de datos
for column in df.columns:
  df[column] = scaler.fit_transform(df[column].values.reshape(-1, 1))

df

"""### Muestreo

Para aplicar los métodos vistos a lo largo del curso usaremos una muestra de nuestros datos con la cual estaremos trabjando. El muestreo será aleatorio, trabajando con el 30% de los datos
"""

df = df.sample(frac=0.3); df

"""# Aplicación

## 1. Análisis de regresión lineal múltiple

Análisis para predecir que describe si la relación entre las variables explicativas y las variables dependientes es significativa, así como qué variables explicativas son más importantes.
Queremos un modelo lineal de la forma: $Y = Xb + ϵ$
"""

# Hacemos una compia del la muestra
# para no modificarla al hacer cada
# uno de los análisis
df_multiple = df.copy()

"""### 1.1 Definimos quién es nuestra matriz *X* conformada por las variables explicativas"""

# Cambiamos el nombre de nuestras variables
df_multiple.rename(columns =
                  {real:'X' + str(nuevo+1) for nuevo, real in enumerate(df_multiple.columns)},
                   inplace = True)

# Insertamos la columna faltantes de 1's

df_multiple.insert(loc=0, column='X0', value=[1 for _ in range(df_multiple.shape[0])]); df_multiple

# En formato de array
X = np.matrix([np.array(df_multiple.loc[i]) for i in df_multiple.index])

"""### 1.2 ¿Quién es $Y$?"""

# La variable diagnosis contiene los valores de
# la columna diagnosis de todas las filas, solo
# seleccionamos las que coincidan con la muestra

Y = Series(diagnosis.iloc[i] for i in df_multiple.index); Y

# Modificamos el formato de Y
# Donde M = 0 y B = 1

Y = Y.replace({"M": 0, "B": 1}); Y

"""### 1.3 ¿Quién es $b$?

Ver si existe $(XX^T)^{-1}$, es decir si X tiene rango máximo
"""

inv(X @ X.T)

"""Al ver que pyton no arroja ningún error en la operación $(XX^T)^{-1}$, entonces el estimador de verosimilitud para $b$ es: $b = (X^{T}X)^{-1}X^{T}Y$"""

b = [inv(X.T @ X)] @ (X.T @ Y)

"""### 1.4 Modelo

$y ≈  0.628 + 0.5289X1 - 0.1718X2 - 0.1023X3 - 0.1932X4 - 0.04091X5 + 0.2872X6 - 0.569X7 + 0.1115X8 + 0.03222X9 + 0.1063X10 - 0.07365X11 - 0.09035X12 - 0.1468X13 + 0.2139X14 - 0.0224X15 + 0.04783X16 + 0.09933X17 - 0.05222X18 + 0.003046X19 + 0.1255X20 - 1.18X21 + 0.1767X22 + 0.2358X23 + 0.5367X24 - 0.0008232X25 - 0.06987X26 + 0.1949X27 - 0.1106X28 - 0.05114X29 - 0.2716X30$

---
"""

b_values = [(i, '') if x == 0 else (i, 'X'+ str(x)) for x, i in enumerate(b[0])]

print(f'El modelo de regresión lineal es: ')
print('')
print('y ≈ ', end=' ' )

for i, (b_n, x_n) in enumerate(b_values):


  if i == 0:

    print('{:.4}{}'.format(b_n, x_n), end=' ')

  else:

    if b_n >= 0: print('+ {:.4}{}'.format(b_n, x_n), end=' ')

    else: print('- {:.4}{}'.format(b_n*-1, x_n), end=' ')

"""---

Como el Anális de regresión lineal múltiple nos ayuda a predecir el valor de datos desconocidos, en este caso suponemos que ese dato desconocido es Y que representa el diagnóstico del tipo de cáncer,  esto lo hace mediante el uso de otro valor de datos relacionado y conocido, en este caso todas nuestras X.
Vemos que la ecuación anterior muestra una "receta" para crear y y las b's, es decir, los cofiecientes de nuestra ecuación son la cantidad de cada variable que hay que poner.

---

### 1.5 Y estimada
"""

Y_pred = []

for i in df_multiple.index:
  y_pred = 0

  for bi, xi in zip(b[0],np.array(df_multiple.loc[i])):
    y_pred += bi*xi

  # Como las etiquetas de Y (diagnosis) solo permite 0's y 1's
  # si el valor de y_pred es menor a 0.5 será 0
  # de ser mayor y_pred será 1

  if y_pred < 0.5: y_pred = 0
  else: y_pred = 1

  Y_pred. append(y_pred)

"""#### 1.5.1 Matriz de confusión"""

confusion_matrix = metrics.confusion_matrix(Y, Y_pred)

# Para crear una pantalla visual más interpretable
# convertimos la tabla confusuion_mattix en una
# pantalla de matriz de confusión

cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [0, 1])
cm_display.plot(cmap=plt.cm.Blues)
plt.title('Matriz de confusión del modelo de regresión lineal múltiple.')
plt.xlabel('Etiqueta predicha.')
plt.ylabel('Verdadera etiqueta.')
plt.show()
#plt.savefig('matriz_confusion.png', dpi = 150, format = 'png')

# Accuracy
metrics.accuracy_score(Y, Y_pred)

"""Con la matriz de confusión vemos que se predijo $65$ valores tipo $0$ (Cáncer Maligno = M) y de esos los $65$ sí son tipo $0$. Por el caso contrario predijo que había $106$ valores tipo $1$ (Cáncer Benigno = B)., de los cuales $103$ sí son del tipo $1$ y el resto realmente son del tipo $0$ Con estos resultados vemos que nuestra predicción es bastante buena, así mismo lo confirma el accuracy, obteniendo un valor del 98.24%

### 1.6 Intervalo de confianza
Primero veremos el intervalo de confianza de nuestras b's para ver qué tan confiable es nuestro modelo, Para ello vamos a considerar el 95% de confianza, eso quiere decir que $α$ vale $0.05$ y $\frac{α}{2}$ $0.025$

#### 1.6.1 Grados de libertad y t-student
Mínima cantidad de parámetros necesarios para determinar una variable
"""

n = df_multiple.shape[1]  #numero de variables
p = df_multiple.shape[0]  # cantidad de elementos en la muestra

Gl = abs(n-(p+1)); Gl

# 1 - (α/2) = 0.975
# n-(p+1) = 141
#t-studet: (0.975, 141)

t = sts.t.ppf(0.975, 141); t

"""#### 1.6.2 Intervalos de confianza

- Varianza no explicativa
"""

VNE = sum([(Y[r]- Y_pred[r])**2 for r in range(Y.shape[0])]); VNE

"""- Varianza residual"""

Sr = VNE/(Gl); Sr

"""- Matriz $Q = (X^{T}X)^{-1}$
>
Donde nos importa los valores de la diagonal $q_{i+1},_{i+1}$ para la fórmula
"""

# Matriz Q para obtenere los valores de la diagonal
# usados al sacar el intervalo de confianza √qi+1,i+1
Q = inv(X.T @ X)

"""- Intervalo de confianza para bi:
$IC_{1-α}(bi) = [\hat{bi} \pm t_{\frac{α}{2}, n-(p+1)} S_{r} \sqrt (q_{i+1},_{i+1})]$
"""

ICs = [(bi - (t * Sr * np.sqrt(Q[i, i])), bi + (t * Sr * np.sqrt(Q[i, i]))) for i, bi in enumerate(b[0])]

ICs

"""Estos dos valoresacotan el valor donde se encontrará de la media de  $b_i$

## 2. Análisis de Componentes principales (ACP)

Método estadístico para la reducción de la dimensionalidad de la base de datos. Esta técnica se utiliza cuando queremos simplificar la base de datos, ya sea para elegir un menor número de predictores para pronosticar una variable objetivo, o para comprender una base de datos de una forma más simple.
Optiene nuevas variables llamadas componente principales $Y_{i}$ que son combinaciones lineales de nuestras varibales $X_{i}$
"""

# Hacemos una compia del la muestra
# para no modificarla al hacer cada
# uno de los análisis

df_acp = df.copy(); df_acp

"""### 2.1 Calcular valores y Vectores propios"""

plt.figure(figsize = (20, 10))
sns.heatmap(df.corr(), annot = True)
plt.title('Matriz de correlación del conjunto de datos.')
plt.show()
#plt.savefig('matriz_corr.png', dpi = 150, format = 'png', bbox_inches = 'tight')

# Los coeficientes de los componentes principales son las "columnas" del segundo arreglo
# están desordenados (no importa la cantidad de varianza que expliquen)
evalues, evectors = np.linalg.eig(df_acp.corr())

# Valores propios
evalues

# Vectores propios (columnas)
evectors

sum(evalues)

"""### 2.2 ACP"""

# Usamos ACP con 3 componentes
pca=PCA(n_components=3)
pca.fit(df_acp)

# Los coeficientes de los CP son los renglones, y además están ordenados
# de mayor a menos varianza
pca.components_

# Porcentaje de varianza explicada por las pimeras dos variables
sum(pca.explained_variance_ratio_)*100

"""### 2.3 Transformación de datos
Convierte cada punto $(x_{1}, x_{2}, x_{3})$ que representa un dato, en las nuevas coordenadas $(y_{1}, y_{2}, y_{3})$ donde $y_{i}$ es un componente principal
"""

df_acp_transform = pca.transform(df_acp); df_acp_transform

# mapa de calor
data_acp_transform = pd.DataFrame()
data_acp_transform['Y1'] = list(map(float, df_acp_transform[:, 0:1]))
data_acp_transform['Y2'] = list(map(float, df_acp_transform[:, 1:2]))
data_acp_transform['Y3'] = list(map(float, df_acp_transform[:, 2:3]))

plt.figure(figsize = (15, 15))
sns.heatmap(data_acp_transform.corr(), annot = True)
plt.title('Mapa de calor de las componentes principales.')
plt.show()
#plt.savefig('mapa_calor.png', dpi = 150, format = 'png', bbox_inches = 'tight')

"""### 2.4 Varianza explicada"""

#Tabla de porcentaje de varianzas explicadas
#Var: por cada componente principal (CP)
#cumVar: acumulada de los primeros k componentes principales

cumVar=pd.DataFrame(np.cumsum(pca.explained_variance_ratio_)*100,
                    columns=["cumVar"])
expVar = pd.DataFrame(pca.explained_variance_ratio_*100, columns=["Var"])
pd.concat([expVar, cumVar], axis=1).rename(index={0: "CP1", 1: "CP2", 2:"CP3"})

"""### 2.5 Gráfica

Graficamos nuestros datos con nuestras coordenadas $y_{1}$, $y_{2}$, $y_{3}$
"""

# Creamos la figura
fig = plt.figure()
# Creamos el plano 3D
ax1 = fig.add_subplot(111, projection='3d')

# Definimos los datos de prueba
x = list(map(float, df_acp_transform[:, 0:1]))
y = list(map(float, df_acp_transform[:, 1:2]))
z = list(map(float, df_acp_transform[:, 2:3]))


# Agregamos los puntos en el plano 3D
ax1.scatter(x, y, z, c='r', marker='o')

#Etiquetas
ax1.zaxis.set_rotate_label(False)
ax1.set_xlabel('CP1', fontsize = 15)
ax1.set_ylabel('CP2', fontsize = 15)
ax1.set_zlabel('CP3', fontsize = 15)  #modificar para que sea visible


# Mostramos el gráfico
plt.title('Gráfica de los datos transformados por las componentes principales.')
plt.show()
#plt.savefig('datos_trans.png', dpi = 150, format = 'png', bbox_inches = 'tight')

"""## 3. Anális Factorial (AF)

Como los demas análisis estadísticos multivariados, el objetivo del analisis factorial, es tratar muchas variables mediante una cantidad menor de variables (en este caso llamados factores), sin perder mucha información.
Escribe cada variable inicial $X_{i}$ como combinación lineal de las nuevas variables $f_{i}$ llamdas factores
"""

# Hacemos una compia del la muestra
# para no modificarla al hacer cada
# uno de los análisis
df_af = df.copy(); df_af

# Cambiamos el nombre de nuestras variables
#df_af.rename(columns = {real:'X' + str(nuevo) for nuevo, real in enumerate(df_af.columns)},
                   #inplace = True)
#df_af

"""### 3.1 Calcular valores y Vectores propios"""

# Los coeficientes de los componentes principales son las "columnas" del segundo arreglo
# están desordenados (no importa la cantidad de varianza que expliquen)
evalues, evectors = np.linalg.eig(df_af.corr())

# Valores propios
evalues

# vectores propios
evectors

"""### 3.2 Varianza explicada

#### 3.2.1 Cálculo
"""

varianza_explicada = evalues/ sum(evalues); varianza_explicada

"""#### 3.2.2 Gráfica"""

plt.plot(np.arange(1, df_af.corr().shape[0] + 1), sorted(varianza_explicada, key = float, reverse = True), marker = 'o')
plt.xlabel('Indice')
plt.ylabel('Varianza Explicada')
plt.xticks(np.arange(1, df_af.corr().shape[0] + 1))
plt.grid(True)

"""Viendo la gráfica y los resultados arrojados nos quedamos con 3 variables que explican el 73.64%

"""

sum(sorted(varianza_explicada, key = float, reverse = True)[0:3])

"""### 3.3 Análisis Factorial

De acuerdo a los resultados arrojados anteriormente con la gráfica, de define 3 factores
"""

fa = FactorAnalyzer()
fa.set_params(n_factors=3, rotation=None)
fa.fit(df_af)

"""#### 3.3.2 Coeficientes de los factores $f_i$ de cada variable explicativa $x_i$"""

factores=pd.DataFrame(fa.loadings_,columns=['F1','F2', 'F3'],index=df_af.columns)
factores

"""### 3.4 Especificidad $\psi_i$
Representa la parte de la varianza específica de cada variable $x_i$
"""

fa = FactorAnalysis(n_components = 3, rotation="varimax")
fa.fit(df_af)
especifidad = Series(fa.noise_variance_, index=df_af.columns)
especifidad.plot(
    kind="bar",
    ylabel="Especifidad"
)

"""### 3.5 Comunalidad $h_{i}^{2}$
Representa la varianza explicada por los factores comunes
"""

comunalidad = Series(np.square(fa.components_.T).sum(axis=1), index=df_af.columns)
comunalidad.plot(
    kind="bar",
    ylabel="communalidad"
)

"""### 3.5 Matriz residual $\psi$
Es el Error de la igualdad $\Sigma = LL^T + \psi$
"""

lambda_ = fa.components_
psi = np.diag(especifidad)
s = np.corrcoef(np.transpose(df_af))
sigma = np.matmul(lambda_.T, lambda_) + psi
residual = (s - sigma)
pd.DataFrame(residual)

"""Realizamos el análisis factorial usando Varimax"""

fa_varimax = factor_analyzer.FactorAnalyzer()
fa_varimax.set_params(n_factors = 4, rotation = 'Varimax')
fa_varimax.fit(df_af)

factores_varimax = pd.DataFrame(fa_varimax.loadings_, columns = ['F1','F2', 'F3'], index = df_af.columns)
factores_varimax

"""## 4. Análisis de conglomerados
Consiste en buscar grupos (conglomerados) en un conjunto de observaciones de forma tal que
aquellas que pertenecen a un mismo grupo se parecen, mientras que aquellas que pertenecen a
grupos distintos son dis ́ımiles, seg ́un alg ́un criterio de distancia o de similitud.

#### 4.1 Kmeans
"""

# sleccionamos solo 2 componentes principales
X = data_acp_transform[['Y1', 'Y2']]

# Método para encontrar la mejor k

Nc = range(1, 20)
kmeans = [KMeans(n_clusters=i) for i in Nc]
kmeans
score = [kmeans[i].fit(X).score(X) for i in range(len(kmeans))]
score
plt.plot(Nc, score)
plt.title('Método del codo para encontrar la mejor k.')
plt.xlabel('Número de clusters')
plt.ylabel('Puntaje')
plt.show()
#plt.savefig('codo.png', dpi = 150, format = 'png', bbox_inches = 'tight')

"""Si biem elegiríamos $k= 2$ debido a que se clasifica en cáncer Maligno y Beningno corroboramos con la gráfica anterior que el "mejor " valor para $k$ es 2"""

kmeans = KMeans(n_clusters=2).fit(X)
centroids = kmeans.cluster_centers_
print(centroids)

# Predicting the clusters
labels = kmeans.predict(X)
labels

confusion_matrix2 = metrics.confusion_matrix(Y, labels)

# Para crear una pantalla visual más interpretable
# convertimos la tabla confusuion_mattix en una
# pantalla de matriz de confusió}}}n

cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix2, display_labels = [0, 1])
cm_display.plot(cmap=plt.cm.Blues)
plt.title('Matriz de confusión del análisis de conglomerados.')
plt.xlabel('Etiqueta predicha.')
plt.ylabel('Verdadera etiqueta.')
plt.show()
#plt.savefig('matriz_confusion_cong.png', dpi = 150, format = 'png')

# accuracy de la categoría real con predicha
metrics.accuracy_score(Y, labels)

"""Con la matriz de confusión vemos que se predijo $52$ valores tipo $0$ (Cáncel Maligno = M) y de esos los $50$ sí son tipo $0$ y $2$ son del tipo $1$. Por el caso contrario predijo que había $119$ valores tipo $1$ (Cáncer Benigno = B)., de los cuales $101$ sí son del tipo $1$ y el resto realmente son del tipo $0$ Con estos resultados vemos que nuestra predicción es bastante buena, así mismo lo confirma el accuracy, obteniendo un valor del 88.30%"""

# Getting the cluster centers
C = kmeans.cluster_centers_
colores=['darkcyan','coral']
asignar=[]
for row in labels:
    asignar.append(colores[row])

"""Clusters predichos visualización"""

fig = plt.figure()
ax = fig.add_subplot(projection = "3d")
#ax = Axes3D(fig)

ax.scatter(data_acp_transform .iloc[:, 0], data_acp_transform.iloc[:, 1], data_acp_transform.iloc[:, 2], c=asignar,s=60)
ax.scatter(C[:, 0], C[:, 1], marker='o', c=colores, s=1000)
#plt.savefig('gráfica.png')
plt.show()

# Getting the values and plotting it
f1 = data_acp_transform['Y1'].values
f2 = data_acp_transform['Y2'].values

plt.scatter(f1, f2, c=asignar, s=70)
plt.scatter(C[:, 0], C[:, 1], marker='^', c=['blue', 'red'], s=1000)
plt.title('Gráfica de los clusters encontrados por el método de KMeans.')
plt.xlabel('Componente 1')
plt.ylabel('Componente 2')
plt.show()
#plt.savefig('clusters_kmeans.png', dpi = 150, format = 'png')
