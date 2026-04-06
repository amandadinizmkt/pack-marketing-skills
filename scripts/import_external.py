#!/usr/bin/env python3
"""
import_external.py — Importa skills faltantes dos repos externos.
"""

import shutil
from pathlib import Path

PACK = Path("/home/kursku/pack-marketing-skills")

# Map: (pack_category, skill_name) -> source_dir
EXTERNAL_MAP = {
    # From coreyhaines31/marketingskills
    ("01-copy-e-conteudo", "content-strategy"): "/tmp/marketingskills/skills/content-strategy",
    ("01-copy-e-conteudo", "cold-email"): "/tmp/marketingskills/skills/cold-email",
    ("01-copy-e-conteudo", "product-marketing-context"): "/tmp/marketingskills/skills/product-marketing-context",
    ("01-copy-e-conteudo", "lead-magnets"): "/tmp/marketingskills/skills/lead-magnets",
    ("03-seo-e-busca", "ai-seo"): "/tmp/marketingskills/skills/ai-seo",
    ("03-seo-e-busca", "site-architecture"): "/tmp/marketingskills/skills/site-architecture",
    ("04-anuncios-e-trafego", "ad-creative"): "/tmp/marketingskills/skills/ad-creative",
    ("05-conversao-e-cro", "customer-research"): "/tmp/marketingskills/skills/customer-research",
    ("06-funis-e-vendas", "sales-enablement"): "/tmp/marketingskills/skills/sales-enablement",
    ("06-funis-e-vendas", "revops"): "/tmp/marketingskills/skills/revops",
    ("06-funis-e-vendas", "churn-prevention"): "/tmp/marketingskills/skills/churn-prevention",

    # From alirezarezvani/claude-skills
    ("01-copy-e-conteudo", "content-production"): "/tmp/claude-skills/marketing-skill/content-production",
    ("01-copy-e-conteudo", "content-humanizer"): "/tmp/claude-skills/marketing-skill/content-humanizer",
    ("01-copy-e-conteudo", "video-content-strategist"): "/tmp/claude-skills/marketing-skill/video-content-strategist",
    ("01-copy-e-conteudo", "prompt-engineer-toolkit"): "/tmp/claude-skills/marketing-skill/prompt-engineer-toolkit",
    ("05-conversao-e-cro", "experiment-designer"): "/tmp/claude-skills/product-team/experiment-designer",
    ("06-funis-e-vendas", "competitive-teardown"): "/tmp/claude-skills/product-team/competitive-teardown",
    ("06-funis-e-vendas", "marketing-demand-acquisition"): "/tmp/claude-skills/marketing-skill/marketing-demand-acquisition",
    ("07-lancamento-e-growth", "marketing-ops"): "/tmp/claude-skills/marketing-skill/marketing-ops",
    ("07-lancamento-e-growth", "marketing-strategy-pmm"): "/tmp/claude-skills/marketing-skill/marketing-strategy-pmm",
    ("08-redes-sociais", "social-media-manager"): "/tmp/claude-skills/marketing-skill/social-media-manager",
    ("08-redes-sociais", "social-media-analyzer"): "/tmp/claude-skills/marketing-skill/social-media-analyzer",
    ("08-redes-sociais", "x-twitter-growth"): "/tmp/claude-skills/marketing-skill/x-twitter-growth",
    ("10-analytics-e-dados", "product-analytics"): "/tmp/claude-skills/product-team/product-analytics",
    ("12-nichos-e-estrategia", "cmo-advisor"): "/tmp/claude-skills/c-level-advisor/cmo-advisor",
    ("12-nichos-e-estrategia", "cro-advisor"): "/tmp/claude-skills/c-level-advisor/cro-advisor",
    ("12-nichos-e-estrategia", "revenue-operations"): "/tmp/claude-skills/business-growth/revenue-operations",
    ("12-nichos-e-estrategia", "sales-engineer"): "/tmp/claude-skills/business-growth/sales-engineer",

    # From blader/humanizer
    ("01-copy-e-conteudo", "humanizer"): "/tmp/humanizer",
}

def main():
    copied = 0
    failed = 0

    for (cat, skill), source_str in EXTERNAL_MAP.items():
        source = Path(source_str)
        dest = PACK / cat / skill

        if not source.exists():
            print(f"  ⚠️  Source not found: {source}")
            failed += 1
            continue

        if dest.exists():
            shutil.rmtree(dest)

        # Copy entire skill directory
        shutil.copytree(source, dest, dirs_exist_ok=True)

        # Remove .git if present (humanizer)
        git_dir = dest / ".git"
        if git_dir.exists():
            shutil.rmtree(git_dir)

        # Check if SKILL.md exists
        if (dest / "SKILL.md").exists():
            print(f"  ✅ {cat}/{skill} (with SKILL.md)")
        else:
            # Some repos use skill.md or other names
            md_files = list(dest.glob("*.md"))
            if md_files:
                print(f"  ✅ {cat}/{skill} (files: {[f.name for f in md_files]})")
            else:
                print(f"  ⚠️  {cat}/{skill} (no .md files found)")

        copied += 1

    print(f"\n📊 Imported: {copied}, Failed: {failed}")


if __name__ == "__main__":
    main()
