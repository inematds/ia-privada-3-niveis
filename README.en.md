# Private AI in 3 Levels — your AI, on your machine, running all the time

[![Private AI in 3 Levels](guia/assets/banner-en.jpg)](https://inematds.github.io/ia-privada-3-niveis/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

A free INEMA kit for running an AI model that **doesn’t send anything outside**—and that you can use from your
phone, anywhere. It chooses the right model for your machine (regular or uncensored), measures its speed,
checks that the port is closed, and shows two ways to keep the AI running all the time: your home GPU through
Tailscale, or a small model on a VPS. Everything is measured for real, with the numbers in the guide.

## 📖 User guide

**https://inematds.github.io/ia-privada-3-niveis/guia/en/**

## The 3 levels

| Level | Where the model runs | What you pay | Where to find it |
|---|---|---|---|
| 1 · API | another company’s server | per use | kit [ia-sem-censura-defensiva](https://inematds.github.io/ia-sem-censura-defensiva/guia/en/) |
| 2 · Local | on your computer | electricity and disk space | [`kit/guias/2-local.md`](kit/guias/2-local.md) (in Portuguese) |
| 3 · Always on | home GPU through Tailscale (A) or a GPU-free VPS (B) | nothing (A) or the VPS (B) | [`kit/guias/3-sempre-ligada.md`](kit/guias/3-sempre-ligada.md) (in Portuguese) |
| + Voice | Jarvis Local with an uncensored brain | nothing | [`kit/guias/4-voz-jarvis.md`](kit/guias/4-voz-jarvis.md) (in Portuguese) |

Before anything else: [`kit/USO-RESPONSAVEL.md`](kit/USO-RESPONSAVEL.md) (in Portuguese) and the quadrant
([`kit/guias/1-quadrante.md`](kit/guias/1-quadrante.md)) (in Portuguese).

## The process, from start to finish

Who does what: 🧠 you in a session with the assistant · ⚙️ kit script · 🤖 agent/model.

| # | Step | Command / file | Who |
|---|---|---|---|
| 1 | Read the rules | [`kit/USO-RESPONSAVEL.md`](kit/USO-RESPONSAVEL.md) (in Portuguese) | 🧠 |
| 2 | Run the kit tests (offline) | `python3 -m unittest discover -s kit/testes -v` | ⚙️ |
| 3 | Choose the quadrant | `python3 kit/scripts/quadrante.py` | 🧠 + ⚙️ |
| 4 | Install Ollama | `curl -fsSL https://ollama.com/install.sh \| sh` (Linux) or installer (Mac/Windows) | 🧠 / 🤖 with [prompt 01](kit/prompts/01-instalar-e-escolher.md) (in Portuguese) |
| 5 | Choose a model for your machine | `python3 kit/scripts/escolhe_modelo.py` | ⚙️ |
| 6 | Download and measure | `ollama pull <modelo>` + `python3 kit/scripts/checa_local.py --modelo <modelo>` | ⚙️ |
| 7 | Check the port | `python3 kit/scripts/checa_local.py --so-porta` → `loopback` | ⚙️ |
| 8a | Always on through your home GPU | `tailscale serve --bg --tcp 11434 tcp://127.0.0.1:11434` ([prompt 02](kit/prompts/02-casa-pelo-tailscale.md)) (in Portuguese) | 🤖, checked by 🧠 |
| 8b | Always on with a GPU-free VPS | [prompt 03](kit/prompts/03-vps-sempre-ligada.md) (in Portuguese) | 🤖, checked by 🧠 |
| 9 | Measure from another device | `checa_local.py --base-url http://100.x.y.z:11434 --modelo <modelo>` | ⚙️ |
| 10 | Voice (optional) | brains from [`kit/config/jarvis-cerebros.exemplo.json`](kit/config/jarvis-cerebros.exemplo.json) in Jarvis Local | 🧠 |

## Requirements

Python 3.10+ (standard library only), Ollama, and—for level 3—a free Tailscale account. For path B, an Ubuntu VPS
with 8 GB of RAM or more.

## License

MIT — see [LICENSE](LICENSE).