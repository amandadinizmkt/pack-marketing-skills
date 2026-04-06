#!/usr/bin/env python3
"""
populate_skills.py — Popula o pack-marketing-skills com SKILL.md das fontes.

Lê os READMEs de cada categoria, extrai os nomes das skills,
e copia os SKILL.md correspondentes do kit-510-ptbr.
"""

import os
import re
import shutil
from pathlib import Path

PACK_ROOT = Path("/home/kursku/pack-marketing-skills")
KIT_ROOT = Path("/home/kursku/Skills/packs/kit-510-ptbr")
SKILLSHARE_ROOT = Path("/home/kursku/Skills/packs/global-skillshare-import")
SKILLS_ROOT = Path("/home/kursku/Skills")  # top-level categories

# Map category slugs to kit-510 directories
KIT_CATEGORY_MAP = {
    "01-copy-e-conteudo": ["01-conteudo-copy"],
    "02-email-e-automacao": ["02-email-automacao"],
    "03-seo-e-busca": ["05-seo-busca"],
    "04-anuncios-e-trafego": ["04-anuncios-trafego"],
    "05-conversao-e-cro": ["03-funis-vendas", "01-conteudo-copy"],
    "06-funis-e-vendas": ["03-funis-vendas", "06-financeiro-precos"],
    "07-lancamento-e-growth": ["08-lancamento-growth"],
    "08-redes-sociais": ["09-redes-sociais"],
    "09-marca-e-branding": ["14-marca-pessoal"],
    "10-analytics-e-dados": ["15-analytics-dados"],
    "11-infoprodutos-e-cursos": ["13-cursos-educacao"],
    "12-nichos-e-estrategia": ["16-nichos-especificos", "10-clientes-consultoria",
                                "06-financeiro-precos", "11-operacoes-sistemas",
                                "12-ia-automacao"],
}


def extract_skills_from_readme(readme_path: Path) -> list[str]:
    """Extract skill names from a category README.md table."""
    content = readme_path.read_text()
    # Match [skill-name](./skill-name/) pattern
    skills = re.findall(r'\[([a-z0-9-]+)\]\(\./[a-z0-9-]+/\)', content)
    return list(dict.fromkeys(skills))  # dedupe preserving order


def find_skill_in_kit(skill_name: str, kit_categories: list[str]) -> Path | None:
    """Find a SKILL.md in kit-510 categories."""
    # First check mapped categories
    for cat in kit_categories:
        skill_path = KIT_ROOT / cat / skill_name / "SKILL.md"
        if skill_path.exists():
            return skill_path

    # Then check ALL kit categories
    for cat_dir in sorted(KIT_ROOT.iterdir()):
        if cat_dir.is_dir():
            skill_path = cat_dir / skill_name / "SKILL.md"
            if skill_path.exists():
                return skill_path

    return None


def find_skill_in_skillshare(skill_name: str) -> Path | None:
    """Find a SKILL.md in skillshare import waves."""
    for wave_dir in sorted(SKILLSHARE_ROOT.iterdir()):
        if wave_dir.is_dir():
            skill_path = wave_dir / skill_name / "SKILL.md"
            if skill_path.exists():
                return skill_path
    return None


def find_skill_in_toplevel(skill_name: str) -> Path | None:
    """Find a SKILL.md in top-level Skills categories."""
    for cat_dir in sorted(SKILLS_ROOT.iterdir()):
        if cat_dir.is_dir() and not cat_dir.name.startswith(('.', 'packs', 'scripts', 'docs', '_')):
            skill_path = cat_dir / skill_name / "SKILL.md"
            if skill_path.exists():
                return skill_path
    return None


def find_skill_anywhere(skill_name: str, kit_categories: list[str]) -> Path | None:
    """Try all sources to find a SKILL.md."""
    # 1. Kit-510
    result = find_skill_in_kit(skill_name, kit_categories)
    if result:
        return result

    # 2. Skillshare import
    result = find_skill_in_skillshare(skill_name)
    if result:
        return result

    # 3. Top-level categories
    result = find_skill_in_toplevel(skill_name)
    if result:
        return result

    return None


def main():
    stats = {"copied": 0, "missing": 0, "total": 0}
    missing_skills = []

    for pack_cat_dir in sorted(PACK_ROOT.iterdir()):
        if not pack_cat_dir.is_dir() or pack_cat_dir.name.startswith(('.', 'scripts', 'docs')):
            continue

        readme = pack_cat_dir / "README.md"
        if not readme.exists():
            continue

        cat_name = pack_cat_dir.name
        kit_categories = KIT_CATEGORY_MAP.get(cat_name, [])
        skills = extract_skills_from_readme(readme)

        print(f"\n{'='*60}")
        print(f"📂 {cat_name} — {len(skills)} skills")
        print(f"{'='*60}")

        for skill_name in skills:
            stats["total"] += 1
            dest_dir = pack_cat_dir / skill_name
            dest_file = dest_dir / "SKILL.md"

            # Skip if already exists
            if dest_file.exists():
                stats["copied"] += 1
                continue

            source = find_skill_anywhere(skill_name, kit_categories)

            if source:
                dest_dir.mkdir(exist_ok=True)
                shutil.copy2(source, dest_file)
                print(f"  ✅ {skill_name}")
                stats["copied"] += 1
            else:
                print(f"  ❌ {skill_name} — NAO ENCONTRADA")
                stats["missing"] += 1
                missing_skills.append((cat_name, skill_name))

    print(f"\n{'='*60}")
    print(f"📊 RESULTADO")
    print(f"{'='*60}")
    print(f"  Total: {stats['total']}")
    print(f"  Copiadas: {stats['copied']}")
    print(f"  Faltando: {stats['missing']}")
    print(f"  Cobertura: {stats['copied']/stats['total']*100:.1f}%")

    if missing_skills:
        print(f"\n❌ Skills faltando ({len(missing_skills)}):")
        for cat, skill in missing_skills:
            print(f"  - {cat}/{skill}")

        # Save missing list for next step
        missing_file = PACK_ROOT / "scripts" / "missing_skills.txt"
        with open(missing_file, "w") as f:
            for cat, skill in missing_skills:
                f.write(f"{cat}/{skill}\n")
        print(f"\nLista salva em: {missing_file}")


if __name__ == "__main__":
    main()
