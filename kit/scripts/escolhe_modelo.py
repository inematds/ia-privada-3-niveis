#!/usr/bin/env python3
"""Escolhe o melhor modelo local (normal e sem censura) para esta maquina.

Le a memoria (placa de video, memoria unificada ou RAM) e o disco livre,
compara com kit/modelos.json e mostra os dois modelos e o comando para baixar.
Nao baixa nada sozinho.

Uso:
  python3 kit/scripts/escolhe_modelo.py
  python3 kit/scripts/escolhe_modelo.py --simular-memoria 16 --simular-disco 80
  python3 kit/scripts/escolhe_modelo.py --json
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
CATALOGO = KIT / "modelos.json"
FOLGA = 1.2          # contexto e cache ocupam ~20% alem do arquivo
RESERVA_RAM = 2.0    # sistema operacional, quando a memoria e compartilhada
RESERVA_VRAM = 0.5   # placa de video com memoria propria
FOLGA_DISCO = 5.0


def carregar_catalogo(caminho=CATALOGO):
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    return sorted(dados["modelos"], key=lambda m: m["nivel"])


def memoria_util(total_gb, dedicada):
    return max(0.0, total_gb - (RESERVA_VRAM if dedicada else RESERVA_RAM))


def cabe(tamanho_gb, util_gb):
    return tamanho_gb * FOLGA <= util_gb


def escolher(catalogo, total_gb, disco_gb, dedicada=False):
    """Devolve dict com o melhor normal e o melhor sem censura que cabem."""
    util = memoria_util(total_gb, dedicada)
    resultado = {"memoria_gb": total_gb, "memoria_util_gb": round(util, 1),
                 "disco_livre_gb": disco_gb, "dedicada": dedicada,
                 "normal": None, "sem_censura": None, "rapido": None, "avisos": []}
    for m in catalogo:
        if cabe(m["normal_gb"], util):
            if m.get("moe"):
                resultado["rapido"] = m
            else:
                resultado["normal"] = m
        if cabe(m["sem_censura_gb"], util) and not m.get("moe"):
            resultado["sem_censura"] = m
    if resultado["normal"] is None:
        resultado["avisos"].append(
            "Memoria pequena demais: nem o menor modelo cabe com folga. "
            "Use o nivel 1 (API) ou o caminho A (GPU de outra maquina pelo Tailscale).")
        return resultado
    if resultado["normal"]["nivel"] <= 2:
        resultado["avisos"].append(
            "So cabem modelos de teste (ate 2B): servem para frases curtas. Para trabalho de verdade, "
            "use o caminho A (a GPU de outra maquina pelo Tailscale) ou o nivel 1 (API).")
    precisa =resultado["normal"]["normal_gb"] + FOLGA_DISCO
    if resultado["sem_censura"]:
        precisa += resultado["sem_censura"]["sem_censura_gb"]
    menor = resultado["normal"]["normal_gb"] + FOLGA_DISCO
    if disco_gb < menor:
        resultado["avisos"].append(
            f"Disco livre ({disco_gb:.0f} GB) nao comporta nem um modelo ({menor:.0f} GB com folga). "
            "Libere espaco antes de baixar.")
    elif disco_gb < precisa:
        resultado["avisos"].append(
            f"Disco livre ({disco_gb:.0f} GB) menor que o necessario para os dois "
            f"modelos ({precisa:.0f} GB). Baixe um de cada vez ou libere espaco.")
    return resultado


def _nvidia_vram_gb():
    if not shutil.which("nvidia-smi"):
        return None
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    valores = []
    for linha in out.splitlines():
        try:
            valores.append(float(linha.strip()) / 1024)
        except ValueError:
            pass  # "[N/A]" = memoria unificada (ex.: DGX Spark)
    return sum(valores) if valores else None


def _ram_gb():
    if platform.system() == "Darwin":
        out = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True).stdout
        return int(out.strip()) / 1024 ** 3
    if platform.system() == "Windows":
        import ctypes

        class MS(ctypes.Structure):
            _fields_ = [("l", ctypes.c_ulong), ("m", ctypes.c_ulong), ("t", ctypes.c_ulonglong),
                        ("a", ctypes.c_ulonglong), ("tp", ctypes.c_ulonglong), ("ap", ctypes.c_ulonglong),
                        ("tv", ctypes.c_ulonglong), ("av", ctypes.c_ulonglong), ("e", ctypes.c_ulonglong)]
        s = MS(); s.l = ctypes.sizeof(MS)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s))
        return s.t / 1024 ** 3
    with open("/proc/meminfo") as f:
        for linha in f:
            if linha.startswith("MemTotal:"):
                return int(linha.split()[1]) / 1024 ** 2
    return 0.0


def detectar():
    vram = _nvidia_vram_gb()
    if vram:
        total, dedicada, origem = vram, True, "placa de video NVIDIA"
    else:
        total, dedicada = _ram_gb(), False
        origem = "memoria unificada" if platform.system() == "Darwin" else "RAM / memoria unificada"
    pasta = os.environ.get("OLLAMA_MODELS") or str(Path.home())
    disco = shutil.disk_usage(pasta).free / 1024 ** 3
    return round(total, 1), round(disco, 1), dedicada, origem


def texto(r, origem):
    linhas = [f"Memoria: {r['memoria_gb']} GB ({origem}); util para modelo: {r['memoria_util_gb']} GB",
              f"Disco livre: {r['disco_livre_gb']} GB", ""]
    if r["normal"]:
        m = r["normal"]
        linhas += [f"Melhor local (normal):       {m['nome']}  ->  ollama pull {m['normal']}  ({m['normal_gb']} GB)",
                   f"  uso: {m['uso']}"]
    if r["sem_censura"]:
        m = r["sem_censura"]
        linhas += [f"Melhor local (sem censura):  {m['nome']}  ->  ollama pull {m['sem_censura']}  ({m['sem_censura_gb']} GB)"]
    if r["rapido"]:
        m = r["rapido"]
        linhas += [f"Alternativa rapida:          {m['nome']}  ->  ollama pull {m['normal']}  /  {m['sem_censura']}"]
    linhas += [f"AVISO: {a}" for a in r["avisos"]]
    return "\n".join(linhas)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--simular-memoria", type=float, help="memoria em GB (em vez de detectar)")
    p.add_argument("--simular-disco", type=float, default=500, help="disco livre em GB na simulacao")
    p.add_argument("--placa-dedicada", action="store_true", help="na simulacao, memoria e de placa de video")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    if a.simular_memoria is not None:
        total, disco, dedicada, origem = a.simular_memoria, a.simular_disco, a.placa_dedicada, "simulado"
    else:
        total, disco, dedicada, origem = detectar()
    r = escolher(carregar_catalogo(), total, disco, dedicada)
    print(json.dumps(r, ensure_ascii=False, indent=1) if a.json else texto(r, origem))
    return 0


if __name__ == "__main__":
    sys.exit(main())
