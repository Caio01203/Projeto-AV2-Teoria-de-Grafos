# biblioteca 
import math

# cria o nó e seus ponteiros
class No:
    def __init__(self, ponto, filho_esq = None, filho_dir = None):
        self.ponto, self.filho_esq, self.filho_dir = ponto, filho_esq, filho_dir

# cria a árvore com seu número de dimensões
class Arvore:
    def __init__(self, pontos = None, k = 2):
        self.k = k
        self.raiz = self._construir(list(pontos)) if pontos else None

# constrói a árvore
    def _construir(self, pts, prof = 0):

        if not pts:
            return None
        
        eixo = prof % self.k
        pts.sort(key = lambda x: x[eixo])
        meio = len(pts) // 2
        return No(pts[meio], self._construir(pts[:meio], prof + 1), self._construir(pts[meio + 1:], prof + 1))
    
# percorre a árvore checando os nós existentes
    def _listar(self, no):

        if no:
            yield no.ponto
            yield from self._listar(no.filho_esq)
            yield from self._listar(no.filho_dir)

# checa a áltura da árvore
    def altura(self, no):
        return 0 if not no else 1 + max(self.altura(no.filho_esq), self.altura(no.filho_dir))

# faz o balanceamento
    def _balancear(self):
        pts = list(self._listar(self.raiz))

        if len(pts) > 2 and self.altura(self.raiz) > math.floor(math.log2(len(pts))) + 2:
            print("[Balanceamento] Rebalanceando árvore...")
            self.raiz = self._construir(pts)

# faz a busca do nó requerido
    def buscar(self, ponto, no = None, prof = 0, inicio = True):
        no = self.raiz if inicio else no

        if not no:
            return False
        
        if no.ponto == ponto:
            return True
        
        eixo = prof % self.k
        proximo = no.filho_esq if ponto[eixo] < no.ponto[eixo] else no.filho_dir
        return self.buscar(ponto, proximo, prof + 1, False)

# confere se o nó já existe para assim adicioná-lo à árvore
    def inserir(self, ponto):

        if self.buscar(ponto):
            return print("Ponto já existe.")
        
        self.raiz = self._inserir(self.raiz, ponto, 0)
        self._balancear()

# desce a árvore até achar nó vazio
    def _inserir(self, no, ponto, prof):

        if not no:
            return No(ponto)
        
        eixo = prof % self.k

        if ponto[eixo] < no.ponto[eixo]:
            no.filho_esq = self._inserir(no.filho_esq, ponto, prof + 1)
        else:
            no.filho_dir = self._inserir(no.filho_dir, ponto, prof + 1)
        return no

    def _minimo(self, no, eixo_alvo, prof):

        if not no:
            return None
        
        if prof % self.k == eixo_alvo:

            return no if not no.filho_esq else self._minimo(no.filho_esq, eixo_alvo, prof + 1)
        
        candidatos = [no, self._minimo(no.filho_esq, eixo_alvo, prof + 1), self._minimo(no.filho_dir, eixo_alvo, prof + 1)]
        return min((c for c in candidatos if c), key = lambda n: n.ponto[eixo_alvo])

# confirma se o nó existe
    def excluir(self, ponto):

        if not self.buscar(ponto):
            return print("Ponto não encontrado.")
        
        self.raiz = self._excluir(self.raiz, ponto, 0)
        self._balancear()
        print(f"Ponto {ponto} removido.")

# percorre a árvore buscando um nó para substituir o removido
    def _excluir(self, no, ponto, prof):

        if not no:
            return None
        
        eixo = prof % self.k

        if no.ponto == ponto:

            if no.filho_dir:
                m = self._minimo(no.filho_dir, eixo, prof + 1)
                no.ponto, no.filho_dir = m.ponto, self._excluir(no.filho_dir, m.ponto, prof + 1)

            elif no.filho_esq:
                m = self._minimo(no.filho_esq, eixo, prof + 1)
                no.ponto, no.filho_dir, no.filho_esq = m.ponto, self._excluir(no.filho_esq, m.ponto, prof + 1), None

            else:
                return None
            
            return no
        
        if ponto[eixo] < no.ponto[eixo]:
            no.filho_esq = self._excluir(no.filho_esq, ponto, prof + 1)

        else:
            no.filho_dir = self._excluir(no.filho_dir, ponto, prof + 1)
        return no

# imprimi os nós
    def exibir(self, no, prof = 0, lado = "Raiz"):

        if no:
            print(f"{'   ' * prof}[{lado} | Eixo {prof % self.k}] -> {no.ponto}")
            self.exibir(no.filho_esq, prof + 1, "Esq")
            self.exibir(no.filho_dir, prof + 1, "Dir")

# lê os dados inseridos pelo usuário
def ler_ponto(k = 2):

    while True:
        try:
            pts = tuple(int(v) for v in input(f"Digite {k} valores (ex: 10 20): ").split())

            if len(pts) == k:
                return pts
            
        except ValueError:
            pass
        print("Entrada inválida.")

# nós pré-estabelecidos
pontos_21 = [
    (50, 50), (25, 75), (75, 25), (10, 40), (30, 90), (60, 10), (85, 60),
    (5, 20), (15, 65), (28, 80), (45, 95), (55, 5), (68, 18), (80, 45),
    (92, 85), (12, 30), (22, 55), (35, 70), (62, 35), (78, 72), (95, 15)
]
arvore = Arvore(pontos_21)

# menu do usuário
while True:
    total = len(list(arvore._listar(arvore.raiz)))
    op = input(f"\n[Nós: {total} | Altura: {arvore.altura(arvore.raiz)}] 1-Inserir | 2-Excluir | 3-Buscar | 4-Exibir | 0-Sair: ")
    if op == "1": arvore.inserir(ler_ponto())
    elif op == "2": arvore.excluir(ler_ponto())
    elif op == "3": print("Encontrado!" if arvore.buscar(ler_ponto()) else "Não encontrado.")
    elif op == "4": arvore.exibir(arvore.raiz)
    elif op == "0": break