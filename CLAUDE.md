# CLAUDE.md — ia-privada-3-niveis

Kit + guia (PT/EN/ES) de IA privada: Ollama local, seletor de modelo pelo hardware, quadrante
local×nuvem / com×sem censura, sempre ligada pelo Tailscale (A: GPU de casa; B: VPS sem GPU).

- Conta/autor: `inematds <inematds@gmail.com>`. Pages da raiz; guia em `guia/` (+ `guia/en/`, `guia/es/`).
- Sem citar fonte (vídeo de terceiro). Sem afiliados. Sem exemplo de copiar app/marca de terceiro.
- Ollama nunca em 0.0.0.0. Expor só por `tailscale serve` (nunca `funnel`).
- Catálogo de modelos em `kit/modelos.json` com data de conferência; ao atualizar, rodar os testes.
- Números de velocidade só medidos (`kit/verificacao/*.json`), nunca estimados.
- Testes: `python3 -m unittest discover -s kit/testes -v`.

## Self-learning

When I correct you, or you catch yourself making a mistake: before continuing, add the lesson as a one-line
rule at the TOP of the Lessons section below, so it never happens again.

## Lessons
