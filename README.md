Projeto 01 – Fila de Espera (Estrutura de Dados)
Descrição

Este projeto implementa um sistema de fila de espera para atendimento de pacientes, simulando a dinâmica de um hospital ou posto de saúde.
A estrutura de dados utilizada é uma lista duplamente encadeada, construída manualmente em Python, sem uso de listas prontas.

O programa permite:

Cadastrar pacientes normais (N) e prioritários (P).

Manter a ordem de prioridade durante a inserção.

Editar informações de pacientes.

Remover (atender) pacientes respeitando regras de alternância entre normais e prioritários.

Exibir a fila em ASCII, inclusive de forma invertida.

Monitorar o consumo de memória em bytes a cada operação.

Iniciar automaticamente com 10 pacientes (5 normais e 5 prioritários, alternados).

 Estrutura e Regras de Negócio

Lista Duplamente Encadeada
Cada paciente é um nó (PatientNode) com ponteiros prev e next.

Ordem de Inserção

Pacientes prioritários (P) são inseridos antes do primeiro paciente normal existente.

Pacientes normais (N) são adicionados ao final da fila.

Atendimento (Remoção)

O sistema alterna entre pacientes prioritários e normais quando a proporção de pacientes prioritários for igual ou superior a 1 para cada 7 normais (7 * prioritários >= normais).

Fora dessa condição, o atendimento segue a ordem normal da fila.


🧩 Funcionalidades Principais
Função	Descrição
add_patient(nome, idade, prioridade)	Adiciona paciente respeitando a ordem e prioridade
remove_patient()	Remove o próximo paciente conforme as regras
edit_patient(nome_antigo, novo_nome, nova_idade, nova_prioridade)	Edita dados e reposiciona paciente se necessário
display()	Mostra a fila em formato ASCII
display_reverse()	Mostra a fila invertida
fill_with_sample()	Gera 10 pacientes automaticamente
interactive_mode()	Abre modo interativo no terminal
💻 Como Executar

🧠 Estrutura de Dados Implementada
PatientNode
 ├── name: str
 ├── age: int
 ├── priority: int  (1 = Normal, 2 = Prioritário)
 ├── prev: PatientNode
 └── next: PatientNode

PatientQueue
 ├── head: PatientNode
 ├── tail: PatientNode
 ├── add_patient()
 ├── remove_patient()
 ├── edit_patient()
 ├── display()
 ├── display_reverse()
 └── fill_with_sample()


Integrantes do Grupo

Nome 1: Maria Clara Souza Cruz 

Nome 2:Maria Gabriela G Barbosa

Nome 3: Thays Gomes 


Este projeto é de uso exclusivamente acadêmico e foi desenvolvido como atividade prática da disciplina Estrutura de Dados (Centro Universitário de Brasília – CEUB).
