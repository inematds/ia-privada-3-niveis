"""Testes offline do kit (nao chamam o Ollama nem a internet).

python3 -m unittest discover -s kit/testes -v
"""
import json
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import checa_local  # noqa: E402
import escolhe_modelo as em  # noqa: E402
import quadrante  # noqa: E402

CAT = em.carregar_catalogo()


class TestCatalogo(unittest.TestCase):
    def test_campos_e_ordem(self):
        niveis = [m["nivel"] for m in CAT]
        self.assertEqual(niveis, sorted(niveis))
        for m in CAT:
            for k in ("nome", "normal", "normal_gb", "sem_censura", "sem_censura_gb", "uso"):
                self.assertIn(k, m)
            self.assertIn("abliterated", m["sem_censura"])

    def test_sem_censura_nunca_e_o_normal(self):
        for m in CAT:
            self.assertNotEqual(m["normal"], m["sem_censura"])


class TestEscolhe(unittest.TestCase):
    def esc(self, mem, disco=500, dedicada=False):
        return em.escolher(CAT, mem, disco, dedicada)

    def test_sempre_cabe_na_memoria(self):
        for mem in (4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192):
            r = self.esc(mem)
            util = em.memoria_util(mem, False)
            for chave, campo in (("normal", "normal_gb"), ("sem_censura", "sem_censura_gb")):
                if r[chave]:
                    self.assertLessEqual(r[chave][campo] * em.FOLGA, util, (mem, chave))

    def test_8gb_pega_4b(self):
        r = self.esc(8)
        self.assertEqual(r["normal"]["normal"], "qwen3.5:4b")
        self.assertEqual(r["sem_censura"]["sem_censura"], "huihui_ai/qwen3.5-abliterated:4B")

    def test_16gb_pega_9b(self):
        self.assertEqual(self.esc(16)["normal"]["normal"], "qwen3.5:9b")

    def test_32gb_pega_27b_e_mostra_rapido(self):
        r = self.esc(32)
        self.assertEqual(r["normal"]["normal"], "qwen3.8:27b")
        self.assertEqual(r["rapido"]["normal"], "qwen3.6:35b-a3b")

    def test_128gb_pega_122b(self):
        self.assertEqual(self.esc(128)["sem_censura"]["sem_censura"], "huihui_ai/qwen3.5-abliterated:122B")

    def test_placa_24gb_dedicada_cabe_27b(self):
        self.assertEqual(self.esc(24, dedicada=True)["normal"]["normal"], "qwen3.8:27b")

    def test_memoria_minima_avisa_sem_quebrar(self):
        r = self.esc(2)
        self.assertIsNone(r["normal"])
        self.assertTrue(any("pequena demais" in a for a in r["avisos"]))

    def test_4gb_avisa_modelo_de_teste(self):
        r = self.esc(4)
        self.assertIsNotNone(r["normal"])
        self.assertTrue(any("modelos de teste" in a for a in r["avisos"]))

    def test_disco_curto_avisa(self):
        r = self.esc(32, disco=20)
        self.assertTrue(any("Disco livre" in a for a in r["avisos"]))

    def test_moe_nunca_e_o_normal(self):
        for mem in (32, 64, 128):
            r = self.esc(mem)
            self.assertFalse(r["normal"].get("moe"))
            self.assertFalse(r["sem_censura"].get("moe"))

    def test_cli_json(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            em.main(["--simular-memoria", "16", "--simular-disco", "80", "--json"])
        self.assertEqual(json.loads(buf.getvalue())["normal"]["normal"], "qwen3.5:9b")


class TestQuadrante(unittest.TestCase):
    def test_quatro_casos(self):
        self.assertEqual(quadrante.decidir(False, False)["quadrante"], "NUVEM NORMAL")
        self.assertEqual(quadrante.decidir(False, True)["quadrante"], "NUVEM SEM CENSURA")
        self.assertEqual(quadrante.decidir(True, False)["quadrante"], "LOCAL NORMAL")
        self.assertEqual(quadrante.decidir(True, True)["quadrante"], "LOCAL SEM CENSURA")

    def test_respostas_aceitas(self):
        self.assertTrue(quadrante._sim("Sim"))
        self.assertFalse(quadrante._sim("não"))
        with self.assertRaises(ValueError):
            quadrante._sim("talvez")


class TestChecaLocal(unittest.TestCase):
    def test_tokens_por_segundo(self):
        self.assertEqual(checa_local.tokens_por_segundo({"eval_count": 100, "eval_duration": 4_000_000_000}), 25.0)
        self.assertEqual(checa_local.tokens_por_segundo({}), 0.0)

    def test_porta_loopback(self):
        ss = "LISTEN 0 4096 127.0.0.1:11434 0.0.0.0:*\nLISTEN 0 128 0.0.0.0:22 0.0.0.0:*"
        ends = checa_local.enderecos_da_porta(ss)
        self.assertEqual(ends, ["127.0.0.1"])
        self.assertEqual(checa_local.classificar(ends), "loopback")

    def test_porta_aberta(self):
        for ss in ("LISTEN 0 4096 *:11434 *:*", "LISTEN 0 4096 0.0.0.0:11434 0.0.0.0:*",
                   "LISTEN 0 4096 [::]:11434 [::]:*", "LISTEN 0 4096 192.168.2.99:11434 0.0.0.0:*"):
            self.assertEqual(checa_local.classificar(checa_local.enderecos_da_porta(ss)), "aberto", ss)

    def test_porta_tailscale(self):
        ends = checa_local.enderecos_da_porta("LISTEN 0 4096 100.70.253.64:11434 0.0.0.0:*")
        self.assertEqual(checa_local.classificar(ends), "tailscale")

    def test_porta_tailscale_serve_com_interface(self):
        # saida real do `ss -ltn` com `tailscale serve` ligado (VPS Ubuntu, 08/11/2026)
        ss = ("LISTEN 0 4096 100.80.113.89%tailscale0:11434 0.0.0.0:*\n"
              "LISTEN 0 4096 127.0.0.1:11434 0.0.0.0:*\n"
              "LISTEN 0 4096 [fd7a:115c:a1e0::282a:715a]%tailscale0:11434 [::]:*")
        self.assertEqual(checa_local.classificar(checa_local.enderecos_da_porta(ss)), "tailscale")

    def test_porta_fechada(self):
        self.assertEqual(checa_local.classificar(checa_local.enderecos_da_porta("LISTEN 0 1 127.0.0.1:22 *:*")), "fechado")

    def test_lsof_mac(self):
        out = "ollama 123 eu 4u IPv4 0x1 0t0 TCP 127.0.0.1:11434 (LISTEN)"
        self.assertEqual(checa_local.classificar(checa_local.enderecos_da_porta(out)), "loopback")


if __name__ == "__main__":
    unittest.main()
