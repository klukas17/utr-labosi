'''
    programsko rješenje za 4. laboratorijsku vježbu na kolegiju "Uvod u teoriju računarstva"
    autor: Mihael Miličević
'''

# osnovna klasa za modeliranje parsera tehnikom rekurzivnog spusta
class RecursiveDescentParser():

    # konstruktor klase parsera koji kao arguemnt prima ulazni niz, te dodatno inicijalizira indeks i obrađene nezavršne znakove
    def __init__(self, sequence):
        self.nonTerminalSymbols = ""
        self.it = self.InputIterator(sequence)
        self.currSymbol = self.it.next()

    # produkcija nezavršnog znaka S
    def S(self):

        # zapis obrade trenutnog nezavršnog znaka
        self.nonTerminalSymbols += "S"

        # trenutni završni znak je a
        if self.currSymbol == "a":
            self.currSymbol = self.it.next()
            self.A()
            self.B()

        # trenutni završni znak je b
        elif self.currSymbol == "b":
            self.currSymbol = self.it.next()
            self.B()
            self.A()

        # parsiranje neuspješno
        else:
            raise RecursiveDescentParser.ParsingFailed()
        
    # produkcija nezavršnog znaka A
    def A(self):

        # zapis obrade trenutnog nezavršnog znaka
        self.nonTerminalSymbols += "A"

        # trenutni završni znak je b
        if self.currSymbol == "b":
            self.currSymbol = self.it.next()
            self.C()

        # trenutni završni znak je a
        elif self.currSymbol == "a":
            self.currSymbol = self.it.next()

        # parsiranje neuspješno
        else:
            raise RecursiveDescentParser.ParsingFailed()

    # produkcija nezavršnog znaka B
    def B(self):
        
        # zapis obrade trenutnog nezavršnog znaka
        self.nonTerminalSymbols += "B"

        # pročitan je cijeli niz ili ulazni znak nije c
        if self.currSymbol != "c":
            return

        # ulazni znak je c
        if self.currSymbol == "c":
            self.currSymbol = self.it.next()

            # ulazni znak je c 
            if self.currSymbol == "c":
                self.currSymbol = self.it.next()

                self.S()

                # ulazni znak je b
                if self.currSymbol == "b":
                    self.currSymbol = self.it.next()

                    # ulazni znak je c
                    if self.currSymbol == "c":
                        self.currSymbol = self.it.next()

                    # parsiranje neuspješno
                    else:
                        raise RecursiveDescentParser.ParsingFailed()

                # parsiranje neuspješno
                else:
                    raise RecursiveDescentParser.ParsingFailed()

            # parsiranje neuspješno
            else:
                raise RecursiveDescentParser.ParsingFailed()

    # produkcija nezavršnog znaka C
    def C(self):
        
        # zapis obrade trenutnog nezavršnog znaka
        self.nonTerminalSymbols += "C"

        self.A()
        self.A()

    # definicija iznimke koja se baci kada je parsiranje neuspješno
    class ParsingFailed(Exception):
        pass

    # iterator po ulaznom nizu
    class InputIterator():

        # konstruktor iteratora
        def __init__(self, input):
            self.input = input
            self.size = len(input)
            self.currIndex = 0

        # funkcija koja vraća sljedeći znak u nizu
        def next(self):

            # nismo došli do kraja niza
            if self.currIndex < self.size:
                retVal = self.input[self.currIndex]
                self.currIndex += 1
                return retVal

            # došli smo do kraja niza i vraćamo None
            else:
                return None 

# glavna funkcija u programu koja čita ulaz, inicijalizira objekt parsera i potom parsira niz
def main():

    # čitanje ulaznog niza 
    sequence = input()

    # incijalizacija objekta parsera
    RDP = RecursiveDescentParser(sequence)

    # zastavica u kojoj ćemo pamtiti je li parsiranje bilo neuspješno
    flag = True

    # pokretanje parsiranja
    try:
        RDP.S()
    
    # parsiranje nije uspješno
    except RecursiveDescentParser.ParsingFailed:
        flag = False

    # ispis svih obrađivanih nezavršnih znakova
    print(RDP.nonTerminalSymbols)

    # pročitan je cijeli ulazni niz i nije bačena iznimka za neuspješno parsiranje
    if not RDP.currSymbol and flag:
        print("DA")

    # parsiranje neuspješno, početni niz ne pripada gramatici
    else:
        print("NE")

# pokretanje glavnog programa
main()