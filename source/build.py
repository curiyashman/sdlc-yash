#!/usr/bin/env python3
"""Builds the installable skills from source/.

  python source/build.py          write Product/, Design/, Development/, Common/
  python source/build.py --check  fail if the built folders differ from source (used by CI)

Each skill folder gets:
  SKILL.md                    source/skills/<name>.md with {{CORE}} replaced by source/core.md
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
TEAMS = {"product-": "Product", "design-": "Design", "dev-": "Development", "pdlc-": "Common"}
PACKS = {
    "compliance.md": ["product-00-product-context", "product-02-prd", "product-04-user-stories",
                      "dev-01-tech-design", "dev-05-test-qa"],
    "threat-model.md": ["dev-01-tech-design", "dev-03-build-tasks", "dev-05-test-qa", "dev-07-maintenance"],
    "ai-features.md": ["product-02-prd", "product-04-user-stories", "design-02-screen-mockups",
                       "dev-01-tech-design", "dev-03-build-tasks", "dev-04-code-plan-build",
                       "dev-05-test-qa", "dev-06-deploy", "dev-07-maintenance"],
    "ci-pdlc-lint.yml": ["product-00-product-context", "dev-00-dev-setup", "pdlc-next"],
}
INSTRUCTIONS = {  # extra files copied into team folders
    "instructions/product-project-instructions.md": "Product/claude-project-instructions.md",
    "instructions/design-agent-instructions.md": "Design/agent-instructions.md",
    "instructions/dev-agent-instructions.md": "Development/agent-instructions.md",
}


def build(out):
    core = open(os.path.join(HERE, "core.md")).read().strip("\n")
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
        text = text.replace("{{CORE}}", core)
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
    # every skill named in a SKILL.md must exist
    for team in set(TEAMS.values()):
        for dp, _, fns in os.walk(os.path.join(out, team)):
            for fn in fns:
                if fn.endswith(".md"):
                    for ref in re.findall(r"\b((?:product|design|dev)-0\d-[a-z-]+[a-z]|pdlc-next)\b", open(os.path.join(dp, fn)).read()):
                        if ref not in names:
                            problems.append(f"{os.path.relpath(os.path.join(dp, fn), out)}: names unknown skill {ref}")
    return names, problems


def tree(root):
    out = {}
    for team in set(TEAMS.values()):
        base = os.path.join(root, team)
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
        for team in set(TEAMS.values()):
            p = os.path.join(REPO, team)
            if os.path.isdir(p):
                shutil.rmtree(p)
        names, problems = build(REPO)
        for n in names:
            team = next(v for k, v in TEAMS.items() if n.startswith(k))
            size = os.path.getsize(os.path.join(REPO, team, n, "SKILL.md"))
            print(f"{team:12} {n:32} SKILL.md {size:6} bytes")
    for p in problems:
        print("PROBLEM", p)
    print(f"{len(names)} skills, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
