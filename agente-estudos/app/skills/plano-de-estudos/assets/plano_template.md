# Template de Saída: Plano de Estudos

Preencha o template abaixo substituindo tudo que estiver entre `[colchetes]`. Mantenha os títulos e a ordem das seções.

---

````markdown
## 🎯 Plano de Estudos: [Objetivo resumido]

**Perfil:** [nível atual] · **Período:** [DD/MM/AAAA] a [DD/MM/AAAA] · **Disponibilidade:** [dias da semana], [X]h por dia às [HH:MM]
**Capacidade:** [N] dias de estudo · [H] horas líquidas · [M] dia(s) de margem para imprevistos

> **Suposições:** [liste as suposições feitas no gating, ou escreva "Nenhuma"]

### 1. Visão Geral dos Módulos

| # | Módulo | Horas | Prioridade |
|---|---|---|---|
| 1 | [nome] | [h] | Essencial |
| ... | ... | ... | Essencial / Opcional |

### 2. Cronograma de Sessões

#### Semana 1: [tema da semana]

| Data | Dia | Revisão (início) | Conteúdo novo | Técnica | Entregável |
|---|---|---|---|---|---|
| [DD/MM] | [seg] | [conteúdos D+1/D+3/D+7 ou "—"] | [tópico] | [técnica] | [entregável concreto] |

**✅ Checkpoint da Semana 1 ([DD/MM])**
1. [pergunta de autoavaliação específica]
2. [...]
3. [...]
- **Critério de "dominei":** [o que precisa conseguir fazer sem consulta]
- **Se não passar:** [tópico a revisar] → encaixar em [DD/MM]

[repita para cada semana]

### 3. O que ficou de fora

[Módulos marcados como Opcional e o motivo, ou "Nada. O objetivo cabe no prazo."]

### 4. Como importar no Google Agenda

1. Baixe o arquivo `plano-de-estudos.csv` (seção 5) para o seu computador.
2. No Google Agenda (computador): **Configurações ⚙️ → Importar e exportar → Importar**.
3. Selecione o arquivo, escolha a agenda de destino e clique em **Importar**.

> Dica: crie uma agenda separada chamada "Estudos". Se quiser refazer o plano, basta excluir essa agenda.

### 5. Agenda (CSV)

📁 Salvei a agenda em `[caminho retornado pelo WriteFile]`, com [N] sessões.

---
**Próximos passos:** posso ajustar o plano se sua rotina mudar, se você atrasar alguma sessão ou se quiser mais detalhes em algum módulo.
````

> Se a ferramenta `WriteFile` não estiver disponível, troque a linha 📁 da seção 5 por um bloco ```` ```csv ```` com o CSV completo.

---

## Regras obrigatórias do CSV

O conteúdo gravado com `WriteFile` em `plano-de-estudos.csv` deve ser **só o CSV** (sem a cerca ```` ```csv ````). O Google Agenda só aceita o arquivo se estas regras forem seguidas **exatamente**:

1. **Cabeçalho** idêntico ao do template, em inglês: `Subject,Start Date,Start Time,End Date,End Time,Description`.
2. **Uma linha por sessão de estudo.** Checkpoints entram como parte da sessão do dia, não como linha separada.
3. **Datas no formato americano `MM/DD/YYYY`** (ex.: 28 de outubro de 2026 → `10/28/2026`). Isso vale **só para o CSV**. No restante do plano, use `DD/MM`.
4. **Horários no formato `HH:MM AM/PM`** (ex.: 20h → `08:00 PM`; 19h30 → `07:30 PM`).
5. **End Time** = Start Time + duração da sessão.
6. **Subject** começa com um emoji e o módulo: `📚 Python: listas e dicionários`. Simulações usam `🎯`, dias de margem usam `🛟 Margem` e, em dias de checkpoint, acrescente ` + ✅ Checkpoint` ao final.
7. **Description** sempre entre aspas duplas, com revisão, técnica e entregável separados por ` | `. Ex.: `"Revisão: variáveis (D+1) | Técnica: Recuperação ativa | Entregável: 10 exercícios resolvidos"`.
8. **Não use vírgulas** fora das aspas, nem linhas em branco no meio do arquivo.
