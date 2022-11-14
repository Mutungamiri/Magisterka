import random
import time
import numpy as np
import func_ga
import glob
from pathlib import Path
import csv


# Parametry GA
wielkosc_populacji = 50
liczba_generacji = 1000
prawdopodobienstwo_krzyzowania = 0.9
prawdopodobienstwo_mutacji = 0.2
wielkosc_turnieju = 5
dane_csv = []
# Wybór operatorów
crossover = 2 #0-OX, 1-PMX, 2-CX
selection = 2 #0-Turniej, 1-Ruletka 2-Stochastyczna
numer_pliku = 0
for i in range(0,10):
    nazwacsv = 'cxstochastyczna_09_02_50_1000'
    pliki = Path('C:\\Users\\Mateusz Perdek\\Desktop\\Mag\\tailardtune').glob('*.txt')
    numer_bench = 1
    for name in pliki:
        plik = open(name, 'r')
        linia = plik.readline().split()

        # Parametry problemu przepływowego
        liczba_jobs, liczba_maszyn, czas_benchmark = int(linia[0]), int(linia[1]), int(linia[2])

        czas_trwania = []

        for i in range(liczba_jobs):
            temp = []
            linia = plik.readline().split()
            for j in range(liczba_maszyn):
                temp.append(int(linia[2*j+1]))
            czas_trwania.append(temp)


        #print(czas_trwania)

        # Generacja populacji

        zliczaniegen = 0
        populacja = func_ga.generacja_populacja(wielkosc_populacji, liczba_jobs)
        najlepsi_osobnicy = []

        #print(populacja)
        #...............FUNKCJA DOPASOWANIA...............
        makespan_populacji = []
        for osobnik in populacja:
            makespan_osobnika = (func_ga.funkcja_dopasowania(osobnik, czas_trwania, liczba_jobs, liczba_maszyn), osobnik)
            makespan_populacji.append(makespan_osobnika)

        #print(makespan_populacji)



        for generacja in range(liczba_generacji):
            #..............SELEKCJA_Turniejowa.................
            if selection == 0:
                makespan_rodzice = func_ga.selekcja_turniejowa(makespan_populacji, wielkosc_populacji, wielkosc_turnieju) 
                makespan_rodzice.sort(key=lambda x: x[0])
                #print("Selekcja",makespan_rodzice)
                #print("Turniej")

            #..............SELEKCJA_koła_ruletki.................
            elif selection == 1:
                makespan_rodzice = func_ga.selekcja_kola_ruletki(makespan_populacji, wielkosc_populacji)
                makespan_rodzice.sort(key=lambda x: x[0])
                # print(makespan_rodzice)
                #print("Ruletka")
                #.............SELEKCJA_koła_rueltki_przez_akceptacje_stochastyczną..................
            elif selection == 2:

                makespan_rodzice = []
                maxpop = []
                maxpop = makespan_populacji
                maxpop.sort(reverse=True)
                i=0
                while i < wielkosc_populacji:
                    osobnik = func_ga.selekcja_stochastyczna_akceptacja(maxpop)
                    makespan_rodzice.append(osobnik)
                    i+=1
            else:
                print("Błąd")
                break

        #     
        #   #...................KRZYŻOWANIE_dwupunktowe_OX.............
            potomkowie = []
            if crossover == 0:
                liczba_krzyzowan = 0
                while liczba_krzyzowan < wielkosc_populacji/2:
                    para_potomkow = func_ga.krzyzowanie_dwupunktowe_OX(makespan_rodzice, prawdopodobienstwo_krzyzowania)
                    potomkowie.append(para_potomkow[0])
                    potomkowie.append(para_potomkow[1])
                    liczba_krzyzowan += 1
                #print("Krzyżowanie", potomkowie)

        #   #...................KRZYŻOWANIE_PMX.......................
            elif crossover == 1:
                liczba_krzyzowan = 0
                while liczba_krzyzowan < wielkosc_populacji/2:
                    para_potomków = func_ga.krzyzowanie_PMX(makespan_rodzice, prawdopodobienstwo_krzyzowania)
                    potomkowie.append(para_potomków[0])
                    potomkowie.append(para_potomków[1])
                    liczba_krzyzowan += 1
                # print("Potomkowie po krzyżowaniu:", potomkowie)
            #.....................KRZYŻOWANIE_CX...................
            elif crossover == 2:
                liczba_krzyzowan = 0
                while liczba_krzyzowan < wielkosc_populacji/2:
                    para_potomków = func_ga.krzyzowanie_CX(makespan_rodzice, prawdopodobienstwo_krzyzowania)
                    potomkowie.append(para_potomków[0])
                    potomkowie.append(para_potomków[1])
                    liczba_krzyzowan += 1
                
                #print("Potomkowie po krzyżowaniu:", potomkowie)
            else:
                print("Błąd")
                break

        #     #....................Mutacja................
            mutowani_potomkowie = []
            for potomek in potomkowie:
                r = np.random.rand()
                if r < prawdopodobienstwo_mutacji:
                    mutowany_potomek = func_ga.mutacja_zamiana_genu(potomek)
                    mutowani_potomkowie.append(mutowany_potomek)


            #print("Mutacja", mutowani_potomkowie)
            #print(type(mutowani_potomkowie))
            potomkowie.extend(mutowani_potomkowie)
            #print("Potomkowie",potomkowie)
            #....................Aktualizacja_Populacji...........
            if len(potomkowie) > 0:
                makespan_populacji = func_ga.aktualizacja_populacji(makespan_rodzice, potomkowie, czas_trwania, liczba_jobs, liczba_maszyn, wielkosc_populacji)
            #print("Populacja po dodaniu:",makespan_populacji)
            # print("Długość populacji", len(makespan_populacji))
            makespan_populacji.sort(key=lambda x: x[0])
            zliczaniegen += 1
            #print("Najlepszy osobnik w populacji:", makespan_populacji[0], "Generacja", zliczaniegen)
            najlepszy_osobnik = makespan_populacji[0]
            najlepsi_osobnicy.append(najlepszy_osobnik)
        najlepsi_osobnicy.sort(key=lambda x: x[0])
        print("Najlepsze rozwiązanie", najlepsi_osobnicy[0], "Błąd", abs((czas_benchmark-najlepsi_osobnicy[0][0])/100), "Benchmark", numer_bench)
        data = []
        data.append(najlepsi_osobnicy[0][0])
        # data.append(abs((czas_benchmark-najlepsi_osobnicy[0][0])/100))
        # data.append(numer_bench)
        dane_csv.append(data)
        numer_bench += 1

    #print(dane_csv)
    # csv_file =  open("sample_file.csv", 'w')
    # csv_writer = csv.writer(csv_file, delimiter=",")
    # for row in dane_csv:
    #     csv_writer.writerow(row)

    # csv_file.close()

with open(nazwacsv+'.csv', 'w', newline='') as file:
    fieldnames = ['Czas']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(0,len(dane_csv)):
        writer.writerow({'Czas': dane_csv[i][0]})
dane_csv = []


