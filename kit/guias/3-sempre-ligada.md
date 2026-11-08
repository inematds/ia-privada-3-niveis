# 3 · Sempre ligada: usar a sua IA de qualquer lugar

No nível 2 a IA só funciona sentado na frente do computador. Aqui ela fica disponível no celular e no
notebook, na rua ou no trabalho, **sem abrir nenhuma porta na internet**. O segredo é o **Tailscale**: uma
rede privada entre os seus aparelhos (grátis para uso pessoal). Só quem está logado na sua conta enxerga a IA.

## Qual caminho escolher

| | **A · GPU de casa pelo Tailscale** | **B · VPS sem placa de vídeo** |
|---|---|---|
| Onde roda | no seu computador forte, em casa | num servidor alugado |
| Modelo | o maior que a sua máquina aguenta (27B, 122B) | até 9B |
| Custo | zero (luz) | a mensalidade da VPS |
| Fica ligado se você desligar o computador? | não | sim |
| Voz (Jarvis) | sim | não (sem placa de vídeo) |

**Recomendação:** se você tem um computador com placa de vídeo que pode ficar ligado, use o **A**. Uma VPS
comum não tem placa de vídeo e não roda modelo grande — não pague por isso esperando um 27B.

## Números medidos (08/11/2026)

Mesma pergunta, 160 tokens de resposta, medidos com `checa_local.py`. Arquivos em `kit/verificacao/`.

| Onde roda | Modelo | Velocidade |
|---|---|---|
| Computador com GPU (128 GB de memória unificada), local | Qwen 3.8 27B sem censura | **17,8 tokens/s** |
| Computador com GPU, local | Qwen 3.8 27B normal | 15,4 tokens/s |
| **Caminho A:** a VPS chamando a GPU de casa pelo Tailscale | Qwen 3.8 27B sem censura | **20,1 tokens/s** |
| **Caminho B:** VPS 4 vCPU / 16 GB, só processador | Qwen 3.5 4B sem censura | 13,6 tokens/s |
| Caminho B, só processador | Qwen 3.5 4B normal | 12,6 tokens/s |
| Caminho B, só processador | Qwen 3.5 9B sem censura | 8,5 tokens/s |
| **Caminho B pela rede:** a GPU de casa chamando a VPS pelo Tailscale | Qwen 3.5 4B sem censura | 12,8 tokens/s |

O que os números dizem:

- **A rede do Tailscale não deixa mais lento.** As diferenças acima são variação entre rodadas, não custo da
  rede. Um texto de leitura confortável fica em torno de 10 tokens/s.
- **A primeira pergunta demora.** Carregar o modelo levou 16 a 47 s na VPS. Depois fica na memória por 5
  minutos (padrão do Ollama) e as respostas saem direto.
- **Sem censura não é mais lento** que o normal do mesmo tamanho.

## Caminho A — passo a passo

Na máquina de casa (com Ollama e o modelo do nível 2):

1. Instale o Tailscale: https://tailscale.com/download (Linux: `curl -fsSL https://tailscale.com/install.sh | sh`),
   depois `sudo tailscale up` e faça o login no navegador.
2. Confira que o Ollama está fechado: `python3 kit/scripts/checa_local.py --so-porta` → `loopback`.
3. Publique o Ollama **só** na sua rede privada:

   ```bash
   tailscale serve --bg --tcp 11434 tcp://127.0.0.1:11434
   ```

   Se der "Access denied": `sudo tailscale set --operator=$USER` uma vez e repita.
4. `tailscale serve status` tem que mostrar **"tailnet only"**. Nunca use `tailscale funnel`: o funnel
   abre para a internet inteira.
5. Pegue o endereço: `tailscale ip -4` (algo como `100.x.y.z`).

No celular ou no notebook: instale o Tailscale, entre na **mesma conta** e use `http://100.x.y.z:11434` em
qualquer app que fale com o Ollama. Para medir:

```bash
python3 kit/scripts/checa_local.py --base-url http://100.x.y.z:11434 --modelo huihui_ai/Qwen3.8-abliterated:27b --nome casa-pelo-tailscale
```

Para desligar: `tailscale serve --tcp 11434 off`.

## Caminho B — passo a passo

Numa VPS Ubuntu com pelo menos 8 GB de RAM (a medição usou 4 vCPU e 16 GB):

```bash
curl -fsSL https://ollama.com/install.sh | sh
ss -ltn | grep 11434
```

A segunda linha tem que mostrar só `127.0.0.1:11434`. Depois:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
tailscale serve --bg --tcp 11434 tcp://127.0.0.1:11434
ollama pull huihui_ai/qwen3.5-abliterated:4B
```

**Prova de que ficou fechado:** do seu computador, `http://<IP público da VPS>:11434` tem que **falhar**
(no teste: tempo esgotado), e `http://<IP Tailscale da VPS>:11434` tem que responder. O `checa_local.py
--so-porta` na VPS mostra `tailscale`.

Quer um assistente fazendo isso por você? Use o [prompt 03](../prompts/03-vps-sempre-ligada.md).

## O que não fazer

- `OLLAMA_HOST=0.0.0.0` numa VPS: o Ollama não tem senha e qualquer pessoa na internet usa (e esgota) o seu
  servidor. O `checa_local.py` acusa `aberto` e devolve erro.
- Abrir a porta 11434 no roteador de casa.
- `tailscale funnel` para o Ollama.
