#si vas a usar esto para apostar, solo tomalo como base, mi recomendacion es no meter a los marcadores exactos ya que pueden variar cada vez que corras el codigo, pero si para tener una idea de quien tiene mas probabilida de ganar
import random
import operator
import itertools as it
import matplotlib.pyplot as plt
import numpy as np
import collections

def Simular_Partido(Country_A, Country_B, CountryElo, simulaciones=10000):
    puntos_A = CountryElo[Country_A]
    puntos_B = CountryElo[Country_B]
    
    #Modelo matemático
    diferencia_elo = puntos_A - puntos_B
    promedio_base = 1.25
    
    base_goles_A = max(0.1, promedio_base + (diferencia_elo / 350))
    base_goles_B = max(0.1, promedio_base - (diferencia_elo / 350))
    
    goles_A_sim = np.random.poisson(base_goles_A, simulaciones)
    goles_B_sim = np.random.poisson(base_goles_B, simulaciones)
    
    todos_los_marcadores = []
    for i in range(simulaciones):
        todos_los_marcadores.append((goles_A_sim[i], goles_B_sim[i]))
    
   #Extraccion de los mejores resultados
    conteo = collections.Counter(todos_los_marcadores)
    mejores_dos = conteo.most_common(2)
    
    #Datos del primer lugar (el mas probable)
    marcador_1, veces_1 = mejores_dos[0]
    porcentaje_1 = (veces_1 / simulaciones) * 100
    
    #Datos del segundo lugar
    marcador_2, veces_2 = mejores_dos[1]
    porcentaje_2 = (veces_2 / simulaciones) * 100
    
    print(f"Prediccion {Country_A} vs {Country_B}: ")
    print(f"   1ra Opcion: {marcador_1[0]} - {marcador_1[1]} ({porcentaje_1:.2f}%)")
    print(f"   2da Opcion: {marcador_2[0]} - {marcador_2[1]} ({porcentaje_2:.2f}%)")
    print("-" * 50)
    
    if marcador_1[0] > marcador_1[1]:
        return marcador_1, Country_A
    elif marcador_1[0] < marcador_1[1]:
        return marcador_1, Country_B
    else:
        return marcador_1, 'Draw'

#ranking sacado de: https://inside.fifa.com/fifa-world-ranking/men
#puede tener variaciones segun la fecha en la que consultes esto
#entre mas avance el mundial, seria recomendable actualizar cada pais
CountryFIFA  = {
'France':1877,
'Spain':1876,
'Argentina':1874,
'England':1825,
'Portugal':1763,
'Brazil':1762,
'Netherlands':1757,
'Morroco':1756,
'Belgium':1739,
'Germany':1739,
'Croatia':1712,
'Colombia':1695,
'Senegal':1686,
'Mexico':1684,
'USA':1675,
'Uruguay':1673,
'Japan':1661,
'Switzerland':1650,
'Denmark':1620,
'Iran':1616,
'Turkey':1601,
'Austria':1597,
'Ecuador':1596,
'South Korea':1589,
'Australia':1578,
'Egypt':1565,
'Argelia':1564,
'Canada':1560,
'Norway':1555,
'Panama':1539,
'Ivory Coast':1532,
'Sweden':1510,
'Paraguay':1503,
'Czechia':1503,
'Scotland':1499,
'Tunisia':1479,
'DR Congo':1478,
'Uzbekistan':1461,
'Qatar':1452,
'Iraq':1447,
'South Africa':1428,
'Saudi Arabia':1419,
'Jordan':1390,
'Bosnia and Herzegovina':1385,
'Cape Verde':1369,
'Ghana':1346,
'Haiti':1296,
'Curacao':1293,
'New Zealand':1276,
}

#Usuario mete los paises (deben coincidir los nombres de CountryFIFA)

#Country_List = ['Mexico', 'South Africa', 'South Korea', 'Czechia'] # GroupA
#Country_List = ['Canada', 'Bosnia and Herzegovina', 'Qatar', 'Switzerland'] # GroupB
#Country_List = ['Brazil', 'Morroco', 'Haiti', 'Scotland'] # GroupC
#Country_List = ['USA', 'Paraguay', 'Australia', 'Turkey'] # GroupD
#Country_List = ['Germany', 'Curacao', 'Ivory Coast', 'Ecuador'] # GroupE
#Country_List = ['Netherlands', 'Japan', 'Sweden', 'Tunisia'] # GroupF
#Country_List = ['Belgium', 'Egypt', 'Iran', 'New Zealand'] # GroupG
Country_List = ['Spain', 'Cape Verde', 'Saudi Arabia', 'Uruguay'] # GroupH
#Country_List = ['France', 'Senegal', 'Iraq', 'Norway'] # GroupI
#Country_List = ['Argentina', 'Argelia', 'Austria', 'Jordan'] # GroupJ
#Country_List = ['Portugal', 'DR Congo', 'Uzbekistan', 'Colombia'] # GroupK
#Country_List = ['England', 'Croatia', 'Ghana', 'Panama'] # GroupL


NumSim = 10000 #numero de veces que se hara montecarlo

Country_Point_Zero = {}

for Country in Country_List :
    Country_Point_Zero[Country] = 0

CountryAverage = Country_Point_Zero.copy()
Match_All_List = list(it.combinations(Country_List, 2))
Qualified_List = [] 

print("======  LOS DOS MARCADORES MAS PROBABLES PREDICHOS ======")
for Match_Competition in Match_All_List:
    Country_A = Match_Competition[0]
    Country_B = Match_Competition[1]
    Simular_Partido(Country_A, Country_B, CountryFIFA, simulaciones=10000)
print("=============================================================\n")


for i in range(0, NumSim):
    CountryPoint = Country_Point_Zero.copy()
    
    for Match_Competition in Match_All_List:
        Country_A = Match_Competition[0]
        Country_B = Match_Competition[1]
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
        
    CountryAverage[Pass1] += Score1 / NumSim
    CountryAverage[Pass2] += Score2 / NumSim    
    CountryAverage[Pass3] += Score3 / NumSim
    CountryAverage[Pass4] += Score4 / NumSim
