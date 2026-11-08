# Prompt 02 · Usar a GPU de casa de qualquer lugar (caminho A)

Cole no assistente **na máquina de casa** (a que tem a placa de vídeo):

```text
Quero acessar o Ollama desta máquina pelo celular e pelo notebook, de qualquer lugar, sem abrir porta na
internet. Siga kit/guias/3-sempre-ligada.md, caminho A.

1. Confira que o Ollama escuta só em 127.0.0.1: python3 kit/scripts/checa_local.py --so-porta deve dizer loopback.
2. Veja se o Tailscale está instalado e logado (tailscale status). Se não, me mostre o instalador do meu
   sistema e espere eu fazer o login no navegador.
3. Publique o Ollama só dentro da minha rede Tailscale com:
   tailscale serve --bg --tcp 11434 tcp://127.0.0.1:11434
   Se der "Access denied", me mostre o comando sudo tailscale set --operator=$USER e espere.
4. Mostre tailscale serve status e confirme que aparece "tailnet only". Nunca use tailscale funnel
   (funnel abre para a internet).
5. Me dê o endereço para usar nos outros aparelhos: http://<IP de tailscale ip -4>:11434
6. Para desligar depois: tailscale serve --tcp 11434 off
```

No outro aparelho (com o Tailscale logado na mesma conta):

```bash
python3 kit/scripts/checa_local.py --base-url http://100.x.y.z:11434 --modelo <modelo> --nome casa-pelo-tailscale
```
