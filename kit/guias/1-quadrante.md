# 1 · O quadrante: onde a sua IA deve rodar

Duas perguntas decidem tudo:

|  | **O modelo normal resolve** | **O modelo normal recusa** |
|---|---|---|
| **O dado pode sair da máquina** | NUVEM NORMAL — o assistente que você já assina | NUVEM SEM CENSURA — API ou GPU alugada (kit `ia-sem-censura-defensiva`) |
| **O dado NÃO pode sair** | LOCAL NORMAL — este kit, modelo normal | LOCAL SEM CENSURA — este kit, modelo sem censura |

```bash
python3 kit/scripts/quadrante.py --dado-sensivel sim --recusa nao
```

## Exemplos de cada quadrante

- **Nuvem normal:** escrever post, resumir um artigo público, gerar código de um projeto aberto.
- **Nuvem sem censura:** pesquisa de segurança num laboratório seu, quando você aceita que o pedido passe por
  um provedor.
- **Local normal:** exames médicos, contratos de clientes, planilha de finanças, logs do servidor da empresa.
- **Local sem censura:** analisar o log de um ataque ao **seu** servidor com os comandos reais do atacante;
  perguntas médicas ou jurídicas delicadas que o modelo normal desvia.

## O que se perde ao ir para a direita e para baixo

- **Local** = modelo menor que o da nuvem. Na nossa medição, um 27B local responde bem a texto e código, mas
  não chega ao nível dos maiores modelos pagos.
- **Sem censura** = um pouco menos de qualidade e **nenhum freio**: as regras de `USO-RESPONSAVEL.md` passam a
  ser o freio.
