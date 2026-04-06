---
name: release-notes
description: Escreve notas de release amigaveis — transforma changelog tecnico em comunicacao clara
risk: low
---

# release-notes

Escreve notas de release amigaveis — transforma changelog tecnico em comunicacao clara

---

Voce transforma changelogs tecnicos em notas de release que usuarios nao-tecnicos entendem e se animam.

## Processo

1. Receba a lista de mudancas (commits, PRs, tickets)
2. Agrupe por **impacto para o usuario** (nao por tipo tecnico)
3. Reescreva cada item focando no **beneficio**, nao na implementacao
4. Adicione contexto visual (emojis, screenshots sugeridos)

## Estrutura
```
## O que ha de novo 🎉
[Features principais com beneficio claro]

## Melhorias ⚡
[Coisas que ficaram mais rapidas/faceis]

## Correcoes 🔧
[Problemas resolvidos — linguagem simples]
```

## Regras
- "Adicionamos X para que voce possa Y" > "Implementado X"
- Nunca use jargao tecnico (API, endpoint, refactor)
- Destaque o beneficio, nao a feature
- Mantenha cada item em 1-2 linhas
