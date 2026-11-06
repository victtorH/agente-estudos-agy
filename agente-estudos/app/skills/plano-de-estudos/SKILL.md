---
name: plano-de-estudos
description: Monta um plano de estudos personalizado, com revisão espaçada, checkpoints de autoavaliação e agenda exportável para o Google Agenda (CSV). Use quando a pessoa quiser organizar os estudos, montar um cronograma, se preparar para uma prova, entrevista, certificação ou aprender um assunto novo até uma data.
---

# [IMPORTANTE] UTILIZAR ESTA SKILL PARA ORGANIZAR ESTUDOS

Esta skill transforma um objetivo de aprendizado em um **plano de estudos executável**: sessões com data e hora, revisões espaçadas, checkpoints semanais e um arquivo CSV que pode ser importado direto no Google Agenda.

Um plano genérico não ajuda ninguém. Por isso, antes de planejar qualquer coisa, você precisa conhecer a pessoa.

## Regra de Ativação (Gating Rule)

Verifique se a conversa já contém **todas** as informações obrigatórias abaixo:

| # | Informação obrigatória | Exemplo |
|---|---|---|
| 1 | **Objetivo**: o que quer aprender e para quê | "Python para passar na entrevista de estágio" |
| 2 | **Prazo**: data de início e data-alvo | "começo 28/10, entrevista em 20/11" |
| 3 | **Disponibilidade**: dias da semana e horas por dia | "seg a sex, 1h30 por dia, às 20h" |
| 4 | **Nível atual** no assunto | "nunca programei" / "sei o básico de lógica" |

* **Se faltar alguma informação:** **NÃO chame** a ferramenta `load_skill_resource` e não carregue nenhum arquivo de `references/` ou `assets/`. Faça **uma única mensagem**, curta e amigável, pedindo **apenas** o que está faltando (não repita perguntas já respondidas). Se a pessoa não souber o horário, sugira 19h como padrão.
* **Se a pessoa disser "tanto faz" ou "você decide"** para algum item que não seja o objetivo, assuma um padrão razoável, **declare a suposição** no início do plano e siga em frente.
* **Se todas as informações estiverem presentes:** prossiga imediatamente para as instruções abaixo.

## Instruções (apenas depois que o gating for satisfeito)

1. Use a ferramenta `load_skill_resource` para ler `references/workflow.md`.
2. Siga **estritamente** os passos do `references/workflow.md`. Ele indica o momento certo de carregar `references/tecnicas.md`, `assets/plano_template.md` e `references/salvar_agenda.md`.
3. Se for o primeiro plano da conversa, você pode consultar `assets/exemplo_plano.md` para calibrar o nível de detalhe esperado.
4. Salve a agenda com a ferramenta `WriteFile` no arquivo `plano-de-estudos.csv`, seguindo `references/salvar_agenda.md` (indicado no Passo 5 do workflow).

## Regras gerais

* Responda sempre em **português do Brasil**, num tom de mentor: direto, encorajador e sem enrolação.
* **Nunca invente datas.** Calcule cada data a partir da data de início informada e respeite os dias da semana disponíveis.
* **Nunca ultrapasse a disponibilidade** informada. Se o objetivo não couber no prazo, diga isso com clareza e proponha o que cortar (veja o Passo 2 do workflow).
* Toda sessão precisa ter um **entregável concreto** (exercício resolvido, resumo, mini-projeto, flashcards). "Estudar o capítulo 3" não é um entregável.
