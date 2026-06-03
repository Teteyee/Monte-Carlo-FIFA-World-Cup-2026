import random
import operator
import itertools as it
import matplotlib.pyplot as plt
#list of ranking of country in Group#A
import numpy as np
import collections

def Simular_Partido_Goles(Country_A, Country_B, CountryElo, simulaciones=10000):
    puntos_A = CountryElo[Country_A]
    puntos_B = CountryElo[Country_B]
    
    # --- MODELO MATEMÁTICO DE GOLES BASADO EN ELO ---
    # En el fútbol, el promedio de goles por partido ronda los 2.5 o 2.8 goles totales.
    # Usamos la proporción de puntos Elo para repartir la peligrosidad ofensiva.
    # Un equipo con más Elo tendrá un promedio esperado de goles mayor.
    
    # 1. Calculamos la diferencia de puntos Elo
    diferencia_elo = puntos_A - puntos_B
    
    # 2. Definimos una base de goles estándar para un partido (aprox 1.2 por equipo)
    promedio_base = 1.25
    
    # 3. Ajustamos los goles según la diferencia. 
    # Dividir entre 350 hace que una diferencia de 350 puntos sume/reste 1 gol entero al promedio.
    base_goles_A = max(0.1, promedio_base + (diferencia_elo / 350))
    base_goles_B = max(0.1, promedio_base - (diferencia_elo / 350))
    
    # Simulamos Montecarlo por fuerza bruta para ESTE partido
    # np.random.poisson nos genera un array de 10,000 resultados de goles basados en el promedio
    goles_A_sim = np.random.poisson(base_goles_A, simulaciones)
    goles_B_sim = np.random.poisson(base_goles_B, simulaciones)
    
    # Guardamos todos los marcadores generados en una lista de tuplas ej: (2, 1)
    todos_los_marcadores = []
    for i in range(simulaciones):
        todos_los_marcadores.append((goles_A_sim[i], goles_B_sim[i]))
    
    # Contamos cuál marcador fue el más repetido de las 10,000 veces
    conteo = collections.Counter(todos_los_marcadores)
    marcador_mas_probable, veces = conteo.most_common(1)[0]
    porcentaje = (veces / simulaciones) * 100
    
    print(f" Prediccion {Country_A} vs {Country_B}: {marcador_mas_probable[0]} - {marcador_mas_probable[1]} ({porcentaje:.2f}% de probabilidad)")
    
    # Regresamos el marcador exacto y quién ganó para que el resto del script sume los puntos del grupo
    if marcador_mas_probable[0] > marcador_mas_probable[1]:
        return marcador_mas_probable, Country_A
    elif marcador_mas_probable[0] < marcador_mas_probable[1]:
        return marcador_mas_probable, Country_B
    else:
        return marcador_mas_probable, 'Draw'







CountryFIFA  = {
'Spain':2165,
'Argentina':2113,
'France':2081,
'England':2020,
'Brazil':1988,
'Portugal':1984,
'Colombia':1977,
'Netherlands':1961,
'Ecuador':1935,
'Germany':1925,
'Norway':1917,
'Croatia':1908,
'Turkey':1906,
'Japan':1906,
'Switzerland':1894,
'Uruguay':1892,
'Belgium':1888,
'Denmark':1870,
'Mexico':1867,
'Senegal':1867,
'Paraguay':1832,
'Austria':1830,
'Morroco':1824,
'Canada':1793,
'Australia':1774,
'Scotland':1770,
'Iran':1764,
'South Korea':1756,
'Algeria':1743,
'Czechia':1733,
'United States':1733,
'Panama':1733,
'Uzbekistan':1718,
'Sweden':1714,
'Egypt':1699,
'Jordan':1685,
'Ivory Coast':1676,
'DR Congo':1655,
'Tunisia':1633,
'Iraq':1608,
'Bosnia and Herzegovina':1591,
'New Zealand':1585,
'Cape Verde':1576,
'Saudi Arabia':1566,
'Haiti':1532,
'South Africa':1518,
'Ghana':1510,
'Curacao':1433,
'Qatar':1423,
'Congo':1207,
}

#User input here, the country name must be consistent with CountryFIFA dictionary

#Country_List = ['Mexico', 'South Africa', 'South Korea', 'Czechia'] # GroupA
#Country_List = ['Canada', 'Bosnia and Herzegovina', 'Qatar', 'Switzerland'] # GroupB
#Country_List = ['Brazil', 'Morroco', 'Haiti', 'Scotland'] # GroupC
#Country_List = ['United States', 'Paraguay', 'Australia', 'Turkey'] # GroupD
#Country_List = ['Germany', 'Curacao', 'Ivory Coast', 'Ecuador'] # GroupE
#Country_List = ['Netherlands', 'Japan', 'Sweden', 'Tunisia'] # GroupF
#Country_List = ['Belgium', 'Egypt', 'Iran', 'New Zealand'] # GroupG
Country_List = ['Spain', 'Cape Verde', 'Saudi Arabia', 'Uruguay'] # GroupH
#Country_List = ['France', 'Senegal', 'Iraq', 'Norway'] # GroupI
#Country_List = ['Argentina', 'Argelia', 'Austria', 'Jordan'] # GroupJ
#Country_List = ['Portugal', 'Congo', 'Uzbekistan', 'Colombia'] # GroupK
#Country_List = ['England', 'Croatia', 'Ghana', 'Panama'] # GroupL



NumSim = 10000 # Number of simulation runs

Country_Point_Zero = {}

#Initialize the dict
for Country in Country_List :
    Country_Point_Zero[Country] = 0

CountryAverage = Country_Point_Zero.copy()

Match_All_List = list(it.combinations(Country_List, 2))


Qualified_List = [] #A list to collect qualified country (2 teams) for 2nd round
Leader_List = [] #A List to collect winner from the group

# =============================================================================
# PRÓXIMA FASE: SIMULACIÓN DE LA TABLA GENERAL (MONTECARLO DE GRUPO)
# =============================================================================

# Primero, antes del bucle masivo, imprimimos las predicciones de marcadores exactos
# corriendo una simulación interna robusta de 10,000 iteraciones por cada partido individual.
print("======  MARCADORES EXACTOS PREDICHOS ======")
for Match_Competition in Match_All_List:
    Country_A = Match_Competition[0]
    Country_B = Match_Competition[1]
    # Aquí corremos 10,000 simulaciones exclusivas para calcular el marcador exacto estadístico
    Simular_Partido_Goles(Country_A, Country_B, CountryFIFA, simulaciones=10000)
print("=============================================================\n")

# Ahora corremos el Montecarlo masivo del grupo SIN prints estorbosos para calcular las posiciones finales
for i in range(0, NumSim):
    CountryPoint = Country_Point_Zero.copy()
    
    for Match_Competition in Match_All_List:
        Country_A = Match_Competition[0]
        Country_B = Match_Competition[1]

        # Para simular el desarrollo de la tabla de posiciones, usamos el modelo de goles con 1 iteración
        # pero guardamos el print para que no sature la consola.
        # Modificación rápida: creamos una versión silenciosa para el bucle masivo.
        puntos_A = CountryFIFA[Country_A]
        puntos_B = CountryFIFA[Country_B]
        base_A = (puntos_A / puntos_B) * 1.35
        base_B = (puntos_B / puntos_A) * 1.15
        
        goles_A = np.random.poisson(base_A)
        goles_B = np.random.poisson(base_B)

        if goles_A > goles_B:
            CountryPoint[Country_A] += 3
        elif goles_A < goles_B:
            CountryPoint[Country_B] += 3
        else:
            CountryPoint[Country_A] += 1
            CountryPoint[Country_B] += 1

    Sorted_Country = sorted(CountryPoint.items(), key=operator.itemgetter(1))

    Pass1 = Sorted_Country[3][0]
    Pass2 = Sorted_Country[2][0]
    Pass3 = Sorted_Country[1][0]
    Pass4 = Sorted_Country[0][0]
    
    Score1 = Sorted_Country[3][1]
    Score2 = Sorted_Country[2][1]
    Score3 = Sorted_Country[1][1]
    Score4 = Sorted_Country[0][1]
    
    Qualified_List.append(Pass1)
    if Score2 != Score3:
        Qualified_List.append(Pass2)
    else:
        if CountryFIFA[Pass2] >= CountryFIFA[Pass3]:
            Qualified_List.append(Pass2)
        else:
            Qualified_List.append(Pass3)
        
    if Score1 != Score2:
        Leader_List.append(Pass1)
    else:
        if CountryFIFA[Pass1] >= CountryFIFA[Pass2]:
            Leader_List.append(Pass1)
        else:
            Leader_List.append(Pass2)

    CountryAverage[Pass1] += Score1 / NumSim
    CountryAverage[Pass2] += Score2 / NumSim    
    CountryAverage[Pass3] += Score3 / NumSim
    CountryAverage[Pass4] += Score4 / NumSim

# =============================================================================
# RESUMEN ESTADÍSTICO FINAL Y GRAFICACIÓN
# =============================================================================
# ... (El resto de tus bucles de cálculo de porcentajes y los plt.bar quedan exactamente igual)