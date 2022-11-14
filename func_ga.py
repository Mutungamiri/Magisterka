from audioop import reverse
import random
from re import I
import time
import numpy as np
from past.builtins import xrange
from sympy import numer

#FUNKCJA GENERUJĄCA POPULACJE
def generacja_populacja(wielkosc_populacji, liczba_jobs):
    populacja = []
    i = 0
    while i < wielkosc_populacji:
        osobnik = list(np.random.permutation(liczba_jobs))
        populacja.append(osobnik)
        i += 1
    return populacja

#FUNKCJA LICZĄCA MAKESPAN OSOBNIKA
def funkcja_dopasowania(osobnik, czas_trwania, liczba_jobs, liczba_maszyn):

    koszt = [0] * liczba_jobs
    for numer_maszyny in range(0, liczba_maszyn):
        for operacja in range(liczba_jobs):
            koszt_aktualny = koszt[operacja]
            if operacja > 0:
                koszt_aktualny = max(koszt[operacja - 1], koszt[operacja])
            koszt[operacja] = koszt_aktualny + czas_trwania[osobnik[operacja]][numer_maszyny]
            #print(koszt[operacja], osobnik[operacja])
    #print(koszt)
    return koszt[liczba_jobs - 1]

#FUNKCJA WYKONUJĄCA SELEKCJE TURNIEJOWĄ
def selekcja_turniejowa(populacja_makespan, wielkosc_populacji, wielkosc_turnieju):
    makespan_rodzice = []
    i=0
    while i < wielkosc_populacji:
        rodzice = random.choices(populacja_makespan, k=wielkosc_turnieju)
        #print(rodzice)
        rodzice.sort(key=lambda x: x[0])
        makespan_rodzice.append(rodzice[0])
        i += 1  
   
    return makespan_rodzice
#FUNKCJA WYKONUJĄCA SELEKCJĘ KOŁA RULETKI
def selekcja_kola_ruletki(populacja_makespan, wielkosc_populacji):
    makespan_rodzice = []
    makespan_populacji = []
    i = 0
    for i in range(0,wielkosc_populacji):
        temp = populacja_makespan[i][0]
        makespan_populacji.append(temp)
    #print(makespan_populacji)
    suma = sum(makespan_populacji)
    #print(suma)
    prawdopodobienstwa = [x/suma for x in makespan_populacji]
    #print(prawdopodobienstwa)

    cumulative_fitness = []
    start = 1
    for prawdopodobienstwo in prawdopodobienstwa:
        start -= prawdopodobienstwo
        cumulative_fitness.append(start)
    #print(cumulative_fitness)

    for count in range(wielkosc_populacji):
        losowy_numer = random.uniform(0,1)
        index_osobnika = 0
        for score in cumulative_fitness:
            if(losowy_numer>=score):
                makespan_rodzice.append(populacja_makespan[index_osobnika])
                break
            index_osobnika += 1
    return makespan_rodzice

def selekcja_stochastyczna_akceptacja(populacja):
    maxpop = []
    maxpop = populacja
    while True:
        osobnik = random.choices(populacja, k=1)
        #maxpop.sort(reverse=True)
        # print("Wybrany osobnik:",osobnik[0][0])
        # print("max", populacja[0][0])
        # print("populacja", populacja)
        r = random.uniform(0,1)
        if r < osobnik[0][0]/maxpop[0][0]:
            #print("Wybrany osobnik", osobnik)
            return osobnik[0]
        else:
            #print("Nie wybrano")
            continue



#FUNKCJA WYKONUJĄCA KRZYŻOWANIE DWUPUNKTOWE OX
def krzyzowanie_dwupunktowe_OX(rodzice, prawdopodobienstwo_krzyzowania):
    dlugosc_rodzica = len(rodzice[0][1])
    pierwszy_punkt= random.randint(0,dlugosc_rodzica)
    drugi_punkt = random.randint(0,dlugosc_rodzica - 1)
    potomkowie = []
    
    if pierwszy_punkt > drugi_punkt:
        t = pierwszy_punkt
        pierwszy_punkt = drugi_punkt
        drugi_punkt = t
    #print("Pierwszy punkt:", pierwszy_punkt, "Drugi punkt:", drugi_punkt)

    rodzic1 = rodzice[0][1]
     
    index = 1
    
    while True:
        temp = rodzice[index][1]
        if index == len(rodzice)-1:
            rodzic2 = temp
            break
        elif temp != rodzice[0][1]:
            rodzic2 = temp
            break
        else:
            index += 1
    
    #print(rodzic1, rodzic2)

    potomkowie.append(list(rodzic1))
    for i in range(pierwszy_punkt, drugi_punkt):
        potomkowie[0][i] = -1

    p = -1
    for i in range(pierwszy_punkt, drugi_punkt):
        while True:
            p += 1
            if rodzic2[p] not in potomkowie[0]:
                potomkowie[0][i] = rodzic2[p]
                break

    potomkowie.append(list(rodzic2))
    for i in range(pierwszy_punkt, drugi_punkt):
        potomkowie[1][i] = -1

    p = -1
    for i in range(pierwszy_punkt, drugi_punkt):
        while True:
            p += 1
            if rodzic1[p] not in potomkowie[1]:
                potomkowie[1][i] = rodzic1[p]
                break

    r = np.random.rand()
    if r < prawdopodobienstwo_krzyzowania:
        #print("Krzyżowanie")
        return potomkowie
    else:
        #print("Bez krzyżowania")
        return [rodzic1, rodzic2]

#FUNKCJA WYKONUJĄCA KRZYŻOWANIE PMX
def krzyzowanie_PMX(rodzice, prawdopodobienstwo_krzyzowania):
    dlugosc_rodzica = len(rodzice[0][1])
    pr1, pr2 = [0] * dlugosc_rodzica, [0] * dlugosc_rodzica
    pierwszy_punkt= random.randint(0,dlugosc_rodzica)
    drugi_punkt = random.randint(0,dlugosc_rodzica - 1)
    
    if drugi_punkt >= pierwszy_punkt:
        drugi_punkt += 1
    else:
        pierwszy_punkt, drugi_punkt = drugi_punkt, pierwszy_punkt

    rodzic1 = rodzice[0][1]
    index = 1
    while True:
        temp = rodzice[index][1]
        if index == len(rodzice)-1:
            rodzic2 = temp
            break
        elif temp != rodzice[0][1]:
            rodzic2 = temp
            break
        else:
            index += 1
    
    bez1 = rodzic1
    bez2 = rodzic2
    #print(pierwszy_punkt, drugi_punkt)
    #print(rodzic1, rodzic2)
    for i in xrange(dlugosc_rodzica):
        pr1[rodzic1[i]] = i
        pr2[rodzic2[i]] = i
    #print(r1, r2)

    for i in xrange(pierwszy_punkt, drugi_punkt):
        tym1 = rodzic1[i]
        tym2 = rodzic2[i]

        rodzic1[i], rodzic1[pr1[tym2]] = tym2, tym1
        rodzic2[i], rodzic2[pr2[tym1]] = tym1, tym2

        pr1[tym1], pr1[tym2] = pr1[tym2], pr1[tym1]
        pr2[tym1], pr2[tym2] = pr2[tym2], pr2[tym1]



    r = np.random.rand()
    if r < prawdopodobienstwo_krzyzowania:
        #print("Krzyżowanie")
        return [rodzic1, rodzic2]
    else:
        #print("Bez krzyżowania")
        return [bez1, bez2]


def krzyzowanie_CX(rodzice, prawdopodobienstwo_krzyzowania):
    rodzic1 = rodzice[0][1]
    index = 1
    while True:
        temp = rodzice[index][1]
        if index == len(rodzice)-1:
            rodzic2 = temp
            break
        elif temp != rodzice[0][1]:
            rodzic2 = temp
            break
        else:
            index += 1
    #print(rodzic1, rodzic2)
    r = np.random.rand()
    if r < prawdopodobienstwo_krzyzowania:
        cykle = [-1]*len(rodzic1)
        numer_cyklu = 1
        start_cyklu = (i for i,v in enumerate(cykle) if v < 0)

        for poz in start_cyklu:
            while cykle[poz] < 0:
                cykle[poz] = numer_cyklu
                poz = rodzic1.index(rodzic2[poz])
            numer_cyklu += 1

        potomek1 = [rodzic1[i] if n%2 else rodzic2[i] for i,n in enumerate(cykle)]
        potomek2 = [rodzic2[i] if n%2 else rodzic1[i] for i,n in enumerate(cykle)]

        #print("Krzyżowanie")
        return [potomek1, potomek2]
    else:
        #print("Bez krzyżowania")
        return [rodzic1, rodzic2]


#FUNKCJA WYKONUJĄCA MUTACJE ZAMIENIAJĄCĄ DWA LOSOWE POZYCJE W TABLICY OSOBNIKA
def mutacja_zamiana_genu(potomek):
    mutowany_potomek = list(potomek)
    dlugosc_potomka = len(potomek)
    pozycje_do_zamiany = list(np.random.permutation(np.arange(dlugosc_potomka))[:2])
    job1 = potomek[pozycje_do_zamiany[0]]
    job2 = potomek[pozycje_do_zamiany[1]]
    mutowany_potomek[pozycje_do_zamiany[0]] = job2
    mutowany_potomek[pozycje_do_zamiany[1]] = job1

    return mutowany_potomek

#FUNKCJA DODAJĄCA POPULACJE POTOMKÓW DO GŁÓWNEJ POPULACJI
def aktualizacja_populacji(populacja, potomkowie, czas_trwania, liczba_jobs, liczba_maszyn, wielkosc_populacji):
    populacja.sort(reverse=True)
    #print("Populacja przed dodaniem:",populacja)
    makespan_potomkowie = []
    for potomek in potomkowie:
        makespan_potomek = (funkcja_dopasowania(potomek, czas_trwania, liczba_jobs, liczba_maszyn), potomek)
        makespan_potomkowie.append(makespan_potomek)
    makespan_potomkowie.sort(key=lambda x: x[0])
    
    for potomek in makespan_potomkowie:
        populacja.append(potomek)

    # while len(populacja) >= wielkosc_populacji:
    #     populacja.remove(populacja[index])
    #     index += 1

    # populacja.sort(key=lambda x: x[0])
    # populacja = populacja[0:wielkosc_populacji]

    return populacja