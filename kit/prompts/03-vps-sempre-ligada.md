# Prompt 03 · Um modelo pequeno ligado 24 horas numa VPS (caminho B)

Para quem não deixa computador ligado em casa. A VPS comum **não tem placa de vídeo**: só modelos de até 9B,
e devagar. Leia os números medidos em `kit/guias/3-sempre-ligada.md` antes de contratar.

Cole no assistente do seu computador, depois de criar a VPS (Ubuntu) e ter o acesso SSH:

```text
Tenho uma VPS Ubuntu em <IP>, acesso ssh root@<IP>. Quero um modelo sem censura pequeno rodando nela 24 h,
acessível só pela minha rede Tailscale. Siga kit/guias/3-sempre-ligada.md, caminho B.

1. Mostre a memória e os processadores (free -g; nproc) e rode o escolhe_modelo.py com --simular-memoria
   igual à memória da VPS. Me diga qual modelo cabe.
2. Instale o Ollama (curl -fsSL https://ollama.com/install.sh | sh) e confirme com ss -ltn que ele escuta
   só em 127.0.0.1:11434.
3. Instale o Tailscale na VPS (curl -fsSL https://tailscale.com/install.sh | sh; tailscale up) e me passe o
   link de login para eu aprovar.
4. Publique só na rede Tailscale: tailscale serve --bg --tcp 11434 tcp://127.0.0.1:11434
5. Confira de fora que a porta pública está FECHADA: do meu computador, a conexão em http://<IP público>:11434
   tem que falhar. Se abrir, pare tudo e me avise.
6. Baixe o modelo que coube e meça com checa_local.py pela rede Tailscale. Me mostre os tokens por segundo.
```
