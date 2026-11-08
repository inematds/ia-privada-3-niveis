# Prompt 01 · Instalar o Ollama e escolher o modelo

Cole no seu assistente (Claude Code, Codex ou outro que rode comandos), com esta pasta aberta:

```text
Quero uma IA privada no meu computador, sem mandar nada para a internet. Use o kit desta pasta.

1. Leia kit/USO-RESPONSAVEL.md e kit/guias/2-local.md antes de qualquer comando.
2. Veja se o Ollama está instalado (ollama --version). Se não estiver, me mostre o comando de instalação do
   meu sistema e espere eu dizer "pode".
3. Rode python3 kit/scripts/escolhe_modelo.py e me mostre a saída inteira.
4. Me diga quanto disco os dois modelos vão ocupar e espere eu escolher: só o normal, só o sem censura, ou os dois.
5. Baixe o que eu escolher com ollama pull.
6. Rode python3 kit/scripts/checa_local.py --modelo <o modelo> e me mostre a velocidade e a linha da porta.
   Se a porta aparecer como "aberto", pare e me explique como voltar para 127.0.0.1.
7. Nunca mude o OLLAMA_HOST para 0.0.0.0 e nunca abra porta no roteador ou no firewall.
```
