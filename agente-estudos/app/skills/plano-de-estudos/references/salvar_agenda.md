# Salvar a Agenda em Arquivo (GCSToolset)

O agente salva a agenda num arquivo CSV em um bucket do **Google Cloud Storage** usando as ferramentas do **GCSToolset** do ADK ([adk.dev/integrations/gcs](https://adk.dev/integrations/gcs/)). A pessoa pode baixar o arquivo ou importar a partir do bucket no Google Agenda.

---

## Ferramentas disponíveis

| Ferramenta | Para que serve | Argumentos |
|---|---|---|
| `create_object` | Cria o objeto ou **sobrescreve** o objeto inteiro no bucket | `bucket_name` (texto), `object_name` (texto), `data` (texto) |
| `get_object_data` | Lê o objeto do bucket e devolve o conteúdo em texto puro no campo `results` | `bucket_name` (texto), `object_name` (texto) |

Use **só** essas duas. Não tente listar objetos ou chamar outras ferramentas. O CSV é sempre gravado inteiro, de uma vez.

## Regras de bucket e objeto

* O nome do bucket é informado na instrução inicial do agente (ex: `'agente-estudos-planos'`). Use exatamente o `bucket_name` informado.
* Use sempre o nome de objeto `object_name: "plano-de-estudos.csv"`.
* Use sempre o mesmo nome de objeto. No replanejamento, a versão nova sobrescreve a anterior.

## Como gravar a agenda

1. Monte o CSV completo seguindo as regras de `assets/plano_template.md`.
2. Antes de chamar a ferramenta, confira o checklist:
   - [ ] A primeira linha é exatamente `Subject,Start Date,Start Time,End Date,End Time,Description`.
   - [ ] Há uma linha por sessão, sem linhas em branco, e nenhuma sessão cai em dia que a pessoa não informou.
   - [ ] Datas em `MM/DD/YYYY` e horários em `HH:MM AM/PM`.
   - [ ] Toda `Description` está entre aspas duplas.
   - [ ] O conteúdo **não** tem a cerca ```` ```csv ```` nem texto explicativo, só o CSV.
3. Chame `create_object` com `bucket_name` igual ao bucket informado, `object_name` igual a `plano-de-estudos.csv` e `data` igual ao CSV, terminando com uma quebra de linha.

Exemplo de chamada:

```json
{
  "bucket_name": "agente-estudos-planos",
  "object_name": "plano-de-estudos.csv",
  "data": "Subject,Start Date,Start Time,End Date,End Time,Description\n📚 Python: variáveis e entrada/saída,11/02/2026,08:00 PM,11/02/2026,09:00 PM,\"Revisão: — | Técnica: Aprender fazendo | Entregável: script de nome e idade\"\n"
}
```

## Como interpretar a resposta

| Resposta da ferramenta | O que fazer |
|---|---|
| `{"status": "SUCCESS", "results": "Object plano-de-estudos.csv created successfully in bucket ..."}` | Sucesso. Informe na seção 5 do template a URI `gs://<bucket>/plano-de-estudos.csv` e o número de sessões. |
| Erro de permissão ou bucket inexistente | Não insista. Diga em uma frase que não foi possível salvar o arquivo no bucket e mostre o CSV num bloco ```` ```csv ```` na seção 5. |
| Qualquer outro erro | Não insista. Diga em uma frase que não foi possível salvar o arquivo e mostre o CSV num bloco ```` ```csv ```` na seção 5. |

Nunca diga que salvou o arquivo sem ter recebido status de sucesso.

## Replanejamento

1. Se precisar lembrar do plano atual, chame `get_object_data` com `bucket_name` igual ao bucket informado e `object_name` igual a `plano-de-estudos.csv`.
2. A resposta contém o texto CSV puro no campo `results`.
3. Se a resposta for erro ou objeto não encontrado, monte o CSV a partir da tabela de sessões da conversa.
4. Monte o CSV novo **inteiro**, já com os ajustes, e grave com `create_object` no mesmo bucket e objeto. A versão anterior é sobrescrita.
5. Na resposta, diga o que mudou e confirme que o arquivo foi atualizado.
