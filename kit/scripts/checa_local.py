#!/usr/bin/env python3
"""Mede um modelo do Ollama e confere se a porta esta exposta.

O que faz:
  1. manda uma pergunta ao Ollama (sem internet, so o endereco que voce der);
  2. mede palavras por segundo (tokens/s) da resposta;
  3. confere em quais enderecos a porta do Ollama esta aberta (Linux/Mac);
  4. grava o resultado em kit/verificacao/<nome>.json.

Uso:
  python3 kit/scripts/checa_local.py --modelo qwen3.5:4b
  python3 kit/scripts/checa_local.py --base-url http://100.70.253.64:11434 --modelo qwen3.8:27b --nome casa-pelo-tailscale
  python3 kit/scripts/checa_local.py --so-porta
"""
import argparse
import datetime as dt
import json
import platform
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
PERGUNTA = ("Em portugues, em 3 frases: por que guardar exames medicos num modelo "
            "que roda no proprio computador protege a privacidade?")
LOOPBACK = ("127.0.0.1", "::1", "[::1]", "localhost")


def tokens_por_segundo(resp):
    """Calcula tok/s a partir da resposta do /api/generate do Ollama."""
    n, dur = resp.get("eval_count", 0), resp.get("eval_duration", 0)
    return round(n / (dur / 1e9), 2) if n and dur else 0.0


def perguntar(base_url, modelo, pergunta=PERGUNTA, max_tokens=160, timeout=600):
    corpo = json.dumps({"model": modelo, "prompt": pergunta, "stream": False, "think": False,
                        "options": {"num_predict": max_tokens}}).encode()
    req = urllib.request.Request(base_url.rstrip("/") + "/api/generate", data=corpo,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def enderecos_da_porta(saida_ss, porta=11434):
    """Le a saida de `ss -ltn` (ou `lsof`) e devolve os enderecos que escutam na porta."""
    achados = []
    for linha in saida_ss.splitlines():
        for campo in linha.split():
            if campo.endswith(f":{porta}") or campo.endswith(f".{porta}"):
                end = campo.rsplit(":", 1)[0] if ":" in campo else campo.rsplit(".", 1)[0]
                if end not in achados:
                    achados.append(end)
                break
    return achados


def classificar(enderecos):
    """loopback = so esta maquina; tailscale = so a sua rede privada; aberto = qualquer um."""
    if not enderecos:
        return "fechado"
    estados = set()
    for e in enderecos:
        e2 = e.strip("[]")
        if e2 in LOOPBACK or e2.startswith("127."):
            estados.add("loopback")
        elif e2.startswith("100.") or e2.startswith("fd7a:115c:a1e0"):
            estados.add("tailscale")
        else:
            estados.add("aberto")  # 0.0.0.0, *, ::, IP publico ou da rede local
    if "aberto" in estados:
        return "aberto"
    return "tailscale" if "tailscale" in estados else "loopback"


def ler_portas(porta=11434):
    if platform.system() == "Linux" and shutil.which("ss"):
        cmd = ["ss", "-ltn"]
    elif shutil.which("lsof"):
        cmd = ["lsof", "-nP", f"-iTCP:{porta}", "-sTCP:LISTEN"]
    else:
        return None
    return subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base-url", default="http://127.0.0.1:11434")
    p.add_argument("--modelo")
    p.add_argument("--nome", help="nome do arquivo em kit/verificacao/ (padrao: o modelo)")
    p.add_argument("--max-tokens", type=int, default=160)
    p.add_argument("--so-porta", action="store_true", help="so confere a exposicao da porta")
    a = p.parse_args(argv)

    resultado = {"quando": dt.datetime.now().isoformat(timespec="seconds"),
                 "maquina": platform.node(), "base_url": a.base_url}
    saida = ler_portas()
    if saida is not None:
        ends = enderecos_da_porta(saida)
        resultado["porta_11434"] = {"enderecos": ends, "estado": classificar(ends)}
        estado = resultado["porta_11434"]["estado"]
        print(f"Porta 11434 nesta maquina: {estado} {ends}")
        if estado == "aberto":
            print("PERIGO: o Ollama esta aberto para a rede. Volte para 127.0.0.1 (veja kit/guias/3-sempre-ligada.md).")
    if a.so_porta:
        return 1 if resultado.get("porta_11434", {}).get("estado") == "aberto" else 0
    if not a.modelo:
        p.error("informe --modelo")

    try:
        r = perguntar(a.base_url, a.modelo, max_tokens=a.max_tokens)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"ERRO: o modelo '{a.modelo}' nao esta baixado nesse Ollama. Rode: ollama pull {a.modelo}")
        else:
            print(f"ERRO: o Ollama respondeu {e.code} em {a.base_url}.")
        return 3
    except (urllib.error.URLError, OSError) as e:
        print(f"ERRO: o Ollama nao respondeu em {a.base_url} ({getattr(e, 'reason', e)}).")
        print("Abra o app do Ollama (Mac/Windows) ou rode 'ollama serve' (Linux); pelo Tailscale, confira o endereco 100.x e o 'tailscale serve status'.")
        return 3
    tps = tokens_por_segundo(r)
    resultado.update({"modelo": a.modelo, "tokens_por_segundo": tps,
                      "tokens_gerados": r.get("eval_count"),
                      "carregar_s": round(r.get("load_duration", 0) / 1e9, 1),
                      "total_s": round(r.get("total_duration", 0) / 1e9, 1),
                      "resposta": (r.get("response") or "").strip()})
    print(f"Modelo: {a.modelo}\nVelocidade: {tps} tokens/s  (carregar {resultado['carregar_s']} s, total {resultado['total_s']} s)")
    print("Resposta:", resultado["resposta"][:400])
    destino = KIT / "verificacao" / f"{(a.nome or a.modelo).replace('/', '_').replace(':', '-')}.json"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Gravado em", destino.relative_to(KIT.parent))
    return 0 if resultado["resposta"] else 2


if __name__ == "__main__":
    sys.exit(main())
