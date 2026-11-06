# Salvar a Agenda em Arquivo (EnvironmentToolset)

O agente salva a agenda num arquivo CSV usando as ferramentas de arquivo do **EnvironmentToolset** do ADK ([adk.dev/integrations/environment-toolset](https://adk.dev/integrations/environment-toolset/)). As ferramentas trabalham dentro de uma pasta do ambiente (o `working_dir`), e a pessoa importa o arquivo gerado no Google Agenda.

---

## Ferramentas disponíveis

| Ferramenta | Para que serve | Argumentos |
|---|---|---|
| `WriteFile` | Cria o arquivo ou **sobrescreve** o arquivo inteiro | `path` (texto), `content` (texto) |
| `ReadFile` | Lê um arquivo e devolve o conteúdo com o número de cada linha | `path` (texto), `start_line` e `end_line` (opcionais) |

Use **só** essas duas. Não tente executar comandos (`Execute`) nem editar trechos (`EditFile`): o CSV é sempre gravado inteiro, de uma vez.

## Regras de caminho

* Use sempre o caminho **relativo** `plano-de-estudos.csv`. Ele é resolvido dentro da pasta do ambiente.
* **Não** use caminho absoluto (`/home/...`) nem `../`. O ambiente recusa esses caminhos com o erro `Path escapes working directory`.
* Use sempre o mesmo nome de arquivo. No replanejamento, a versão nova substitui a anterior.

## Como gravar a agenda

1. Monte o CSV completo seguindo as regras de `assets/plano_template.md`.
2. Antes de chamar a ferramenta, confira o checklist:
   - [ ] A primeira linha é exatamente `Subject,Start Date,Start Time,End Date,End Time,Description`.
   - [ ] Há uma linha por sessão, sem linhas em branco, e nenhuma sessão cai em dia que a pessoa não informou.
   - [ ] Datas em `MM/DD/YYYY` e horários em `HH:MM AM/PM`.
   - [ ] Toda `Description` está entre aspas duplas.
   - [ ] O conteúdo **não** tem a cerca ```` ```csv ```` nem texto explicativo, só o CSV.
3. Chame `WriteFile` com `path` igual a `plano-de-estudos.csv` e `content` igual ao CSV, terminando com uma quebra de linha.

Exemplo de chamada:

```json
{
  "path": "plano-de-estudos.csv",
  "content": "Subject,Start Date,Start Time,End Date,End Time,Description\n📚 Python: variáveis e entrada/saída,11/02/2026,08:00 PM,11/02/2026,09:00 PM,\"Revisão: — | Técnica: Aprender fazendo | Entregável: script de nome e idade\"\n"
}
```

## Como interpretar a resposta

| Resposta da ferramenta | O que fazer |
|---|---|
| `{"status": "ok", "message": "Wrote plano-de-estudos.csv"}` | Sucesso. Informe na seção 5 do template o caminho e o número de sessões. |
| `{"status": "error", "error": "Path escapes working directory: ..."}` | O caminho estava errado. Tente de novo **uma vez** com `plano-de-estudos.csv`. |
| Qualquer outro erro | Não insista. Diga em uma frase que não foi possível salvar o arquivo e mostre o CSV num bloco ```` ```csv ```` na seção 5. |

Nunca diga que salvou o arquivo sem ter recebido `"status": "ok"`.

## Replanejamento

1. Se precisar lembrar do plano atual, chame `ReadFile` com `path` igual a `plano-de-estudos.csv`.
2. A resposta vem com o número de cada linha na frente (ex.: `     1\tSubject,Start Date,...`). Esses números **não** fazem parte do arquivo: remova-os antes de reaproveitar qualquer linha.
3. Se a resposta for `File not found`, monte o CSV a partir da tabela de sessões da conversa.
4. Monte o CSV novo **inteiro**, já com os ajustes, e grave com `WriteFile` no mesmo caminho. A versão anterior é substituída.
5. Na resposta, diga o que mudou e confirme que o arquivo foi atualizado.
