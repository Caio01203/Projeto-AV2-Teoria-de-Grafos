# definindo constantes para as cores
VERMELHO, PRETO = 1, 0

# cria o nó com sua chave e cor
class No:
    def __init__(self, chave, cor = VERMELHO, nil = None):
        self.chave, self.cor, self.pai = chave, cor, nil
        self.filhos = [nil, nil]

# cria a árvore
class ArvoreRubroNegra:
    def __init__(self):
        self.NIL = No(None, PRETO)
        self.NIL.pai = self.NIL.filhos = [self.NIL, self.NIL]
        self.raiz, self.total = self.NIL, 0

# percorre a árvore até achar a chave desejada
    def buscar(self, chave):
        atual = self.raiz

        while atual != self.NIL and chave != atual.chave:
            atual = atual.filhos[chave > atual.chave]

        return atual if atual != self.NIL else None
    
# faz a rotação dos nós
    def _rotacionar(self, x, d):
        o = 1 - d
        y = x.filhos[o]

        x.filhos[o] = y.filhos[d]
        if y.filhos[d] != self.NIL:
            y.filhos[d].pai = x
        y.pai = x.pai

        if x.pai == self.NIL:
            self.raiz = y

        else:
            x.pai.filhos[x == x.pai.filhos[1]] = y
        y.filhos[d], x.pai = x, y

# insere uma nova chave
    def inserir(self, chave):
        novo = No(chave, VERMELHO, self.NIL)
        pai, atual = self.NIL, self.raiz

        while atual != self.NIL:
            pai = atual

            if chave == atual.chave:
                return False
            
            atual = atual.filhos[chave > atual.chave]
        novo.pai = pai

        if pai == self.NIL:
            self.raiz = novo

        else:
            pai.filhos[chave > pai.chave] = novo
        self.total += 1

        while novo.pai.cor == VERMELHO:
            avo = novo.pai.pai
            d = int(novo.pai == avo.filhos[1])
            tio = avo.filhos[1 - d]

            if tio.cor == VERMELHO:
                novo.pai.cor = tio.cor = PRETO
                avo.cor, novo = VERMELHO, avo

            else:
                if novo == novo.pai.filhos[1 - d]:
                    novo = novo.pai
                    self._rotacionar(novo, d)
                novo.pai.cor, avo.cor = PRETO, VERMELHO
                self._rotacionar(avo, 1 - d)
        self.raiz.cor = PRETO
        return True

# atualiza o pai de 'u'
    def _transplantar(self, u, v):

        if u.pai == self.NIL:
            self.raiz = v

        else:
            u.pai.filhos[u == u.pai.filhos[1]] = v
        v.pai = u.pai

# faz a exclusão da chave informada
    def excluir(self, chave):
        z = self.buscar(chave)

        if not z:
            return False
        
        y, cor_orig = z, z.cor

        if self.NIL in z.filhos:
            x = z.filhos[int(z.filhos[0] == self.NIL)]
            self._transplantar(z, x)

        else:
            y = z.filhos[1]

            while y.filhos[0] != self.NIL:
                y = y.filhos[0]
            cor_orig, x = y.cor, y.filhos[1]

            if y.pai == z:
                x.pai = y

            else:
                self._transplantar(y, x)
                y.filhos[1] = z.filhos[1]
                y.filhos[1].pai = y
            self._transplantar(z, y)
            y.filhos[0], y.filhos[0].pai, y.cor = z.filhos[0], y, z.cor
        self.total -= 1

        if cor_orig == PRETO:

            while x != self.raiz and x.cor == PRETO:
                d = int(x == x.pai.filhos[1])
                irmao = x.pai.filhos[1 - d]

                if irmao.cor == VERMELHO:
                    irmao.cor, x.pai.cor = PRETO, VERMELHO
                    self._rotacionar(x.pai, d)
                    irmao = x.pai.filhos[1 - d]

                if all(f.cor == PRETO for f in irmao.filhos):
                    irmao.cor, x = VERMELHO, x.pai

                else:

                    if irmao.filhos[1 - d].cor == PRETO:
                        irmao.filhos[d].cor, irmao.cor = PRETO, VERMELHO
                        self._rotacionar(irmao, 1 - d)
                        irmao = x.pai.filhos[1 - d]
                    irmao.cor, x.pai.cor, irmao.filhos[1 - d].cor = x.pai.cor, PRETO, PRETO
                    self._rotacionar(x.pai, d)
                    x = self.raiz
            x.cor = PRETO
        return True

# retorna lista com as chaves ordenadas
    def em_ordem(self, no=None):
        no = self.raiz if no is None else no

        if no == self.NIL:
            return []
        
        return self.em_ordem(no.filhos[0]) + [f"{no.chave}({'V' if no.cor else 'P'})"] + self.em_ordem(no.filhos[1])

# menu do usuário
if __name__ == "__main__":
    arn = ArvoreRubroNegra()

    while arn.total < 21:
        for v in input(f"[{arn.total}/21 nós] Digite inteiro(s): ").split():
            if v.lstrip("-").isdigit():
                arn.inserir(int(v))

    while True:
        print(f"\nNós ({arn.total}):", " ".join(arn.em_ordem()))
        op = input("[1]Inserir [2]Buscar [3]Excluir [0]Sair: ").strip()
        if op == "0":
            break

        val = input("Número: ").strip()
        if op in ("1", "2", "3") and val.lstrip("-").isdigit():
            n = int(val)

            if op == "1":
                print("OK" if arn.inserir(n) else "Já existe")

            elif op == "2":
                res = arn.buscar(n)
                print(f"Achou ({'V' if res.cor else 'P'})" if res else "Não achou")

            elif op == "3":
                print("OK" if arn.total > 21 and arn.excluir(n) else "Não removido (mínimo 21 ou inexistente)")