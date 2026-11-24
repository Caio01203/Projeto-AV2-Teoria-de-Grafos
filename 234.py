from bisect import bisect_left

# cria um nó
class No:
    def __init__(self, chaves=None, filhos=None):
        self.chaves = chaves or []
        self.filhos = filhos or []

# confere se o nó possui filhos
    @property
    def folha(self):
        return not self.filhos

#cria a árvore
class Arvore234:
    def __init__(self):
        self.raiz = No()

# procura um valor na árvore
    def buscar(self, k, no=None):
        no = no or self.raiz
        i = bisect_left(no.chaves, k)

        if i < len(no.chaves) and no.chaves[i] == k:
            return True
        
        return False if no.folha else self.buscar(k, no.filhos[i])

# realizada o balanceamento da inserção
    def _split(self, pai, i):
        cheio = pai.filhos[i]
        pai.chaves.insert(i, cheio.chaves[1])
        pai.filhos[i:i+1] = [
            No([cheio.chaves[0]], cheio.filhos[:2]),
            No([cheio.chaves[2]], cheio.filhos[2:])
        ]

# insere um novo nó
    def inserir(self, k):

        if self.buscar(k):
            return False
        
        if len(self.raiz.chaves) == 3:
            self.raiz = No([], [self.raiz])
            self._split(self.raiz, 0)
        no = self.raiz

        while not no.folha:
            i = bisect_left(no.chaves, k)

            if len(no.filhos[i].chaves) == 3:
                self._split(no, i)

                if k > no.chaves[i]:
                    i += 1
            no = no.filhos[i]
        no.chaves.insert(bisect_left(no.chaves, k), k)
        return True

# faz a fusão de um nó para removê-lo
    def _fundir(self, no, i):
        esq, dir_ = no.filhos[i], no.filhos.pop(i + 1)
        esq.chaves += [no.chaves.pop(i)] + dir_.chaves
        esq.filhos += dir_.filhos

# confere se o nó inserido pelo usuário existe
    def remover(self, k):

        if not self.buscar(k):
            return False
        
        self._rem(self.raiz, k)
        if not self.raiz.chaves and not self.raiz.folha:
            self.raiz = self.raiz.filhos[0]
        return True

# remove um nó
    def _rem(self, no, k):
        i = bisect_left(no.chaves, k)

        if i < len(no.chaves) and no.chaves[i] == k:

            if no.folha:
                no.chaves.pop(i)

            elif len(no.filhos[i].chaves) >= 2:
                atual = no.filhos[i]

                while not atual.folha: atual = atual.filhos[-1]
                no.chaves[i] = pred = atual.chaves[-1]
                self._rem(no.filhos[i], pred)

            elif len(no.filhos[i + 1].chaves) >= 2:
                atual = no.filhos[i + 1]

                while not atual.folha: atual = atual.filhos[0]
                no.chaves[i] = succ = atual.chaves[0]
                self._rem(no.filhos[i + 1], succ)

            else:
                self._fundir(no, i)
                self._rem(no.filhos[i], k)

        else:
            if len(no.filhos[i].chaves) == 1:

                if i > 0 and len(no.filhos[i - 1].chaves) >= 2:
                    f, irm = no.filhos[i], no.filhos[i - 1]
                    f.chaves.insert(0, no.chaves[i - 1])
                    no.chaves[i - 1] = irm.chaves.pop()

                    if not f.folha: f.filhos.insert(0, irm.filhos.pop())

                elif i < len(no.chaves) and len(no.filhos[i + 1].chaves) >= 2:
                    f, irm = no.filhos[i], no.filhos[i + 1]
                    f.chaves.append(no.chaves[i])
                    no.chaves[i] = irm.chaves.pop(0)

                    if not f.folha: f.filhos.append(irm.filhos.pop(0))
                else:

                    if i == len(no.chaves): i -= 1
                    self._fundir(no, i)
            self._rem(no.filhos[i], k)

# conta a quantidade de nós
    def contar_nos(self, no=None):
        no = no or self.raiz
        return 0 if not no.chaves else 1 + sum(self.contar_nos(f) for f in no.filhos)

# imprime a árvore
    def exibir(self, no=None, niv=0):
        no = no or self.raiz

        if not no.chaves: return print("(Vazia)")
        print("  " * niv + f"N{niv}: {no.chaves}")
        
        for f in no.filhos: self.exibir(f, niv + 1)

# menu do usuário
arv = Arvore234()
while True:
    nos = arv.contar_nos()
    print(f"\n[Nós: {nos} {'(OK >= 21)' if nos >= 21 else f'(Faltam {21 - nos})'}]")
    op = input("1:Inserir(s) | 2:Buscar | 3:Remover | 4:Exibir | 0:Sair -> ")
    if op == "0": break
    elif op == "1":
        for v in map(int, input("Valores (espaço): ").split()): arv.inserir(v)
    elif op == "2":
        print("Achou:", arv.buscar(int(input("Buscar: "))))
    elif op == "3":
        print("Removido:", arv.remover(int(input("Remover: "))))
    elif op == "4":
        arv.exibir()