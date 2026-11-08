# 2 · Nível local: o modelo mora no seu computador

Nada do que você digita sai da máquina. Não há conta por palavra; o custo é luz e disco.

## Passo 1 — Instalar o Ollama

**Linux:**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Mac e Windows:** baixe o instalador em https://ollama.com/download e abra.

Confira:

```bash
ollama --version
```

O Ollama já sobe ouvindo só em `127.0.0.1` (só o próprio computador). **Deixe assim.**

## Passo 2 — Descobrir o modelo certo para a sua máquina

```bash
python3 kit/scripts/escolhe_modelo.py
```

Ele lê a memória (placa de vídeo, memória unificada do Mac ou RAM) e o disco, e mostra **dois** modelos:
o melhor normal e o melhor sem censura que cabem com folga. Não baixa nada sozinho.

| Memória | Normal | Sem censura | Tamanho |
|---|---|---|---|
| 8 GB | `qwen3.5:4b` | `huihui_ai/qwen3.5-abliterated:4B` | 3,3 GB |
| 16 GB | `qwen3.5:9b` | `huihui_ai/qwen3.5-abliterated:9b` | 6,6 GB |
| 24–32 GB | `qwen3.8:27b` | `huihui_ai/Qwen3.8-abliterated:27b` | 18 GB |
| 128 GB | `qwen3.5:122b` | `huihui_ai/qwen3.5-abliterated:122B` | 81 GB |

Com 32 GB ou mais ele também mostra uma **alternativa rápida** (`qwen3.6:35b-a3b`), que usa só uma parte do
modelo por palavra e responde mais depressa. Lista completa e data da conferência: `kit/modelos.json`.

## Passo 3 — Baixar e testar

```bash
ollama pull huihui_ai/qwen3.5-abliterated:9b
python3 kit/scripts/checa_local.py --modelo huihui_ai/qwen3.5-abliterated:9b
```

O `checa_local.py` faz uma pergunta, mede a velocidade (tokens por segundo), confere se a porta está fechada
para a rede e grava tudo em `kit/verificacao/`.

## Passo 4 — Conversar

```bash
ollama run huihui_ai/qwen3.5-abliterated:9b
```

Para sair, digite `/bye`. Quer uma janela em vez do terminal? O app do Ollama (Mac/Windows) já abre um chat
com os modelos baixados.

## Trocar entre normal e sem censura

Basta trocar o nome do modelo. Os dois ficam baixados lado a lado; o Ollama carrega o que você chamar.
