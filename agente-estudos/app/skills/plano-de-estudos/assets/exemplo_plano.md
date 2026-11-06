# Exemplo de Plano Preenchido

Use este exemplo apenas para **calibrar o nível de detalhe e o formato**. Não copie o conteúdo: cada plano deve ser feito para o objetivo, o prazo e o nível da pessoa.

**Entrada da pessoa:**
> "Quero aprender Python do zero para uma entrevista de estágio no dia 14/11/2026. Posso estudar de segunda a sexta, 1h por dia, às 20h. Começo segunda, 02/11/2026."

---

## 🎯 Plano de Estudos: Python do zero para entrevista de estágio

**Perfil:** iniciante · **Período:** 02/11/2026 a 13/11/2026 · **Disponibilidade:** seg a sex, 1h por dia às 20:00
**Capacidade:** 10 dias de estudo · 9 horas líquidas · 1 dia de margem para imprevistos

> **Suposições:** Nenhuma

### 1. Visão Geral dos Módulos

| # | Módulo | Horas | Prioridade |
|---|---|---|---|
| 1 | Variáveis, tipos, entrada e saída | 1 | Essencial |
| 2 | Operadores e condicionais | 1 | Essencial |
| 3 | Laços (`for` e `while`) | 1 | Essencial |
| 4 | Listas e dicionários | 2 | Essencial |
| 5 | Funções | 2 | Essencial |
| 6 | Mini-projeto + simulação de entrevista | 2 | Essencial |

### 2. Cronograma de Sessões

#### Semana 1: Fundamentos

| Data | Dia | Revisão (início) | Conteúdo novo | Técnica | Entregável |
|---|---|---|---|---|---|
| 02/11 | seg | — | Variáveis, tipos, `input`/`print` | Aprender fazendo | Script que pede nome e idade e calcula o ano de nascimento |
| 03/11 | ter | Variáveis (D+1) | Operadores e `if`/`elif`/`else` | Recuperação ativa | 5 exercícios: par/ímpar, maior de 3 números, faixa etária… |
| 04/11 | qua | Condicionais (D+1) | Laços `for` e `while` | Feynman | Tabuada com `for` + jogo de adivinhação com `while` |
| 05/11 | qui | Variáveis (D+3), Laços (D+1) | Listas | Aprender fazendo | Lista de compras: adicionar, remover e ordenar itens |
| 06/11 | sex | Condicionais (D+3), Listas (D+1) | Dicionários | Aprender fazendo | Agenda de contatos usando `dict` |

**✅ Checkpoint da Semana 1 (06/11)**
1. Qual a diferença entre `=` e `==`? Dê um exemplo de cada.
2. Quando faz mais sentido usar `while` em vez de `for`?
3. Como acessar o último item de uma lista sem saber o tamanho dela?
4. O que acontece se você acessar uma chave que não existe em um dicionário? Como evitar o erro?
- **Critério de "dominei":** escrever, sem consulta, um programa que lê 5 números e mostra o maior, o menor e a média.
- **Se não passar:** revisar laços e listas → encaixar em 09/11, antes de funções.

#### Semana 2: Funções e preparação para a entrevista

| Data | Dia | Revisão (início) | Conteúdo novo | Técnica | Entregável |
|---|---|---|---|---|---|
| 09/11 | seg | Variáveis (D+7), Laços e Listas (D+3) | Funções: `def`, parâmetros e `return` | Aprender fazendo | Lista de compras refatorada em funções |
| 10/11 | ter | Condicionais (D+7), Dicionários (D+3), Funções (D+1) | Funções com listas e dicionários | Prática intercalada | 6 exercícios mistos no estilo de entrevista |
| 11/11 | qua | Laços (D+7), Funções (D+1) | Mini-projeto integrador | Aprender fazendo | Gerenciador de tarefas no terminal publicado no GitHub |
| 12/11 | qui | Listas (D+7), Funções (D+3) | 🎯 Simulação de entrevista técnica | Simulação | 2 problemas resolvidos em 40 min + lista de erros |
| 13/11 | sex | Erros da simulação | 🛟 Margem: recuperar atrasos ou fazer um simulado extra | Recuperação ativa | Simulado extra ou sessões pendentes concluídas |

**✅ Checkpoint da Semana 2 (13/11)**
1. Qual a diferença entre `print` e `return` dentro de uma função?
2. Escreva de memória uma função que recebe uma lista e devolve só os números pares.
3. Como você explicaria o seu mini-projeto em 1 minuto para o entrevistador?
- **Critério de "dominei":** resolver um problema novo de nível fácil em até 20 minutos, explicando o raciocínio em voz alta.
- **Se não passar:** refazer os exercícios errados da simulação na própria sessão de 13/11.

### 3. O que ficou de fora

Nada. O objetivo cabe no prazo. Se sobrar fôlego depois da entrevista, o próximo passo natural é estudar orientação a objetos.

### 4. Como importar no Google Agenda

1. Baixe o arquivo `plano-de-estudos.csv` (seção 5) para o seu computador.
2. No Google Agenda (computador): **Configurações ⚙️ → Importar e exportar → Importar**.
3. Selecione o arquivo, escolha a agenda de destino e clique em **Importar**.

> Dica: crie uma agenda separada chamada "Estudos". Se quiser refazer o plano, basta excluir essa agenda.

### 5. Agenda (CSV)

📁 Salvei a agenda em `plano-de-estudos.csv`, com 10 sessões.

---
**Próximos passos:** posso ajustar o plano se sua rotina mudar, se você atrasar alguma sessão ou se quiser mais detalhes em algum módulo.

---

**Conteúdo gravado com `WriteFile` em `plano-de-estudos.csv`** (não aparece na resposta):

```csv
Subject,Start Date,Start Time,End Date,End Time,Description
📚 Python: variáveis e entrada/saída,11/02/2026,08:00 PM,11/02/2026,09:00 PM,"Revisão: — | Técnica: Aprender fazendo | Entregável: script de nome e idade"
📚 Python: operadores e condicionais,11/03/2026,08:00 PM,11/03/2026,09:00 PM,"Revisão: variáveis (D+1) | Técnica: Recuperação ativa | Entregável: 5 exercícios de if"
📚 Python: laços for e while,11/04/2026,08:00 PM,11/04/2026,09:00 PM,"Revisão: condicionais (D+1) | Técnica: Feynman | Entregável: tabuada + jogo de adivinhação"
📚 Python: listas,11/05/2026,08:00 PM,11/05/2026,09:00 PM,"Revisão: variáveis (D+3) e laços (D+1) | Técnica: Aprender fazendo | Entregável: lista de compras"
📚 Python: dicionários + ✅ Checkpoint,11/06/2026,08:00 PM,11/06/2026,09:00 PM,"Revisão: condicionais (D+3) e listas (D+1) | Técnica: Aprender fazendo | Entregável: agenda de contatos + checkpoint da semana 1"
📚 Python: funções,11/09/2026,08:00 PM,11/09/2026,09:00 PM,"Revisão: variáveis (D+7) e laços e listas (D+3) | Técnica: Aprender fazendo | Entregável: lista de compras em funções"
📚 Python: funções com listas e dicionários,11/10/2026,08:00 PM,11/10/2026,09:00 PM,"Revisão: condicionais (D+7) e dicionários (D+3) e funções (D+1) | Técnica: Prática intercalada | Entregável: 6 exercícios mistos"
📚 Python: mini-projeto integrador,11/11/2026,08:00 PM,11/11/2026,09:00 PM,"Revisão: laços (D+7) e funções (D+1) | Técnica: Aprender fazendo | Entregável: gerenciador de tarefas no GitHub"
🎯 Python: simulação de entrevista,11/12/2026,08:00 PM,11/12/2026,09:00 PM,"Revisão: listas (D+7) e funções (D+3) | Técnica: Simulação | Entregável: 2 problemas em 40 min + lista de erros"
🛟 Margem + ✅ Checkpoint,11/13/2026,08:00 PM,11/13/2026,09:00 PM,"Revisão: erros da simulação | Técnica: Recuperação ativa | Entregável: simulado extra ou pendências + checkpoint da semana 2"
```
