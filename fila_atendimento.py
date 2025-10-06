import sys

class PatientNode:
    def __init__(self, name: str, age: int, priority: int):
        self.name = name
        self.age = int(age)
        self.priority = int(priority)
        self.prev = None
        self.next = None

    def __repr__(self):
        tag = "(P)" if self.priority == 2 else "(N)"
        return f"[ {self.name} {tag} ]"


class PatientQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.next_should_be_normal = False

    def _sum_memory(self) -> int:
        """Percorre os nós e soma sys.getsizeof dos objetos relevantes (estimativa)."""
        total = 0
        cur = self.head
        while cur:
            total += sys.getsizeof(cur)
            total += sys.getsizeof(cur.name)
            total += sys.getsizeof(cur.age)
            total += sys.getsizeof(cur.priority)
            cur = cur.next
        total += sys.getsizeof(self)
        return total

    def _count_priorities_and_normals(self):
        p = n = 0
        cur = self.head
        while cur:
            if cur.priority == 2:
                p += 1
            else:
                n += 1
            cur = cur.next
        return p, n

    def _print_memory_change(self, before: int, after: int, label: str):
        diff = after - before
        print(f"\n[{label}] Memória antes: {before} bytes | depois: {after} bytes | diferença: {diff} bytes\n")

    def _insert_before(self, node: PatientNode, ref: PatientNode):
        """Insere node antes de ref (ambos não None)."""
        node.next = ref
        node.prev = ref.prev
        if ref.prev:
            ref.prev.next = node
        else:
            self.head = node
        ref.prev = node
        self.size += 1

    def _append_tail(self, node: PatientNode):
        if not self.head:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def _remove_node(self, node: PatientNode) -> PatientNode:
        """Remove um nó dado da lista e retorna ele (desconectado)."""
        if not node:
            return None
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None
        self.size -= 1
        return node

    def _find_first_with_priority(self, priority: int):
        cur = self.head
        while cur:
            if cur.priority == priority:
                return cur
            cur = cur.next
        return None

    def add_patient(self, name: str, age: int, priority_input):
        # aceita 'P'/'N' ou 1/2
        if isinstance(priority_input, str):
            p = 2 if priority_input.strip().upper().startswith("P") else 1
        else:
            p = int(priority_input)
        new_node = PatientNode(name, age, p)

        mem_before = self._sum_memory()

        if new_node.priority == 2:
            cur = self.head
            while cur and cur.priority == 2:
                cur = cur.next
            if cur: 
                self._insert_before(new_node, cur)
            else:
                self._append_tail(new_node)
        else:
            self._append_tail(new_node)

        mem_after = self._sum_memory()
        self._print_memory_change(mem_before, mem_after, f"ADD {name}")

    def remove_patient(self):
        """Remove paciente atendido conforme regras, informando o próximo."""
        mem_before = self._sum_memory()

        p_count, n_count = self._count_priorities_and_normals()
        alternation_active = False
        if n_count > 0 and (7 * p_count) >= n_count:
            alternation_active = True

        removed_node = None
        if alternation_active and self.next_should_be_normal:
            first_normal = self._find_first_with_priority(1)
            if first_normal:
                removed_node = self._remove_node(first_normal)
            else:
                removed_node = self._remove_node(self.head)
        else:
            removed_node = self._remove_node(self.head)
        if alternation_active:
            self.next_should_be_normal = not self.next_should_be_normal
        else:
            self.next_should_be_normal = False

        mem_after = self._sum_memory()
        self._print_memory_change(mem_before, mem_after, f"REMOVE {removed_node.name if removed_node else 'N/A'}")
        
        next_patient = self.head
        if next_patient:
            print(f"Paciente atendido: {removed_node.name}. Próximo: {next_patient.name} {'(P)' if next_patient.priority == 2 else '(N)'}")
        else:
            print(f"Paciente atendido: {removed_node.name}. Fila vazia.")
        return removed_node

    def edit_patient(self, search_name: str, new_name: str = None, new_age: int = None, new_priority_input = None):
        """Edita os dados do primeiro paciente com name == search_name."""
        mem_before = self._sum_memory()

        cur = self.head
        while cur and cur.name != search_name:
            cur = cur.next
        if not cur:
            print(f"Paciente '{search_name}' não encontrado.")
            return None

        if new_name:
            cur.name = new_name
        if new_age is not None:
            cur.age = int(new_age)
        if new_priority_input is not None:
            if isinstance(new_priority_input, str):
                new_p = 2 if new_priority_input.strip().upper().startswith("P") else 1
            else:
                new_p = int(new_priority_input)
            if new_p != cur.priority:
                node = self._remove_node(cur)
                node.priority = new_p
                if node.priority == 2:
                    ref = self._find_first_with_priority(1)
                    if ref:
                        self._insert_before(node, ref)
                    else:
                        self._append_tail(node)
                else:
                    self._append_tail(node)

        mem_after = self._sum_memory()
        self._print_memory_change(mem_before, mem_after, f"EDIT {search_name}")
        print(f"Paciente '{search_name}' alterado com sucesso.")
        return cur

    def display(self):
        parts = []
        cur = self.head
        while cur:
            tag = "(P)" if cur.priority == 2 else "(N)"
            parts.append(f"[ {cur.name} {tag} ]")
            cur = cur.next
            if cur:
                parts.append("-->")
        line = " ".join(parts) if parts else "<fila vazia>"
        print(line)

    def display_reverse(self):
        parts = []
        cur = self.tail
        while cur:
            tag = "(P)" if cur.priority == 2 else "(N)"
            parts.append(f"[ {cur.name} {tag} ]")
            cur = cur.prev
            if cur:
                parts.append("-->")
        line = " ".join(parts) if parts else "<fila vazia>"
        print(line)

    def fill_with_sample(self):
        """Inclui automaticamente 10 pacientes alternados entre normais e prioritários."""
        sample = [
            ("Joao", 30, "N"),
            ("Maria", 28, "P"),
            ("Carlos", 40, "N"),
            ("Ana", 35, "P"),
            ("Paulo", 22, "N"),
            ("Lucia", 50, "P"),
            ("Rafael", 19, "N"),
            ("Sofia", 60, "P"),
            ("Bruno", 45, "N"),
            ("Mariana", 33, "P"),
        ]
        for name, age, pr in sample:
            self.add_patient(name, age, pr)

    def interactive_mode(self):
        print("Modo interativo (comandos: add Nome Idade P/N | assist | edit Nome NovoNome NovaIdade P/N | show | showrev | exit )")
        while True:
            try:
                cmd = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nSaindo do modo interativo.")
                break
            if not cmd:
                continue
            parts = cmd.split()
            op = parts[0].lower()
            if op == "add" and len(parts) >= 4:
                name = parts[1]
                age = parts[2]
                pr = parts[3]
                self.add_patient(name, age, pr)
            elif op == "assist":
                self.remove_patient()
            elif op == "edit" and len(parts) >= 5:
                old = parts[1]
                newname = parts[2]
                newage = parts[3]
                newpr = parts[4]
                self.edit_patient(old, newname, newage, newpr)
            elif op == "show":
                self.display()
            elif op == "showrev":
                self.display_reverse()
            elif op == "exit":
                print("Encerrando modo interativo.")
                break
            else:
                print("Comando inválido. Exemplos: add Joao 35 P | assist | edit Maria MariaNova 40 N | show | showrev | exit")

# ----------------- exemplo de uso -----------------
if __name__ == "__main__":
    fila = PatientQueue()
    fila.fill_with_sample()
    print("Fila inicial (10 pacientes alternados):")
    fila.display()
    print("\n-- Remover (assist) 1 --")
    fila.remove_patient()
    print("\n-- Adicionar novo prioritário 'Diego' --")
    fila.add_patient("Diego", 29, "P")
    print("\n-- Editar 'Carlos' para prioridade P --")
    fila.edit_patient("Carlos", new_priority_input="P")
    print("\nFila final:")
    fila.display()