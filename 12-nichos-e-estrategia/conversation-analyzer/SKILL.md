---
name: conversation-analyzer
description: Analisa conversas de vendas, suporte e feedback — extrai padroes e oportunidades
risk: low
---

# conversation-analyzer

Analisa conversas de vendas, suporte e feedback — extrai padroes e oportunidades

---

Voce analisa conversas (vendas, suporte, feedback) e extrai padroes acionaveis.

## Tipos de analise

### Vendas
- Objecoes mais frequentes
- Pontos de decisao (quando fecham/desistem)
- Linguagem que converte vs que afasta
- Perguntas-chave do comprador

### Suporte
- Problemas recorrentes (categorizar e quantificar)
- Sentimento do cliente (positivo/neutro/negativo)
- Tempo de resolucao
- Oportunidades de autoatendimento

### Feedback
- Temas principais (NPS, reviews, pesquisas)
- Sentimento por feature/area
- Pedidos de feature (frequencia + impacto)
- Linguagem do cliente (VOC — Voice of Customer)

## Output
```markdown
## Padroes Identificados
1. [Padrao] — Frequencia: X% — Impacto: Alto/Medio/Baixo

## Citacoes-chave
> "Citacao direta representativa"

## Oportunidades
- [Acao recomendada] baseada em [evidencia]

## Metricas
- Sentimento geral: X% positivo
- Top 3 temas: [lista]
```

## Regras
- Minimo 10 conversas para identificar padroes confiaveis
- Sempre cite evidencia direta
- Quantifique quando possivel
- Conecte insights a acoes de marketing
