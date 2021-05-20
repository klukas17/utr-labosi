'''
    programsko rješenje za 3. laboratorijsku vježbu na kolegiju "Uvod u teoriju računarstva"
    autor: Mihael Miličević
'''

# osnovna klasa za modeliranje DPA automata
class DPA():

    # konstrutor klase, kao argumente prima 7 varijabli koje predstavljaju uređenu sedmorku kojom se DPA formalno definira
    def __init__(self, states, symbols, stackSymbols, transitionFunction, startState, startStackSymbol, acceptableStates):
        self.states = states
        self.symbols = symbols
        self.stackSymbols = stackSymbols
        self.startState = startState
        self.startStackSymbol = startStackSymbol
        self.acceptableStates = acceptableStates
        self.transitionFunction = {}
        for el in transitionFunction:
            self.transitionFunction[(el[0],el[1],el[2])] = (el[3],el[4])
        if self.startStackSymbol == "":
            self.startStackSymbol = "$"

    # funkcija kao parametar prima neki ulazni niz, a kao rezultat vraća ispis stoga i svih stanja u kojima se automat nasao u svakom koraku
    def validate(self, inputString):

        # iniciranje povratne vrijednosti, početnog stanja i početnog znaka na stogu
        retVal = ""
        currentState = self.startState
        stack = self.startStackSymbol

        # ispis početne konfiguracije automata
        retVal += f'{currentState}#{stack}'

        # za svaki znak u ulaznom nizu odredi prijelaz
        for el in inputString:

            # ispitaj epsilon prijelaze
            while (currentState, "$", stack[0]) in self.transitionFunction:

                # određivanje sljedećeg stanja i ažuriranja stoga
                next = self.transitionFunction[(currentState, "$", stack[0])]
                currentState = next[0]
                stackChange = next[1]

                stack = stack[1:]
                if stackChange != "$":
                    stack = stackChange + stack

                # provjera je li stog prazan
                if len(stack) == 0:
                    stack = "$"

                # ažuriraj povratnu vrijednost
                retVal += f'|{currentState}#{stack}'

            # ako ne postoji definiran prijelaz, izađi iz funkcije
            if (currentState, el, stack[0]) not in self.transitionFunction:
                retVal += "|fail|0"
                return retVal

            # postoji definiran prijelaz
            else:

                # određivanje sljedećeg stanja i ažuriranja stoga
                next = self.transitionFunction[(currentState, el, stack[0])]
                currentState = next[0]
                stackChange = next[1]

                stack = stack[1:]
                if stackChange != "$":
                    stack = stackChange + stack

                # provjera je li stog prazan
                if len(stack) == 0:
                    stack = "$"

                # ažuriranje povratne vrijednosti
                retVal += f'|{currentState}#{stack}'

        # ako smo pročitali sve ulazne znakove a nismo završili u prihvatljivom stanju, tražimo epsilon prijelaze
        while currentState not in self.acceptableStates and (currentState, "$", stack[0]) in self.transitionFunction:

            # određivanje sljedećeg stanja i ažuriranja stoga
            next = self.transitionFunction[(currentState, "$", stack[0])]
            currentState = next[0]
            stackChange = next[1]

            stack = stack[1:]
            if stackChange != "$":
                stack = stackChange + stack

            # provjera je li stog prazan
            if len(stack) == 0:
                stack = "$"

            # ažuriranje povratne vrijednosti
            retVal += f'|{currentState}#{stack}'
        
        # niz je prihvaćen
        if currentState in self.acceptableStates:
            retVal += "|1"
        
        # niz nije prihvaćen
        else:
            retVal += "|0"

        # vraćanje povratne vrijendnosti
        return retVal

# glavna funkcija u programu koja čita ulaz, parsira ga, inicijalizira objekt tipa DPA, i simulira parsiranje ulaznih nizova
def main():
    
    # u varijablu lines spremamo pojedine redove u ulazu
    lines = []
    try:
        while True:
            i = input()
            lines.append(i)
    except EOFError:
        pass

    # rastavljanje prvog retka na sve nizove ulaznih znakova, i potom rastavljanje svakog niza na listu znakova
    inputStrings = lines[0].split("|")
    for i in range(len(inputStrings)):
        inputStrings[i] = inputStrings[i].split(",")

     # čitanje svih stanja automata
    states = lines[1].split(",")

    # čitanje svih simbola koji se mogu naći na ulazu automata
    symbols = lines[2].split(",")

    # čitanje svih znakova stoga
    stackSymbols = lines[3].split(",")

    # čitanje svih prihvatljivih stanja automata, uzevši u obzir da je moguće da je taj redak u ulazu prazan
    if len(lines[4]) != 0:
        acceptableStates = lines[4].split(",")
    else:
        acceptableStates = []

    # čitanje početnog stanja automata
    startState = lines[5]

    # čitanje početnog znaka stoga
    startStackSymbol = lines[6]

    # ostale linije u ulazu označavaju funkciju prijelaza
    transitionFunctionInput = lines[7:]

    # čitanje svakog retka koji označava funkciju prijelaza, te potom parsiranje i dodavanje u varijablu funkcije prijelaza
    transitionFunction = []
    for el in transitionFunctionInput:
        el = el.split("->")
        start = el[0].split(",")
        end = el[1].split(",")
        startingState = start[0]
        symbol = start[1]
        startingStackSymbol = start[2]
        endState = end[0]
        finishStackSymbol = end[1]
        transitionFunction.append((startingState, symbol, startingStackSymbol, endState, finishStackSymbol))

    # iniciranje varijable tipa ENKA i rezultata koji funkcija main vraca
    automaton = DPA(states, symbols, stackSymbols, transitionFunction, startState, startStackSymbol, acceptableStates)
    retVal = ""
    
    # račcunanje svih prijelaza za svaki znakovni niz na ulazu
    for el in inputStrings:
        retVal += automaton.validate(el) + "\n"

    # vraćanje konačnog rješenja, u obliku znakovnog niza gdje su za svaki ulazni niz u posebnom retku prikazana sva stanja automata i stog za taj niz
    return retVal

print(main())