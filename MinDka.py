'''
    programsko rješenje za 2. laboratorijsku vježbu na kolegiju "Uvod u teoriju računarstva"
    autor: Mihael Miličević
'''

# osnovna klasa za modeliranje DKA automata
class DKA():

    # konstrutor klase, kao argumente prima 5 varijabli koje predstavljaju uređenu petorku kojom se DKA formalno definira
    def __init__(self, states, symbols, acceptableStates, startState, transitionFunction):
        self.states = states
        self.symbols = symbols
        self.acceptableStates = acceptableStates
        self.startState = startState
        self.transitionFunction = {}
        for el in transitionFunction:
            self.transitionFunction[(el[0],el[1])] = el[2]

    # glavna funkcija minimizacije automata, prvo poziva funkciju uklanjanja nedohvatljivih stanja, a potom poziva funkciju spajanja istovjetnih stanja
    def minimize(self):
        self.dropUnreachableStates()
        self.mergeNondistinguishableStates()

    # pomoćna funkcija čija svrha je pronalazak i uklanjanje nedohvatljivih stanja automata
    def dropUnreachableStates(self):

        # kretanje iz početnog stanja automata i korištenje BFS-a za identifikaciju svih dohvatljivih stanja
        reachedStates = set()
        queue = [self.startState]
        while len(queue) != 0:
            curr = queue.pop(0)

            # računanje svih stanja u koje automat može ići iz trenutnog stanja
            transitions = [transition for transition in self.transitionFunction if transition[0] == curr]
            for transition in transitions:

                # svrha ove provjere je da se ne zavrtimo u beskonačnoj petlji, tj. da ne obilazimo već obiđena stanja
                if transition[0] not in reachedStates:
                    queue.append(self.transitionFunction[transition])
            reachedStates.add(curr)

        # računanje svih nedohvatljivih stanja
        self.states = set(self.states)
        self.acceptableStates = set(self.acceptableStates)
        unreachableStates = self.states - reachedStates

        #uklanjanje nedohvatljivih stanja iz automata
        for state in unreachableStates:

            # uklanjanje nedohvatljivog stanja iz liste svih stanja automata
            self.states.remove(state)

            # uklanjanje nedohvatljivog stanja iz liste svih prihvatljivih stanja automata
            if state in self.acceptableStates:
                self.acceptableStates.remove(state)

            # uklanjanje nedohvatljivog stanja iz definicije funkcije prijelaza automata
            transitions = [transition for transition in self.transitionFunction if transition[0] == state]
            for transition in transitions:
                self.transitionFunction.pop(transition)
            
        # pretvorba skupa stanja nazad u listu, i sortiranje liste
        self.states = list(self.states)
        self.states.sort()

        # pretvordba skupa prihvatljivih stanja nazad u listu, i sortiranje liste
        self.acceptableStates = list(self.acceptableStates)
        self.acceptableStates.sort()

    # pomoćna funkcija čija svrha je pronalazak svih istovjetnih stanja, i spajanje takvih stanja u jedno
    def mergeNondistinguishableStates(self):

        # korišteni algoritam je Algoritam 3 iz udžbenika(str. 25.-27.), pa je prvi korak iniciranje tablice
        table = {}
        propagationTable = {}
        for i in range(1, len(self.states)):
            for j in range(i):
                table[(self.states[i],self.states[j])] = 0
                propagationTable[(self.states[i],self.states[j])] = []

        # svrha varijable iter je iteriranje po svih parovima stanja
        iter = list(table)
        iter.sort()

        # pronalazak parova u kojima članovi nemaju istu prihvatljivost, i označavanje takvih parova u tablici kao 1
        for el in iter:
            flag1 = False
            flag2 = False
            if el[0] in self.acceptableStates:
                flag1 = True
            if el[1] in self.acceptableStates:
                flag2 = True
            if flag1 != flag2:
                table[el] = 1

        # prolazak kroz sve elemente tablice sa svrhom identifikacije različitih stanja
        for el in iter:

            # ukoliko smo došli na par stanja koji je označen kao 1 tj. stanja su različita, nemamo što provjeravati, idemo na sljedeći korak
            if table[el] == 1:
                continue

            # računanje stanja prijelaza za prvi i drugi element para stanja koji trenutno obrađujemo
            states1 = [self.transitionFunction[transition] for transition in self.transitionFunction if transition[0] == el[0]]
            states2 = [self.transitionFunction[transition] for transition in self.transitionFunction if transition[0] == el[1]]

            # provjera istovjetnosti stanja za svaki par prijelaza
            flag = False
            for i in range(len(states1)):
                state1 = states1[i]
                state2 = states2[i]

                # izvođenje algoritma ovisi o tome da je leksikografski veće stanje na prvom mjestu, pa ovdje vršimo zamjenu ako to nije slučaj
                if state1 < state2:
                    state1,state2 = state2,state1

                # provjera različitosti stanja je nužna jer postoji mogućnost da oba stanja za neki znak prelaze u isto stanje, i tada nemamo što provjeravati
                if state1 != state2:

                    # ukoliko stanja koja provjeravamo za neki ulazni znak prelaze u stanja za koja znamo da su različita, nužno su i stanja koja provjeravamo različita
                    if table[(state1,state2)] == 1:
                        flag = True

                    # spremamo stanja koja trenutno provjeravamo u listu koja pripada stanjima u koja naša trenutna stanja prelaze, kako bismo mogli promijeniti trenutno provjeravana stanja ako se stanja u koja trenutno prelazimo u nekom trenutku identificiraju kao različita
                    else:
                        propagationTable[(state1,state2)].append(el)
                
                # zastavica označava da smo trenutni par stanja označili kao različita, i sad je potrebno rekurzivno sve parove koji ovise o trenutnom paru također označiti kao različite
                if flag:

                    # koristimo BFS, pa nam stoga treba red
                    queue = [el]
                    while len(queue) != 0:
                        state = queue.pop(0)
                        for propagation in propagationTable[state]:
                            if table[propagation] == 0:
                                queue.append(propagation)
                        table[state] = 1
        
        # istovjetna stanja prepoznajemo po tome što je vrijednost njihovog para u tablici jednaka nuli
        undistinguishableStates = [el for el in table if table[el] == 0]

        # u ovu listu ćemo spremati sve skupove stanja koja treba združiti
        mergedStates = []

        # obrađujemo jedan po jedan par istovjetnih stanja, i stoga izvodimo petlju dok god ih ne obradimo sve
        while len(undistinguishableStates) != 0:
            
            # stvaramo novi skup u koji ćemo na temelju svojstva tranzitivnosti relacije istovjetnosti dodavati sva istovjetna stanja
            newMerge = set()

            # prvo stanje uzimamo kao prvi element liste parova istovjetnih stanja
            state = undistinguishableStates.pop(0)

            # dodavanje prva dva stanja u skup svih istovjetnih stanja
            newMerge.add(state[0])
            newMerge.add(state[1])

            # izvodit ćemo sljedeću petlju dok god ne budemo u ostalim istovjetnim stanjima mogli pronaći ijedan par koji odgovara elementima trenutnog skupa
            flag = True
            while flag:

                # u varijablu indexes ćemo spremati indekse onih parova koje treba ubaciti u trenutni skup
                indexes = []

                # za svaki par istovjetnih stanja koje dosad nismo spojili u neki u skup provjeravamo imaju li zajednički element s trenutnim skupom
                for i in range(len(undistinguishableStates)):
                    if undistinguishableStates[i][0] in newMerge or undistinguishableStates[i][1] in newMerge:
                        indexes.append(i)

                # ukoliko u listi indexes nema ništa, više ne možemo ništa spariti i prekidamo petlju
                if len(indexes) == 0:
                    flag = False

                # inače smo pronašli barem jedan par stanja koji ćemo spojiti s trenutnim skupom
                else:

                    # obrtanje indeksa radi potencijalnih nuspojava pri brisanju odgovarajućih parova iz liste istovjetnih stanja
                    indexes = indexes[::-1]

                    # dodavanje oba elementa para u skup
                    for index in indexes:
                        newMerge.add(undistinguishableStates[index][0])
                        newMerge.add(undistinguishableStates[index][1])

                    # brisanje para iz liste istovjetnih stanja
                    for index in indexes:
                        undistinguishableStates.pop(index)

            # u varijabli mergedStates čuvamo sve skupove stanja, i sada u nju dodajemo novi skup
            mergedStates.append(newMerge)

        # pretvaranje listi stanja i prihvatljivih stanja u skupove radi lakšeg brisanja i dodavanja elemenata
        self.acceptableStates = set(self.acceptableStates)
        self.states = set(self.states)
        
        # petlju ponavljamo za svako stanje u listu skupova mergedStates
        for state in mergedStates:

            # pretvaranje skupa u listu
            l = list(state)

            # sortiranje liste i uzimanje leksikografski najmanjeg člana kao oznaku ovog stanja, sva ostala ekvivalentna stanja ćemo zamijeniti s ovim stanjem
            l.sort()
            newState = l[0]

            # svaki element tog skupa koji nije početni tj. leksikografski najmanji brišemo i na prikladan način mijenjamo u definiciji automata
            for el in l[1:]:

                # ukoliko je to stanje u skupu prihvatljivih stanja, mijenjamo ga s novom oznakom tog zajedničkog stanja
                if el in self.acceptableStates:
                    self.acceptableStates.remove(el)
                    self.acceptableStates.add(newState)

                # mičemo stanje iz skupa svih stanja automata
                self.states.remove(el)

                # ukoliko je to stanje početno stanje, mijenjamo ga s novom oznakom tog zajedničkog stanja
                if self.startState == el:
                    self.startState = newState

                # brisanje stanja iz funkcije prijelaza
                for k in self.transitionFunction:

                    # za svaki prijelaz koji završava u tom stanju, to stanje mijenjamo novom oznakom zajedničkog stanja
                    if self.transitionFunction[k] == el:
                        self.transitionFunction[k] = newState

                # u varijabli keys nalaze se svi parovi prijelaza za stanje koje brišemo
                keys = [k for k in self.transitionFunction if k[0] == el]
                
                # brisanje prijelaza stanja kojeg brišemo iz funkcije prijelaza
                for key in keys:
                    self.transitionFunction.pop(key)

        # pretvorba skupa stanja nazad u listu, i sortiranje liste
        self.states = list(self.states)
        self.states.sort()

        # pretvorba skupa prihvatljivih stanja nazad u listu, i sortiranje liste
        self.acceptableStates = list(self.acceptableStates)
        self.acceptableStates.sort()

    # funkcija generira znakovni niz koji odgovara traženoj definiciji automata                   
    def definition(self):

        # u varijablu retVal ćemo spremiti definiciju automata
        retVal = ""

        # računanje pravilnog ispisa svih stanja automata
        states = ""
        self.states.sort()
        for state in self.states:
            states += state + ","
        states = states[:len(states)-1]
        retVal += states + "\n"

        # računanje pravilnog ispisa svih znakove abecede automata
        symbols = ""
        self.symbols.sort()
        for symbol in self.symbols:
            symbols += symbol + ","
        symbols = symbols[:len(symbols)-1]
        retVal += symbols + "\n"

        # računanje pravilnog ispisa svih prihvatljivih stanja automata
        acceptableStates = ""
        self.acceptableStates.sort()
        for state in self.acceptableStates:
            acceptableStates += state + ","
        acceptableStates = acceptableStates[:len(acceptableStates)-1]
        retVal += acceptableStates + "\n"

        # računanje pravilnog ispisa početnog stanja automata
        retVal += self.startState + "\n"

        # računanje pravilnog ispisa funkcije prijelaza automata
        transitions = []
        for el in self.transitionFunction: 
            transition = el[0] + "," + el[1] + "->" + self.transitionFunction[(el[0],el[1])]
            transitions.append(transition)
        transitions.sort()
        for transition in transitions:
            retVal += transition + "\n"

        # vraćanje znakovnog niza koji odgovora definiciji automata
        return retVal

# glavna funkcija u programu koja čita ulaz, parsira ga, inicijalizira objekt tipa DKA, minimizira taj automat, i potom vraća njegovu definiciju
def main():

    # u varijablu lines spremamo pojedine redove u ulazu
    lines = []
    try:
        while True:
            i = input()
            lines.append(i)
    except EOFError:
        pass

    # čitanje svih stanja automata
    states = lines[0].split(",")

    # čitanje svih simbola koji se mogu naći na ulazu automata
    symbols = lines[1].split(",")

    # čitanje svih prihvatljivih stanja automata, uzevši u obzir da je moguće da je taj redak u ulazu prazan
    if len(lines[2]) != 0:
        acceptableStates = lines[2].split(",")
    else:
        acceptableStates = []

    # čitanje početnog stanja automata
    startState = lines[3]

    # ostale linije u ulazu označavaju funkciju prijelaza
    transitionFunctionInput = lines[4:]

    # čitanje svakog retka koji označava funkciju prijelaza, te potom parsiranje i dodavanje u varijablu funkcije prijelaza
    transitionFunction = []
    for el in transitionFunctionInput:
        el = el.split("->")
        start = el[0].split(",")[0]
        symbol = el[0].split(",")[1]
        finish = el[1].split(",")[0]
        transitionFunction.append((start,symbol,finish))

    # inicijaliziranje varijable tipa DKA
    automaton = DKA(states,symbols,acceptableStates,startState,transitionFunction)

    # pozivanje funkcije minimiziranja DKA
    automaton.minimize()

    # vraćanje definicije minimiziranog automata
    return automaton.definition()

# pokretanje glavne funkcije i ispis rezultata
print(main())