"""
rbtree.py
---------
Estrutura de dados: Árvore Rubro-Negra ("Bosque dos Corvos").

Reengenharia do núcleo de árvore encontrado no bundle original do jogo
"The Hanoi Tree" (funções minificadas `aa` = insert AVL, `Rr` = rebalance
por altura, `yu`/`vu` = rotações, `ms` = delete). Ali o invariante
verificado era numérico (fator de balanceamento / altura). Aqui o
invariante passa a ser qualitativo: a cor de cada nó (RED/BLACK) e a
altura-preta (black-height) de cada caminho raiz→folha, conforme o
Game Design Document (seção 4.2 — Árvore Rubro-Negra).

Cada nó representa um "ninho" ocupado por um "filhote de corvo" (chave
inteira). Filhotes nascem sempre RED (instável). A correção estrutural
é feita por duas ações mapeadas 1:1 nas mecânicas do jogo:

    - "repintar_ninho"    -> recoloração (tio vermelho)
    - "realocar_galho"    -> rotação simples ou dupla + recoloração
                              (tio preto/ausente)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict


class Color(Enum):
    RED = "red"
    BLACK = "black"


@dataclass
class Node:
    key: int
    color: Color = Color.RED
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None

    def is_red(self) -> bool:
        return self.color == Color.RED

    def sibling(self) -> Optional["Node"]:
        if self.parent is None:
            return None
        return self.parent.right if self is self.parent.left else self.parent.left

    def uncle(self) -> Optional["Node"]:
        if self.parent is None or self.parent.parent is None:
            return None
        return self.parent.sibling()


@dataclass
class FixupAction:
    """Um passo de correção estrutural — 1 ação de gameplay."""
    kind: str            # "repintar_ninho" | "realocar_galho_simples" | "realocar_galho_dupla"
    node_key: int
    reason: str


class RedBlackForest:
    """
    Árvore Rubro-Negra com fixup exposto passo-a-passo, para que o
    motor de jogo (game_engine.py) possa pedir ao jogador que escolha
    a ação correta em cada violação, em vez de aplicar tudo de forma
    opaca como uma biblioteca de produção faria.
    """

    def __init__(self) -> None:
        self.root: Optional[Node] = None
        self.size: int = 0

    # ------------------------------------------------------------------ #
    # Inserção (fase 1 do core loop: "Um novo filhote de corvo pousa...") #
    # ------------------------------------------------------------------ #
    def insert(self, key: int) -> List[Node]:
        """
        Insere `key` como um novo nó RED via descida BST clássica
        (equivalente à busca de posição do jogo original) e devolve o
        caminho percorrido (raiz -> novo nó), útil para logar a
        travessia comparativa exigida no passo 2 do core loop.
        """
        path: List[Node] = []
        new_node = Node(key=key, color=Color.RED)
        self.size += 1

        if self.root is None:
            self.root = new_node
            new_node.color = Color.BLACK  # raiz é sempre preta (propriedade 2)
            return [new_node]

        cur = self.root
        parent = None
        while cur is not None:
            path.append(cur)
            parent = cur
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                raise ValueError(f"Chave {key} já existe no bosque")

        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        path.append(new_node)
        return path

    def has_violation(self, node: Node) -> bool:
        """Vermelho sob vermelho — a violação central da RN-Tree."""
        return (
            node.color == Color.RED
            and node.parent is not None
            and node.parent.color == Color.RED
        )

    def required_action(self, node: Node) -> FixupAction:
        """
        Determina, SEM aplicar, qual é a ação correta para resolver a
        violação em `node`. É o "gabarito" contra o qual a escolha do
        jogador é validada.
        """
        if not self.has_violation(node):
            raise ValueError("Nó sem violação — nada a corrigir")

        uncle = node.uncle()
        if uncle is not None and uncle.color == Color.RED:
            return FixupAction(
                kind="repintar_ninho",
                node_key=node.key,
                reason="Tio vermelho: repinta pai, tio (pretos) e avô (vermelho).",
            )

        parent = node.parent
        grandparent = parent.parent
        is_left_parent = parent is grandparent.left
        is_left_node = node is parent.left
        # "Triângulo" (zig-zag) exige rotação dupla; "linha" exige rotação simples.
        if is_left_parent == is_left_node:
            kind = "realocar_galho_simples"
            reason = "Tio preto/ausente, formação em linha: 1 rotação + recoloração."
        else:
            kind = "realocar_galho_dupla"
            reason = "Tio preto/ausente, formação em triângulo: 2 rotações + recoloração."
        return FixupAction(kind=kind, node_key=node.key, reason=reason)

    def apply_action(self, node: Node, action: FixupAction) -> Node:
        """
        Aplica a ação de correção e devolve o nó a partir do qual a
        verificação de violação deve continuar subindo na árvore
        (loop do CLRS RB-INSERT-FIXUP).
        """
        uncle = node.uncle()
        parent = node.parent
        grandparent = parent.parent

        if action.kind == "repintar_ninho":
            parent.color = Color.BLACK
            uncle.color = Color.BLACK
            grandparent.color = Color.RED
            return grandparent

        is_left_parent = parent is grandparent.left
        if is_left_parent:
            if action.kind == "realocar_galho_dupla":
                self._rotate_left(parent)
                node, parent = parent, node  # `node` volta a apontar pro nó "pivô"
            parent.color = Color.BLACK
            grandparent.color = Color.RED
            self._rotate_right(grandparent)
        else:
            if action.kind == "realocar_galho_dupla":
                self._rotate_right(parent)
                node, parent = parent, node
            parent.color = Color.BLACK
            grandparent.color = Color.RED
            self._rotate_left(grandparent)

        return node

    def fixup_chain(self, node: Node) -> List[FixupAction]:
        """
        Devolve a sequência COMPLETA de ações corretas necessárias para
        sanar toda a cadeia de violações a partir de `node` — o gabarito
        de referência do "modo automático"/oráculo usado pelos testes e
        pela simulação sem UI.
        """
        actions: List[FixupAction] = []
        cur = node
        while cur is not None and self.has_violation(cur):
            action = self.required_action(cur)
            actions.append(action)
            cur = self.apply_action(cur, action)
        self.root.color = Color.BLACK
        return actions

    # ------------------------------------------------------------------ #
    # Rotações (reaproveitadas do jogo base, ver seção 4.3 do GDD)       #
    # ------------------------------------------------------------------ #
    def _rotate_left(self, x: Node) -> None:
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x: Node) -> None:
        y = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # ------------------------------------------------------------------ #
    # Invariantes / "equilíbrio de sombra" (passo 4 do core loop)        #
    # ------------------------------------------------------------------ #
    def black_heights(self) -> Dict[int, int]:
        """
        Altura preta de cada caminho raiz->NIL (folha virtual), tratando
        os ponteiros nulos como as sentinelas pretas da formalização
        clássica (CLRS) da árvore Rubro-Negra. Cada NIL alcançado vira
        uma entrada no dicionário (chave sintética -> altura preta).
        """
        heights: Dict[int, int] = {}
        counter = [0]

        def walk(node: Optional[Node], bh: int) -> None:
            if node is None:
                heights[counter[0]] = bh + 1  # NIL conta como preto
                counter[0] += 1
                return
            bh_here = bh + (1 if node.color == Color.BLACK else 0)
            walk(node.left, bh_here)
            walk(node.right, bh_here)

        walk(self.root, 0)
        return heights

    def is_shade_balanced(self) -> bool:
        """'Dossel uniforme': todo caminho raiz->folha tem a mesma bh."""
        if self.root is None:
            return True
        values = set(self.black_heights().values())
        return len(values) == 1

    def has_red_red_violation(self) -> bool:
        found = False

        def walk(node: Optional[Node]) -> None:
            nonlocal found
            if node is None:
                return
            if self.has_violation(node):
                found = True
            walk(node.left)
            walk(node.right)

        walk(self.root)
        return found

    def is_valid_red_black_tree(self) -> bool:
        """Checklist das 5 propriedades formais da árvore Rubro-Negra."""
        if self.root is None:
            return True
        if self.root.color != Color.BLACK:
            return False
        if self.has_red_red_violation():
            return False
        return self.is_shade_balanced()

    # ------------------------------------------------------------------ #
    # Condição de derrota — colapso estrutural (seção 4.4 do GDD)        #
    # ------------------------------------------------------------------ #
    def is_degenerate_chain(self) -> bool:
        """
        Detecta o "bosque em colapso": a árvore se degenerou numa fila
        única ao longo do tronco (cada nó tem no máximo 1 filho), o que
        implica busca O(n) em vez de O(log n).
        """
        def walk(node: Optional[Node]) -> bool:
            if node is None:
                return True
            children = (1 if node.left else 0) + (1 if node.right else 0)
            if children > 1:
                return False
            return walk(node.left) and walk(node.right)

        return self.size > 2 and walk(self.root)

    def collapse_to_chain(self) -> None:
        """
        Aplica o efeito visual/estrutural de derrota descrito no GDD:
        "os ninhos se realinham em uma única fileira ao longo do
        tronco" — reconstrói a árvore como uma corrente (linked list)
        preservando a ordem das chaves.
        """
        keys = sorted(self._inorder_keys())
        self.root = None
        self.size = 0
        cur = None
        for k in keys:
            node = Node(key=k, color=Color.BLACK)
            self.size += 1
            if self.root is None:
                self.root = node
            else:
                cur.right = node
                node.parent = cur
            cur = node

    def _inorder_keys(self, node: Optional[Node] = None, _first: bool = True) -> List[int]:
        if _first:
            node = self.root
        if node is None:
            return []
        return self._inorder_keys(node.left, False) + [node.key] + self._inorder_keys(node.right, False)

    def height(self) -> int:
        def walk(node: Optional[Node]) -> int:
            if node is None:
                return 0
            return 1 + max(walk(node.left), walk(node.right))
        return walk(self.root)
