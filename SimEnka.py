'''
    programsko rjesenje za 1. laboratorijsku vjezbu na kolegiju "Uvod u teoriju racunarstva"
    autor: Mihael Milicevic
'''

# osnovna klasa za modeliranje epsilon-NKA automata
class ENKA():

    # konstrutor klase, kao argumente prima 5 varijabli koje predstavljaju uredjenu petorku kojom se epsilon-NKA formalno definira
    def __init__(self, states, symbols, acceptableStates, startState, transitionFunction):
        self.states = states
        self.symbols = symbols
        self.acceptableStates = acceptableStates
        self.startState = startState
        self.transitionFunction = {}
        for el in transitionFunction:
            self.transitionFunction[(el[0],el[1])] = el[2]

    # funkcija kao parametar prima neki ulazni tekst, a kao rezultat vraca ispis svih stanja u kojim se automat nasao u svakom koraku
    def validate(self, inputString):

        # inicijalizira se varijabla retVal, i u listu trenutnih stanja se doda pocetno stanje
        retVal = ""
        currentStates = []
        currentStates.append(self.startState)

        # racunanje mogucih epsilon prijelaza iz pocetnog stanja, jer su to sve stanja u kojima se automat nasao u trenutnom koraku
        currentStates = set(currentStates)
        visitedStates = set()
        while True:
            flag = True
            for state in currentStates:
                if state not in visitedStates and (state,"$") in self.transitionFunction:
                    currentStates = currentStates.union(set(self.transitionFunction[(state, "$")]))
                    flag = False
                visitedStates.add(state)
            if flag:
                break

        # pretvaranje skupa trenutnih stanja u listu, i sortiranje te liste
        currentStates = list(currentStates)
        currentStates.sort()

        # ispis stanja u kojima se automat nasao prije citanja prvog znaka
        for state in currentStates:
            retVal += state + ","
        retVal = retVal[:len(retVal)-1]

        # za svaki znak u ulaznom nizu ponavljat cemo sljedecu petlju
        for el in inputString:

            # dodavanje znaka | jer prelazimo na citanje iduceg znaka
            retVal += "|"

            # ukoliko se ne nalazimo niti u jednom stanju, moramo ispisati # i vratiti se na pocetak petlje
            if currentStates == ["#"]:
                retVal += "#"
                continue

            # racunanje svih stanja u kojima ce se automat naci u iducem koraku koristeci funkciju prijelaza
            nextStates = set()
            for state in currentStates:
                if (state,el) in self.transitionFunction:
                    if self.transitionFunction[(state,el)] != ["#"]:
                        nextStates = nextStates.union(set(self.transitionFunction[(state,el)]))
                
            # kada smo izracunali sva stanja u koja mozemo preci preko funkcije prijelaza, potrebno je izracunati sva stanja u koja mozemo doci epsilon prijelazima
            visitedStates = set()
            while True:
                flag = True
                for state in nextStates:
                    if state not in visitedStates and (state, "$") in self.transitionFunction:
                        nextStates = nextStates.union(set(self.transitionFunction[(state,"$")]))
                        flag = False
                    visitedStates.add(state)
                if flag:
                    break

            # ukoliko je specificirano da neki prijelaz vodi automat u # tj. ne vodi ga u niti jedno stanje, brisemo taj prijelaz iz skupa sljedecih stanja
            if "#" in nextStates:
                nextStates.remove("#")

            # ukoliko nam se dogodilo da nam je lista sljedecih prijelaza prazna, u nju dodajemo znak za prazan skup # i nastavljamo na iduci korak petlje
            if len(nextStates) == 0:
                currentStates = ["#"]
                retVal += "#"
                continue
            
            # dodavanje svih trenutnih stanja na izlaz funkcije
            currentStates = list(nextStates)
            currentStates.sort()
            for state in currentStates:
                retVal += state + ","
            retVal = retVal[:len(retVal)-1]

        # vracanje znakovnog niza koji oznacava sva stanja u kojima se automat nasao u svakom koraku
        return retVal

# glavna funkcija u programu koja cita ulaz, parsira ga, inicijalizira objekt tipa ENKA i racuna potreban ispis za sve ulazne nizove znakova
def main():

    # u varijablu lines spremamo pojedine redove u ulazu
    lines = []
    try:
        while (i := input()):
            lines.append(i)
    except EOFError:
        pass

    # rastavljanje prvog retka na sve nizove ulaznih znakova, i potom rastavljanje svakog niza na listu znakova
    inputStrings = lines[0].split("|")
    for i in range(len(inputStrings)):
        inputStrings[i] = inputStrings[i].split(",")

    # citanje svih stanja automata
    states = lines[1].split(",")

    # citanje svih simbola koji se mogu naci na ulazu automata
    symbols = lines[2].split(",")

    # citanje svih prihvatljivih stanja automata, uzevsi u obzir da je moguce da je taj redak u ulazu prazan
    if len(lines[3]) != 0:
        acceptableStates = lines[3].split(",")
    else:
        acceptableStates = []

    # citanje pocetnog stanja automata
    startState = lines[4]

    # ostale linije u ulazu oznacavaju funkciju prijelaza
    transitionFunctionInput = lines[5:]

    # citanje svakog retka koji oznacava funkciju prijelaza, te potom parsiranje i dodavanje u varijablu funkcije prijelaza
    transitionFunction = []
    for el in transitionFunctionInput:
        el = el.split("->")
        start = el[0].split(",")[0]
        symbol = el[0].split(",")[1]
        finish = el[1].split(",")
        transitionFunction.append((start, symbol, finish))

    # iniciranje varijable tipa ENKA i rezultata koji funkcija main vraca
    automaton = ENKA(states, symbols, acceptableStates, startState, transitionFunction)
    retVal = ""
    
    # racunanje svih prijelaza za svaki znakovni niz na ulazu
    for el in inputStrings:
        retVal += automaton.validate(el) + "\n"

    # vracanje konacnog rjesenja, u obliku znakovnog niza gdje su za svaki ulazni niz u posebnom retku prikazana sva stanja automata za taj niz
    return retVal

# pokretanje glavne funkcije i ispis rezultata
print(main())