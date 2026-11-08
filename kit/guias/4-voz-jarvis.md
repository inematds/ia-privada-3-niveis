# 4 · Falar com ela: o interruptor "sem censura" no Jarvis local

Você não precisa de nenhum "sistema operacional de agentes" pago. O kit gratuito **Jarvis Local** do INEMA
(https://inematds.github.io/jarvis-local/guia/) já faz conversa por voz, ouvidos e memória 100% locais, com
uma prateleira de "cérebros" que você troca falando. Aqui você só acrescenta dois cérebros nessa prateleira.

## O que acrescentar no `config.json` do Jarvis

Copie as entradas de [`kit/config/jarvis-cerebros.exemplo.json`](../config/jarvis-cerebros.exemplo.json):

- `"sem_censura"` → o modelo sem censura que o `escolhe_modelo.py` indicou, no Ollama desta máquina;
- `"casa"` → o modelo da GPU de casa pelo Tailscale (guia 3, caminho A). Serve para o notebook leve usar a
  máquina forte.

Depois diga: **"muda para o cérebro sem censura"**, **"muda para casa"**, **"em qual cérebro você está?"**.
O selo na tela mostra qual está ligado — confira antes de perguntar algo delicado.

## Voz

A voz continua local (VoxCPM2 no Jarvis Local), fala português e não manda áudio para fora. Vozes por
assinatura na nuvem existem, mas mandam seu texto para um servidor: contradiz o objetivo deste kit.

## Atenção

- Voz pede placa de vídeo. Numa VPS sem placa de vídeo (guia 3, caminho B) use só texto.
- O cérebro sem censura não deve ganhar ferramentas (ler arquivos, rodar comandos) até você testá-lo só
  conversando. Ver `USO-RESPONSAVEL.md`.
