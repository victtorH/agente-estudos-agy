# 🧠 Agente de Estudos com Antigravity CLI + Google ADK

Neste lab você vai usar o **Antigravity CLI (`agy`)** para criar, com o **Google ADK**, um agente especialista em estudos. O agente usa a skill [`plano-de-estudos`](skills/plano-de-estudos/SKILL.md): você diz o que quer aprender e até quando, e ele monta um plano de estudos e salva um arquivo CSV para importar no Google Agenda, usando o [EnvironmentToolset](https://adk.dev/integrations/environment-toolset/) do ADK.

## Pré-requisitos

- Conta Google com um projeto do Google Cloud com faturamento ativo (os créditos do [free trial](https://cloud.google.com/free) servem)
- Chave de API do Google AI Studio, criada em [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Conta no GitHub

---

# 1. Introdução ao Antigravity CLI

## 1. Preparar o Cloud Shell

Abra o [Console do Google Cloud](https://console.cloud.google.com/), selecione o seu projeto e clique em **Ativar o Cloud Shell** (ícone `>_`). Depois rode:

```bash
export PROJECT_ID=$(gcloud config get-value project)
echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> ~/.bashrc

# Habilita a Agent Platform (acesso aos modelos usados pelo agy)
gcloud services enable aiplatform.googleapis.com cloudaicompanion.googleapis.com

git clone https://github.com/estevamvicttor/agente-estudos-agy.git ~/agente-estudos-agy
cd ~/agente-estudos-agy
```

> Se o Cloud Shell não abrir no projeto certo, rode `gcloud config set project SEU_PROJECT_ID` antes.

## 2. Instalar e configurar o `agy`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -fsSL https://antigravity.google/cli/install.sh | bash
source ~/.bashrc
```

Para iniciar o Antigravity CLI, utilize o comando:

```bash
agy
```

No setup do `agy`, escolha:

1. `Use a Google Cloud project` → `Continue with Google Cloud`
2. Abra o link, autorize com a sua conta e cole o código no terminal
3. Cole o ID do projeto (`echo $PROJECT_ID`)
4. Location: `global` · License: `Agent Platform`
5. Aceite os termos e confirme `Yes, I trust this folder`

> Dica: no Cloud Shell, use `CTRL+SHIFT+V` para colar. O `CTRL+C` encerra o programa.

## 3. Primeiros passos no `agy`

Teste alguns comandos e prompts:

```text
/help
```

```text
Leia skills/plano-de-estudos/SKILL.md e me explique o que essa skill faz.
```

Saia com `/exit`.

## 4. Instalar o agents-cli

```bash
uvx google-agents-cli setup
agy
```

No `agy`:

1. Rode `/skills` e confira se aparecem as skills `google-agents-cli-*`.
2. Rode `/config` e mude **Tool Permission** para `always-proceed`.

## 5. Criar o agente com `/grill-me`

```text
/grill-me
```

O `agy` vai te entrevistar sobre o agente. Use estas respostas como base:

- **Objetivo:** um mentor de estudos que monta planos personalizados, com revisão espaçada e uma agenda em CSV para o Google Agenda.
- **Skills:** usar ADK Skills ([adk.dev/skills](https://adk.dev/skills/)) com a skill `skills/plano-de-estudos`.
- **Comportamento:** se faltar objetivo, prazo, disponibilidade ou nível, o agente pergunta antes de montar o plano.
- **Arquivos:** o agente salva a agenda em `plano-de-estudos.csv` usando o [EnvironmentToolset](https://adk.dev/integrations/environment-toolset/), sem acesso ao shell.
- **Execução:** local, no ADK Web, com API Key do Google AI Studio. Sem deploy.

Depois peça a criação do projeto:

```text
Crie um agente ADK chamado agente-estudos seguindo as convenções do agents-cli e a especificação de ADK Skills. Copie a skill skills/plano-de-estudos para agente-estudos/app/skills/ e carregue-a com SkillToolset. Adicione o EnvironmentToolset com um LocalEnvironment na pasta agente-estudos/planos/, expondo só as ferramentas ReadFile e WriteFile, para o agente salvar o CSV. O modelo vem da variável MODEL e a instrução do agente deve incluir a data de hoje. Sem configuração de deploy.
```

Saia com `/exit`.

---

# 2. Engenharia de software com IA e CLI

## 6. Configurar a API Key

Configure o agente com a sua chave do AI Studio (ela não aparece na tela):

```bash
cd ~/agente-estudos-agy/agente-estudos
read -s -p "Cole sua API Key: " KEY && echo

cat << EOF > .env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GEMINI_API_KEY=${KEY}
MODEL=gemini-3.8-flash
EOF

uv sync
```

## 7. Testar no ADK Web

```bash
uv run adk web --allow_origins="*"
```

Clique no link `http://127.0.0.1:8000` que aparece no terminal e escolha o agente `app`. Teste:

1. **Pedido incompleto:** o agente deve fazer perguntas antes de montar o plano.
    ```text
    Quero organizar meus estudos de JavaScript.
    ```
2. **Pedido completo:** o agente deve entregar o plano e chamar a ferramenta `WriteFile` para salvar o CSV.
    ```text
    Quero aprender JavaScript para fazer meu primeiro projeto de portfólio em 5 semanas. Começo segunda que vem. Posso estudar segunda, quarta e sexta, 2h por dia às 19h. Já sei HTML e CSS, mas nunca programei.
    ```
3. **Ajuste:** o agente deve reorganizar o plano e sobrescrever o CSV.
    ```text
    Perdi as sessões de quarta e sexta da primeira semana. Ajusta o plano?
    ```

No ADK Web, clique nos eventos `WriteFile` para ver os argumentos e a resposta da ferramenta. Depois confira o arquivo numa segunda aba do Cloud Shell:

```bash
cat ~/agente-estudos-agy/agente-estudos/planos/plano-de-estudos.csv
cloudshell download ~/agente-estudos-agy/agente-estudos/planos/plano-de-estudos.csv
```

Com o arquivo no computador, importe no [Google Agenda](https://calendar.google.com/): **Configurações → Importar e exportar → Importar**.

## 8. Evoluir o agente com o `agy`

Abra uma segunda aba no Cloud Shell (`+`) e rode:

```bash
cd ~/agente-estudos-agy
agy
```

**Revisão de código:**

```text
Revise o código do agente-estudos e liste os problemas por severidade antes de corrigir.
```

**Validar o resultado:**

```text
Leia agente-estudos/planos/plano-de-estudos.csv e confira se ele segue as regras do CSV em skills/plano-de-estudos/assets/plano_template.md: cabeçalho, formato de data e hora, aspas na descrição e nenhuma sessão fora dos dias combinados. Liste o que estiver errado.
```

**Corrigir um problema que você viu no teste:**

```text
No teste do ADK Web ou na validação, o agente [descreva o problema]. Descubra a causa e corrija.
```

**Nova skill:**

```text
Crie uma skill ADK chamada revisao-ativa, no mesmo padrão da plano-de-estudos, que recebe um material de estudo e gera flashcards e um quiz de 5 perguntas. Adicione-a ao agente.
```

Para testar, reinicie o ADK Web na primeira aba (`CTRL+C` e `uv run adk web --allow_origins="*"`).

## 9. Versionar no GitHub

1. Configure o seu nome e e-mail no git:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
```

2. No `agy`, peça para preparar os commits:

```text
Confira se não há API Key em nenhum arquivo versionado e faça commits com mensagens descritivas das mudanças.
```

3. Saia do `agy` (`/exit`) e envie para o seu repositório no GitHub:

```bash
cd ~/agente-estudos-agy
git remote set-url origin https://github.com/estevamvicttor/agente-estudos-agy.git
git push -u origin main
```

---

## 📚 Referências

- [Antigravity CLI](https://antigravity.google/)
- [Google ADK: documentação](https://adk.dev/)
- [ADK Skills](https://adk.dev/skills/) · [Especificação Agent Skills](https://agentskills.io/specification)
- [ADK EnvironmentToolset](https://adk.dev/integrations/environment-toolset/)
- [Google AI Studio: API Keys](https://aistudio.google.com/apikey)
