#!/usr/bin/env python3
"""Builds the installable skills from source/.

  python source/build.py          write team folders + flat skills/ (for Cursor / Agent plugins)
  python source/build.py --check  fail if the built folders differ from source (used by CI)

Writes:
  Product/, Design/, Development/, QA/, Deployment/, Security/, Common/
  skills/<name>/                  flat copy of every skill (plugin discovery)

Each skill folder gets:
  SKILL.md                    source/skills/<name>.md with {{CORE}} replaced by
                              source/core.md (or source/core-security.md for sec-*)
  references/conventions.md   source/conventions.md (read on demand)
  references/<pack>           the packs this skill needs (see PACKS)
  scripts/pdlc.py             tools/pdlc.py
"""
import filecmp
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TEAMS = {"product-": "Product", "design-": "Design", "dev-": "Development", "qa-": "QA",
         "deploy-": "Deployment", "sec-": "Security", "pdlc-": "Common"}
SKILLS_DIR = "skills"
PACKS = {
    "compliance.md": ["product-00-product-context", "product-02-prd", "product-04-user-stories",
                      "design-04-design-system", "dev-01-tech-design", "dev-05-test-qa", "qa-01-test-plan",
                      "deploy-04-observability-sre", "deploy-05-incident-response"],
    "threat-model.md": ["dev-01-tech-design", "dev-03-build-tasks", "dev-05-test-qa", "dev-07-maintenance"],
    "ai-features.md": ["product-02-prd", "product-04-user-stories", "design-02-screen-mockups", "design-04-design-system",
                       "dev-01-tech-design", "dev-03-build-tasks", "dev-04-code-plan-build",
                       "dev-05-test-qa", "qa-01-test-plan", "qa-04-nonfunctional-testing",
                       "deploy-03-release", "deploy-04-observability-sre", "dev-07-maintenance"],
    "design-system-references.md": ["design-04-design-system"],
    "responsive-platforms.md": ["design-00-design-setup", "design-01-sitemap-flows", "design-02-screen-mockups",
                                "design-03-design-handoff", "design-04-design-system", "qa-01-test-plan",
                                "qa-04-nonfunctional-testing"],
    # Every non-Security product skill that the pack's team tables name. Intentional omits:
    # sec-* (use core-security + security-methodology/jurisdictions); pdlc-next (dispatcher only).
    "secure-by-design.md": ["product-00-product-context", "product-01-feature-brainstorm", "product-02-prd",
                            "product-03-ux-flows", "product-04-user-stories", "product-05-change-request",
                            "product-06-project-tracker", "product-07-launch",
                            "design-00-design-setup", "design-01-sitemap-flows", "design-02-screen-mockups",
                            "design-03-design-handoff", "design-04-design-system",
                            "dev-00-dev-setup", "dev-01-tech-design", "dev-02-data-model", "dev-03-build-tasks",
                            "dev-04-code-plan-build", "dev-05-test-qa", "dev-06-deploy", "dev-07-maintenance",
                            "qa-00-qa-setup", "qa-01-test-plan", "qa-02-test-execution", "qa-03-release-signoff",
                            "qa-04-nonfunctional-testing",
                            "deploy-00-deploy-setup", "deploy-01-environments", "deploy-02-pipeline",
                            "deploy-03-release", "deploy-04-observability-sre", "deploy-05-incident-response"],
    "qa-techniques.md": ["qa-00-qa-setup", "qa-01-test-plan", "qa-02-test-execution", "qa-03-release-signoff",
                         "qa-04-nonfunctional-testing"],
    "deploy-platforms.md": ["deploy-00-deploy-setup", "deploy-01-environments", "deploy-02-pipeline",
                            "deploy-03-release"],
    "deploy-methods.md": ["deploy-03-release", "deploy-05-incident-response", "deploy-02-pipeline"],
    "observability-sre.md": ["deploy-04-observability-sre", "deploy-05-incident-response", "deploy-01-environments"],
    "security-methodology.md": ["sec-00-engagement-scope", "sec-01-attack-surface", "sec-02-vulnerability-assessment",
                                "sec-03-privacy-compliance-audit", "sec-04-audit-report-remediation",
                                "sec-05-retest-signoff"],
    "security-jurisdictions.md": ["sec-00-engagement-scope", "sec-03-privacy-compliance-audit",
                                  "sec-04-audit-report-remediation"],
    "ci-pdlc-lint.yml": ["product-00-product-context", "dev-00-dev-setup", "deploy-02-pipeline", "pdlc-next"],
}
INSTRUCTIONS = {  # extra files copied into team folders
    "instructions/product-project-instructions.md": "Product/claude-project-instructions.md",
    "instructions/design-agent-instructions.md": "Design/agent-instructions.md",
    "instructions/dev-agent-instructions.md": "Development/agent-instructions.md",
    "instructions/qa-agent-instructions.md": "QA/agent-instructions.md",
    "instructions/deploy-agent-instructions.md": "Deployment/agent-instructions.md",
    "instructions/security-agent-instructions.md": "Security/agent-instructions.md",
}


def build(out):
    core = open(os.path.join(HERE, "core.md")).read().strip("\n")
    core_sec = open(os.path.join(HERE, "core-security.md")).read().strip("\n")
    problems = []
    names = []
    for fn in sorted(os.listdir(os.path.join(HERE, "skills"))):
        if not fn.endswith(".md"):
            continue
        name = fn[:-3]
        names.append(name)
        team = next(v for k, v in TEAMS.items() if name.startswith(k))
        text = open(os.path.join(HERE, "skills", fn)).read()
        if text.count("{{CORE}}") != 1:
            problems.append(f"{name}: needs exactly one {{{{CORE}}}}")
        text = text.replace("{{CORE}}", core_sec if name.startswith("sec-") else core)
        m = re.match(r'---\nname: (.+)\ndescription: "(.+)"\n---\n', text)
        if not m or m.group(1) != name:
            problems.append(f"{name}: frontmatter name must match the file name")
        else:
            d = m.group(2)
            if len(d) > 1024:
                problems.append(f"{name}: description is {len(d)} characters (max 1024)")
            if "<" in d or ">" in d:
                problems.append(f"{name}: description contains angle brackets")
        d = os.path.join(out, team, name)
        os.makedirs(os.path.join(d, "references"), exist_ok=True)
        os.makedirs(os.path.join(d, "scripts"), exist_ok=True)
        with open(os.path.join(d, "SKILL.md"), "w") as f:
            f.write(text if text.endswith("\n") else text + "\n")
        shutil.copyfile(os.path.join(HERE, "conventions.md"), os.path.join(d, "references", "conventions.md"))
        shutil.copyfile(os.path.join(REPO, "tools", "pdlc.py"), os.path.join(d, "scripts", "pdlc.py"))
        for pack, users in PACKS.items():
            if name in users:
                shutil.copyfile(os.path.join(HERE, "packs", pack), os.path.join(d, "references", pack))
    for src, dst in INSTRUCTIONS.items():
        p = os.path.join(HERE, src)
        if os.path.exists(p):
            os.makedirs(os.path.dirname(os.path.join(out, dst)), exist_ok=True)
            shutil.copyfile(p, os.path.join(out, dst))
    # Flat skills/ for Cursor Plugin and Agent Plugin discovery (install once at user root).
    skills_root = os.path.join(out, SKILLS_DIR)
    if os.path.isdir(skills_root):
        shutil.rmtree(skills_root)
    os.makedirs(skills_root, exist_ok=True)
    for name in names:
        team = next(v for k, v in TEAMS.items() if name.startswith(k))
        shutil.copytree(os.path.join(out, team, name), os.path.join(skills_root, name))
    # every skill named in a SKILL.md must exist
    for team in set(TEAMS.values()):
        for dp, _, fns in os.walk(os.path.join(out, team)):
            for fn in fns:
                if fn.endswith(".md"):
                    for ref in re.findall(r"\b((?:product|design|dev|qa|deploy|sec)-0\d-[a-z-]+[a-z]|pdlc-next)\b", open(os.path.join(dp, fn)).read()):
                        if ref not in names:
                            problems.append(f"{os.path.relpath(os.path.join(dp, fn), out)}: names unknown skill {ref}")
    return names, problems


def tree(root):
    out = {}
    for team in list(TEAMS.values()) + [SKILLS_DIR]:
        base = os.path.join(root, team)
        if not os.path.isdir(base):
            continue
        for dp, _, fns in os.walk(base):
            for fn in fns:
                p = os.path.join(dp, fn)
                out[os.path.relpath(p, root)] = p
    return out


def main():
    check = "--check" in sys.argv
    if check:
        tmp = tempfile.mkdtemp()
        names, problems = build(tmp)
        a, b = tree(tmp), tree(REPO)
        for rel in sorted(set(a) | set(b)):
            if rel not in b:
                problems.append(f"missing in repo (run build): {rel}")
            elif rel not in a:
                problems.append(f"not produced by source (remove or add to source): {rel}")
            elif not filecmp.cmp(a[rel], b[rel], shallow=False):
                problems.append(f"out of date (run build): {rel}")
        shutil.rmtree(tmp)
    else:
        for team in list(TEAMS.values()) + [SKILLS_DIR]:
            p = os.path.join(REPO, team)
            if os.path.isdir(p):
                shutil.rmtree(p)
        names, problems = build(REPO)
        for n in names:
            team = next(v for k, v in TEAMS.items() if n.startswith(k))
            size = os.path.getsize(os.path.join(REPO, team, n, "SKILL.md"))
            print(f"{team:12} {n:32} SKILL.md {size:6} bytes")
        print(f"skills/     {len(names)} flat skill folders (plugin layout)")
    for p in problems:
        print("PROBLEM", p)
    print(f"{len(names)} skills, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
