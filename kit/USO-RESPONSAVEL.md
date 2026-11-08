# Uso responsável

Um modelo "sem censura" (*abliterated*) é um modelo aberto do qual foi tirado o reflexo de recusar. Ele
responde quase tudo — e por isso a responsabilidade passa a ser **sua**, não do modelo.

## As regras do kit

1. **Seus dados, seus sistemas.** Teste segurança só no que é seu ou no que o dono autorizou por escrito.
2. **Privado não é anônimo.** Rodar local esconde o pedido das empresas de IA; não muda o que é crime.
3. **Marca dos outros não se copia.** Recriar a *função* de um app para uso próprio é estudo; copiar nome,
   logo, cores e telas para distribuir é infração. O kit não traz exemplo disso de propósito.
4. **Resposta sem recusa também erra.** Modelo sem censura inventa com a mesma confiança. Em saúde, direito e
   dinheiro, confira com um profissional antes de agir.
5. **A porta do Ollama nunca fica aberta na internet.** Ele não tem senha. O Ollama escuta só em `127.0.0.1`. Para acessar de fora, use
   só a rede privada do Tailscale. `python3 kit/scripts/checa_local.py --so-porta` precisa dizer `loopback` ou
   `tailscale`, nunca `aberto`.
6. **Modelo baixado é código de terceiro.** Baixe de nomes conhecidos (o kit usa a biblioteca do Ollama) e
   não dê ferramentas ao modelo (ler arquivos, rodar comandos) antes de testá-lo só conversando.
7. **Menores de idade:** não instale modelo sem censura em computador usado por crianças.

## Quando NÃO usar o sem censura

Se o modelo normal resolve, use o normal. O quadrante (`kit/scripts/quadrante.py`) existe para isso: só vá
para "sem censura" quando o normal recusar uma tarefa legítima.
