# IA privada em 3 níveis — sua IA, na sua máquina, ligada o tempo todo

[![IA privada em 3 níveis](guia/assets/banner.jpg)](https://inematds.github.io/ia-privada-3-niveis/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Kit gratuito do INEMA para ter um modelo de IA que **não manda nada para fora** — e que você pode usar do
celular, de qualquer lugar. Ele escolhe o modelo certo para a sua máquina (normal ou sem censura), mede a
velocidade, confere se a porta está fechada e mostra dois jeitos de deixar a IA sempre ligada: a placa de
vídeo de casa pelo Tailscale, ou um modelo pequeno numa VPS. Tudo medido de verdade, com os números no guia.

## 📖 Guia de uso

**https://inematds.github.io/ia-privada-3-niveis/guia/**

## Os 3 níveis

| Nível | Onde o modelo roda | O que você paga | Onde está |
|---|---|---|---|
| 1 · API | servidor de outra empresa | por uso | kit [ia-sem-censura-defensiva](https://inematds.github.io/ia-sem-censura-defensiva/guia/) |
| 2 · Local | no seu computador | luz e disco | [`kit/guias/2-local.md`](kit/guias/2-local.md) |
| 3 · Sempre ligada | GPU de casa pelo Tailscale (A) ou VPS sem GPU (B) | nada (A) ou a VPS (B) | [`kit/guias/3-sempre-ligada.md`](kit/guias/3-sempre-ligada.md) |
| + Voz | Jarvis Local com cérebro sem censura | nada | [`kit/guias/4-voz-jarvis.md`](kit/guias/4-voz-jarvis.md) |

Antes de tudo: [`kit/USO-RESPONSAVEL.md`](kit/USO-RESPONSAVEL.md) e o quadrante
([`kit/guias/1-quadrante.md`](kit/guias/1-quadrante.md)).

## O processo, do início ao fim

Quem faz: 🧠 você numa sessão com o assistente · ⚙️ script do kit · 🤖 agente/modelo.

| # | Passo | Comando / arquivo | Quem |
|---|---|---|---|
| 1 | Ler as regras | [`kit/USO-RESPONSAVEL.md`](kit/USO-RESPONSAVEL.md) | 🧠 |
| 2 | Rodar os testes do kit (offline) | `python3 -m unittest discover -s kit/testes -v` | ⚙️ |
| 3 | Decidir o quadrante | `python3 kit/scripts/quadrante.py` | 🧠 + ⚙️ |
| 4 | Instalar o Ollama | `curl -fsSL https://ollama.com/install.sh \| sh` (Linux) ou instalador (Mac/Windows) | 🧠 / 🤖 com o [prompt 01](kit/prompts/01-instalar-e-escolher.md) |
| 5 | Escolher o modelo pela máquina | `python3 kit/scripts/escolhe_modelo.py` | ⚙️ |
| 6 | Baixar e medir | `ollama pull <modelo>` + `python3 kit/scripts/checa_local.py --modelo <modelo>` | ⚙️ |
| 7 | Conferir a porta | `python3 kit/scripts/checa_local.py --so-porta` → `loopback` | ⚙️ |
| 8a | Sempre ligada pela GPU de casa | `tailscale serve --bg --tcp 11434 tcp://127.0.0.1:11434` ([prompt 02](kit/prompts/02-casa-pelo-tailscale.md)) | 🤖, conferido por 🧠 |
| 8b | Sempre ligada numa VPS sem GPU | [prompt 03](kit/prompts/03-vps-sempre-ligada.md) | 🤖, conferido por 🧠 |
| 9 | Medir de outro aparelho | `checa_local.py --base-url http://100.x.y.z:11434 --modelo <modelo>` | ⚙️ |
| 10 | Voz (opcional) | cérebros de [`kit/config/jarvis-cerebros.exemplo.json`](kit/config/jarvis-cerebros.exemplo.json) no Jarvis Local | 🧠 |

## Requisitos

Python 3.10+ (só biblioteca padrão), Ollama, e — para o nível 3 — uma conta gratuita no Tailscale. Para o
caminho B, uma VPS Ubuntu com 8 GB de RAM ou mais.

## Licença

MIT — veja [LICENSE](LICENSE).
