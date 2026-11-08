#!/usr/bin/env python3
"""Quadrante da IA privada: duas perguntas, uma resposta.

  1. O dado pode sair da sua maquina?   (nao -> local)
  2. O modelo normal recusa o que voce precisa fazer?  (sim -> sem censura)

Uso:
  python3 kit/scripts/quadrante.py --dado-sensivel sim --recusa nao
  python3 kit/scripts/quadrante.py            (pergunta na tela)
"""
import argparse
import sys

QUADRANTES = {
    (False, False): ("NUVEM NORMAL", "O melhor desempenho: o assistente que voce ja assina (Claude, ChatGPT).",
                     "Nada a instalar."),
    (False, True): ("NUVEM SEM CENSURA", "Modelo sem censura por API ou GPU alugada; o pedido sai da maquina.",
                    "Kit ia-sem-censura-defensiva (rotas API e RunPod)."),
    (True, False): ("LOCAL NORMAL", "Exames, contratos, financas, logs da empresa: nada sai do computador.",
                    "Nivel 2 deste kit: escolhe_modelo.py -> modelo normal."),
    (True, True): ("LOCAL SEM CENSURA", "Privado e sem recusa: pesquisa de seguranca nos seus sistemas, temas medicos e juridicos delicados.",
                   "Nivel 2 deste kit: escolhe_modelo.py -> modelo sem censura. Regras em USO-RESPONSAVEL.md."),
}


def decidir(dado_sensivel: bool, recusa: bool):
    nome, quando, como = QUADRANTES[(bool(dado_sensivel), bool(recusa))]
    return {"quadrante": nome, "quando": quando, "como": como}


def _sim(txt):
    t = (txt or "").strip().lower()
    if t in ("s", "sim", "y", "yes", "si", "1"):
        return True
    if t in ("n", "nao", "não", "no", "0"):
        return False
    raise ValueError(f"responda sim ou nao: {txt!r}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dado-sensivel", help="sim/nao: o dado NAO pode sair da sua maquina?")
    p.add_argument("--recusa", help="sim/nao: o modelo normal recusa a tarefa?")
    a = p.parse_args(argv)
    sens = a.dado_sensivel if a.dado_sensivel is not None else input("O dado NAO pode sair da sua maquina? (sim/nao) ")
    rec = a.recusa if a.recusa is not None else input("O modelo normal recusa a tarefa? (sim/nao) ")
    r = decidir(_sim(sens), _sim(rec))
    print(f"{r['quadrante']}\n  quando: {r['quando']}\n  como:   {r['como']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
