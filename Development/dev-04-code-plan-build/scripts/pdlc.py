#!/usr/bin/env python3
"""pdlc.py: checks and views for a product's PDLC docs (Product, Design, Development,
QA, Deployment, Security chain).

Commands (run from anywhere; --root is the product's docs path, default docs/pdlc):
  lint     [--fix] [--strict]  validate headers, upstream versions, IDs, citations, dependencies,
                               queries, handoff and design references. --fix writes dep levels.
  board                        regenerate tracker.md from tracker.yaml and the file headers.
  next     [--team product|design|dev|qa|deploy|security]   the next steps and scopes, by dependency.
  new-id   KIND [PARENT]       the next free ID (initiative, module, sub-module, feature, story,
                               task, subtask, fr, br, nfr, ec, ac, ev, sc, fl, tc, bug, query,
                               cr, dec, hf, td, upg, spk, chr).
  open                         every Open item and query in one view.

Python 3.8+. Uses PyYAML when installed, otherwise a built-in reader for the subset the chain uses.
Exit code: 0 clean, 1 errors, 2 usage problem.
"""
import argparse
import os
import re
import subprocess
import sys
from datetime import date

VERSION = "1.0.0"

ROLES = ["backlog", "in_definition", "in_design", "ready_for_dev", "in_progress",
         "in_review", "in_qa", "done", "released", "blocked", "removed"]
DONE_ROLES = {"done", "released", "removed"}
BUILT_ROLES = {"in_review", "in_qa", "done", "released"}
HANDED_OFF_ROLES = {"ready_for_dev", "in_progress", "in_review", "in_qa", "done", "released"}

H2 = r"\d{2,}"
H3 = r"\d{3,}"
ID_RE = {
    "initiative": rf"I-{H3}",
    "module": rf"M{H2}",
    "sub-module": rf"M{H2}\.S{H2}",
    "feature": rf"M{H2}\.S{H2}\.F{H2}",
    "story": rf"M{H2}\.S{H2}\.F{H2}-US{H2}",
    "task": rf"M{H2}\.S{H2}\.F{H2}-US{H2}-T{H2}",
    "subtask": rf"M{H2}\.S{H2}\.F{H2}-US{H2}-T{H2}-ST{H2}",
    "bug": rf"BUG-{H3}",
    "hotfix": rf"HF-{H3}",
    "tech_debt": rf"TD-{H3}",
    "upgrade": rf"UPG-{H3}",
    "spike": rf"SPK-{H3}",
    "chore": rf"CHR-{H3}",
    "query": rf"Q-{H3}",
    "cr": rf"CR-{H3}",
    "dec": rf"DEC-{H3}",
}
PARENT_TYPE = {"sub-module": "module", "feature": "sub-module", "story": "feature",
               "task": "story", "subtask": "task"}
MAINT_TYPES = {"hotfix", "tech_debt", "upgrade", "spike", "chore"}
ITEM_TYPES = set(ID_RE) - {"query", "cr", "dec", "task", "subtask"}

SCOPE = rf"M{H2}(?:\.S{H2}(?:\.F{H2})?)?"
FEAT = rf"M{H2}\.S{H2}\.F{H2}"
STORY = rf"{FEAT}-US{H2}"
# citation kind -> (regex, owner path test)
CITE = {
    "FR": (rf"\b{FEAT}-FR{H2}\b", lambda p: p.endswith("/02-prd.md")),
    "BR": (rf"\b{FEAT}-BR{H2}\b", lambda p: p.endswith("/02-prd.md")),
    "EC": (rf"\b{FEAT}-EC{H2}\b", lambda p: "/04-stories/" in p),
    "AC": (rf"\b{STORY}-AC{H2}\b", lambda p: "/04-stories/" in p),
    "US": (rf"\b{STORY}\b(?!-(?:AC|T){H2})", lambda p: "/04-stories/" in p),
    "SC": (rf"\b{SCOPE}-SC{H2}\b", lambda p: "/03-ux/" in p),
    "FL": (rf"\b{SCOPE}-FL{H2}\b", lambda p: "/03-ux/" in p),
    "TC": (rf"\b{STORY}-TC{H2}\b",
           lambda p: "/05-qa/" in p or "/01-test-plan/" in p or p.startswith("qa/")
           or p.startswith("dev/releases/")),
    "NFR": (rf"\bI-{H3}-NFR{H2}\b", lambda p: p.endswith("/02-prd.md")),
    "EV": (rf"\b{FEAT}-EV{H2}\b", lambda p: "/04-stories/" in p),
}
STEP_ORDER = [
    "P00", "P01", "P02", "P03", "P04", "P05", "P06", "P07",
    "G00", "G01", "G02", "G03", "G04",
    "D00", "D01", "D02", "D03", "D04", "D05", "D06", "D07",
    "Q00", "Q01", "Q02", "Q03", "Q04",
    "O00", "O01", "O02", "O03", "O04", "O05",
    "S00", "S01", "S02", "S03", "S04", "S05",
    "DEC",
]
REQUIRED_KEYS = ["pdlc_step", "scope", "doc_version", "status", "depends_on", "updated"]
SKILL = {
    "P00": "product-00-product-context", "P01": "product-01-feature-brainstorm",
    "P02": "product-02-prd", "P03": "product-03-ux-flows", "P04": "product-04-user-stories",
    "P05": "product-05-change-request", "P06": "product-06-project-tracker",
    "P07": "product-07-launch", "G00": "design-00-design-setup",
    "G01": "design-01-sitemap-flows", "G02": "design-02-screen-mockups",
    "G03": "design-03-design-handoff",
    "G04": "design-04-design-system", "D00": "dev-00-dev-setup", "D01": "dev-01-tech-design",
    "D02": "dev-02-data-model", "D03": "dev-03-build-tasks", "D04": "dev-04-code-plan-build",
    "D05": "dev-05-test-qa", "D06": "dev-06-deploy", "D07": "dev-07-maintenance",
    "Q00": "qa-00-qa-setup", "Q01": "qa-01-test-plan", "Q02": "qa-02-test-execution",
    "Q03": "qa-03-release-signoff", "Q04": "qa-04-nonfunctional-testing",
    "O00": "deploy-00-deploy-setup", "O01": "deploy-01-environments", "O02": "deploy-02-pipeline",
    "O03": "deploy-03-release", "O04": "deploy-04-observability-sre",
    "O05": "deploy-05-incident-response",
    "S00": "sec-00-engagement-scope", "S01": "sec-01-attack-surface",
    "S02": "sec-02-vulnerability-assessment", "S03": "sec-03-privacy-compliance-audit",
    "S04": "sec-04-audit-report-remediation", "S05": "sec-05-retest-signoff",
}
TEAM_OF = {
    "P": "product", "G": "design", "D": "dev",
    "Q": "qa", "O": "deploy", "S": "security",
}
NEXT_TEAMS = ("product", "design", "dev", "qa", "deploy", "security")


def team_of_step(step):
    if not step:
        return "dev"
    return TEAM_OF.get(str(step)[0], "dev")

# ---------------------------------------------------------------- YAML

try:
    import yaml as _yaml  # type: ignore
except Exception:  # pragma: no cover
    _yaml = None
if os.environ.get("PDLC_NO_YAML"):
    _yaml = None


def _scalar(s):
    s = s.strip()
    if s == "" or s in ("~", "null"):
        return None
    if s[0] in "\"'" and s[-1] == s[0] and len(s) >= 2:
        return s[1:-1]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [] if not inner else [_scalar(x) for x in _split_flow(inner)]
    if s.startswith("{") and s.endswith("}"):
        inner = s[1:-1].strip()
        out = {}
        for part in _split_flow(inner):
            if ":" in part:
                k, v = part.split(":", 1)
                out[k.strip().strip("\"'")] = _scalar(v)
        return out
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return s


def _split_flow(s):
    parts, depth, cur, q = [], 0, "", None
    for ch in s:
        if q:
            cur += ch
            if ch == q:
                q = None
            continue
        if ch in "\"'":
            q = ch
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
            continue
        cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


def _strip_comment(line):
    out, q = "", None
    for i, ch in enumerate(line):
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out += ch
    return out.rstrip()


def _mini_load(text):
    lines = []
    for raw in text.splitlines():
        line = _strip_comment(raw)
        if line.strip():
            lines.append((len(line) - len(line.lstrip(" ")), line.strip()))
    pos = [0]

    def block(indent):
        if pos[0] >= len(lines):
            return None
        if lines[pos[0]][1].startswith("- ") or lines[pos[0]][1] == "-":
            return seq(lines[pos[0]][0])
        return mapping(lines[pos[0]][0])

    def mapping(indent):
        out = {}
        while pos[0] < len(lines):
            ind, txt = lines[pos[0]]
            if ind < indent or txt.startswith("- "):
                break
            if ind > indent:
                raise ValueError("bad indent: " + txt)
            key, _, rest = txt.partition(":")
            pos[0] += 1
            key = key.strip().strip("\"'")
            if rest.strip():
                out[key] = _scalar(rest)
            elif pos[0] < len(lines) and lines[pos[0]][0] > ind:
                out[key] = block(lines[pos[0]][0])
            elif pos[0] < len(lines) and lines[pos[0]][0] == ind and lines[pos[0]][1].startswith("- "):
                out[key] = seq(ind)
            else:
                out[key] = None
        return out

    def seq(indent):
        out = []
        while pos[0] < len(lines):
            ind, txt = lines[pos[0]]
            if ind != indent or not (txt.startswith("- ") or txt == "-"):
                break
            body = txt[2:].strip() if txt != "-" else ""
            if not body:
                pos[0] += 1
                out.append(block(lines[pos[0]][0]) if pos[0] < len(lines) and lines[pos[0]][0] > ind else None)
            elif re.match(r"^[\w\-\"']+\s*:(\s|$)", body) and not body.startswith(("[", "{")):
                # mapping item: rewrite the line as a mapping at indent+2
                lines[pos[0]] = (ind + 2, body)
                out.append(mapping(ind + 2))
            else:
                pos[0] += 1
                out.append(_scalar(body))
        return out

    return block(0) if lines else None


def yload(text):
    if _yaml:
        return _yaml.safe_load(text)
    return _mini_load(text)


def _ydump_value(v, indent):
    pad = " " * indent
    if isinstance(v, dict):
        if not v:
            return " {}\n"
        out = "\n"
        for k, x in v.items():
            out += f"{pad}{k}:" + _ydump_value(x, indent + 2)
        return out
    if isinstance(v, list):
        if not v:
            return " []\n"
        if all(not isinstance(x, (dict, list)) for x in v):
            return " [" + ", ".join(_yq(x) for x in v) + "]\n"
        out = "\n"
        for x in v:
            if isinstance(x, dict) and x:
                first = True
                for k, y in x.items():
                    lead = f"{pad}- " if first else f"{pad}  "
                    out += f"{lead}{k}:" + _ydump_value(y, indent + 4)
                    first = False
            else:
                out += f"{pad}-" + _ydump_value(x, indent + 2)
        return out
    return " " + _yq(v) + "\n"


def _yq(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    s = str(v)
    if s == "" or re.search(r"[:#\[\]{},&*!|>'\"%@`]", s) or s.strip() != s or s in ("true", "false", "null"):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def ydump(obj):
    out = ""
    for k, v in obj.items():
        out += f"{k}:" + _ydump_value(v, 2)
    return out

# ---------------------------------------------------------------- model


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append((where, msg))

    def warn(self, where, msg):
        self.warnings.append((where, msg))


def semver(v):
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", str(v or "").strip())
    return tuple(int(x) for x in m.groups()) if m else None


class Docs:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.files = {}      # rel path -> {"fm": dict|None, "body": str, "text": str}
        self.tracker = {}
        self.tracker_path = os.path.join(self.root, "tracker.yaml")
        self.tasks = []      # task dicts with "_file"
        self.load()

    def load(self):
        for dp, dns, fns in os.walk(self.root):
            dns[:] = [d for d in dns if not d.startswith(".") and d not in ("node_modules",)]
            for fn in fns:
                if not fn.endswith(".md") or fn == "tracker.md":
                    continue
                full = os.path.join(dp, fn)
                rel = os.path.relpath(full, self.root).replace(os.sep, "/")
                with open(full, encoding="utf-8") as f:
                    text = f.read()
                fm, body = None, text
                m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
                if m:
                    try:
                        fm = yload(m.group(1)) or {}
                    except Exception as e:  # noqa
                        fm = {"_error": str(e)}
                    body = text[m.end():]
                self.files[rel] = {"fm": fm, "body": body, "text": text}
                if "/03-tasks/" in "/" + rel:
                    for blk in re.findall(r"```ya?ml pdlc-tasks\s*\n(.*?)```", body, re.S):
                        try:
                            data = yload(blk) or []
                        except Exception as e:  # noqa
                            self.tasks.append({"_file": rel, "_error": str(e)})
                            continue
                        for t in data if isinstance(data, list) else []:
                            if isinstance(t, dict):
                                t["_file"] = rel
                                self.tasks.append(t)
        if os.path.exists(self.tracker_path):
            with open(self.tracker_path, encoding="utf-8") as f:
                self.tracker = yload(f.read()) or {}
        for k in ("initiatives", "items", "queries", "versions", "change_requests", "sprints"):
            if not isinstance(self.tracker.get(k), list):
                self.tracker[k] = self.tracker.get(k) or []
        self.tracker.setdefault("config", {})

    # convenience
    @property
    def items(self):
        return [i for i in self.tracker["items"] if isinstance(i, dict)]

    def item_index(self):
        idx = {}
        for i in self.items:
            idx[str(i.get("id"))] = i
        for t in self.tasks:
            if "id" in t:
                idx[str(t["id"])] = dict(t, type="task")
                for st in t.get("subtasks") or []:
                    if isinstance(st, dict) and "id" in st:
                        idx[str(st["id"])] = dict(st, type="subtask", parent=t["id"])
        return idx

    def chain_docs(self):
        return {p: d for p, d in self.files.items() if d["fm"] and "pdlc_step" in d["fm"]}

    def design_stage(self):
        cfg = self.tracker.get("config") or {}
        if "design_stage" in cfg:
            return bool(cfg["design_stage"])
        d = self.files.get("design/00-design-setup.md")
        return bool(d and d["fm"] and d["fm"].get("status") == "approved")

    def qa_stage(self):
        cfg = self.tracker.get("config") or {}
        if "qa_stage" in cfg:
            return bool(cfg["qa_stage"])
        d = self.files.get("qa/00-qa-setup.md")
        return bool(d and d["fm"] and d["fm"].get("status") == "approved")

    def deploy_stage(self):
        cfg = self.tracker.get("config") or {}
        if "deploy_stage" in cfg:
            return bool(cfg["deploy_stage"])
        d = self.files.get("deploy/00-deploy-setup.md")
        return bool(d and d["fm"] and d["fm"].get("status") == "approved")

    def security_stage(self):
        cfg = self.tracker.get("config") or {}
        if "security_stage" in cfg:
            return bool(cfg["security_stage"])
        # Any approved engagement scope turns the stage on when the flag is unset.
        for p, d in self.files.items():
            if p.startswith("security/") and p.endswith("00-engagement.md"):
                fm = d.get("fm") or {}
                if fm.get("status") == "approved" and str(fm.get("pdlc_step")) == "S00":
                    return True
        return False

    def status_name(self, role):
        names = (self.tracker.get("config") or {}).get("statuses") or {}
        return names.get(role, role)

    def find(self, step, initiative=None, scope=None):
        for p, d in sorted(self.chain_docs().items()):
            fm = d["fm"]
            if str(fm.get("pdlc_step")) != step:
                continue
            if initiative is not None and str(fm.get("initiative", "")) != initiative:
                continue
            if scope is not None and str(fm.get("scope", "")) != scope:
                continue
            return p, fm
        return None, None

    def scopes(self):
        out = []
        for ini in self.tracker["initiatives"]:
            if not isinstance(ini, dict):
                continue
            for s in ini.get("scopes") or []:
                if isinstance(s, dict) and s.get("id"):
                    out.append((str(ini.get("id")), s))
        return out


# ---------------------------------------------------------------- checks

def stale_map(docs, rep=None):
    """path -> list of (dep, pinned, current) for MAJOR/MINOR moves."""
    stale = {}
    for p, d in docs.chain_docs().items():
        deps = d["fm"].get("depends_on") or []
        if isinstance(deps, str):
            deps = [deps]
        for dep in deps:
            dep = str(dep)
            if "@" not in dep:
                if rep:
                    rep.err(p, f"depends_on entry without @version: {dep}")
                continue
            path, ver = dep.rsplit("@", 1)
            path = path.strip()
            tgt = docs.files.get(path)
            if tgt is None:
                if rep:
                    rep.err(p, f"depends_on points to a missing file: {path}")
                continue
            cur = semver((tgt["fm"] or {}).get("doc_version"))
            pin = semver(ver)
            if not pin or not cur:
                if rep:
                    rep.err(p, f"bad version in depends_on or upstream header: {dep}")
                continue
            if pin > cur:
                if rep:
                    rep.err(p, f"pins {path}@{ver} but that file is at {'.'.join(map(str, cur))}")
            elif pin[:2] < cur[:2]:
                stale.setdefault(p, []).append((path, ver, ".".join(map(str, cur))))
    return stale


def check_headers(docs, rep):
    for p, d in docs.files.items():
        top = p.split("/")[0]
        if top not in ("product", "design", "dev", "decisions"):
            continue
        fm = d["fm"]
        if fm is None:
            rep.err(p, "no front matter header")
            continue
        if "_error" in fm:
            rep.err(p, f"header is not valid YAML: {fm['_error']}")
            continue
        for k in REQUIRED_KEYS:
            if k not in fm:
                rep.err(p, f"header is missing '{k}'")
        step = str(fm.get("pdlc_step", ""))
        if step and step not in STEP_ORDER:
            rep.err(p, f"unknown pdlc_step '{step}'")
        if fm.get("status") not in ("draft", "approved", "superseded"):
            rep.err(p, f"status must be draft, approved, or superseded (is '{fm.get('status')}')")
        if not semver(fm.get("doc_version")):
            rep.err(p, f"doc_version must be MAJOR.MINOR.PATCH (is '{fm.get('doc_version')}')")
        if step in ("P01", "P02", "P03", "P04", "G01", "G02", "G03", "D01", "D02", "D03") and \
                not (step == "D01" and p == "dev/architecture.md") and not fm.get("initiative"):
            rep.err(p, "header is missing 'initiative'")
        if "Change log" not in d["body"]:
            rep.warn(p, "no Change log section")
        bl = fm.get("blocking") or []
        if bl and not fm.get("open_items"):
            rep.err(p, "lists blocking items but open_items is 0")


def check_ids(docs, rep):
    seen = {}
    idx = {}
    for i in docs.items:
        iid, typ = str(i.get("id", "")), i.get("type")
        if not iid:
            rep.err("tracker.yaml", f"item without id: {i}")
            continue
        if typ not in ITEM_TYPES:
            rep.err("tracker.yaml", f"{iid}: unknown type '{typ}'")
        elif not re.fullmatch(ID_RE[typ], iid):
            rep.err("tracker.yaml", f"{iid}: ID does not match type '{typ}'")
        if iid in seen:
            rep.err("tracker.yaml", f"{iid}: duplicate ID")
        seen[iid] = True
        idx[iid] = i
        st = i.get("status")
        if st not in ROLES:
            rep.err("tracker.yaml", f"{iid}: status '{st}' is not a role ({', '.join(ROLES)})")
        if typ in PARENT_TYPE:
            par = str(i.get("parent", ""))
            if not par:
                rep.err("tracker.yaml", f"{iid}: no parent")
            elif not iid.startswith(par):
                rep.err("tracker.yaml", f"{iid}: ID does not sit under parent {par}")
            elif par not in idx and par not in {str(x.get('id')) for x in docs.items}:
                rep.err("tracker.yaml", f"{iid}: parent {par} is not in the tracker")
        if typ == "story" and not i.get("scope"):
            rep.err("tracker.yaml", f"{iid}: story without scope")
        src = i.get("source")
        if src:
            sp = str(src).split("@")[0]
            if sp not in docs.files:
                rep.err("tracker.yaml", f"{iid}: source file not found: {sp}")
            elif typ in ("story", "feature") and iid not in docs.files[sp]["text"]:
                rep.err("tracker.yaml", f"{iid}: not found in its source file {sp}")
        elif typ not in ("module", "sub-module", "feature") or st not in ("released", "removed"):
            if typ != "initiative":
                rep.warn("tracker.yaml", f"{iid}: no source")
    for t in docs.tasks:
        if "_error" in t:
            rep.err(t["_file"], f"pdlc-tasks block is not valid YAML: {t['_error']}")
            continue
        tid = str(t.get("id", ""))
        if not re.fullmatch(ID_RE["task"], tid):
            rep.err(t["_file"], f"task ID '{tid}' is not a task ID")
            continue
        if tid in seen:
            rep.err(t["_file"], f"{tid}: duplicate ID")
        seen[tid] = True
        story = tid.rsplit("-T", 1)[0]
        if story not in idx:
            rep.err(t["_file"], f"{tid}: its story {story} is not in the tracker")
        if t.get("status") not in ROLES:
            rep.err(t["_file"], f"{tid}: status '{t.get('status')}' is not a role")
        for st in t.get("subtasks") or []:
            sid = str((st or {}).get("id", ""))
            if not re.fullmatch(ID_RE["subtask"], sid) or not sid.startswith(tid + "-ST"):
                rep.err(t["_file"], f"{sid}: not a sub-task ID under {tid}")
            if sid in seen:
                rep.err(t["_file"], f"{sid}: duplicate ID")
            seen[sid] = True
    for key, prefix in (("queries", "query"), ("change_requests", "cr")):
        for q in docs.tracker.get(key) or []:
            qid = str((q or {}).get("id", ""))
            if not re.fullmatch(ID_RE[prefix], qid):
                rep.err("tracker.yaml", f"{key}: bad ID '{qid}'")
            if qid in seen:
                rep.err("tracker.yaml", f"{qid}: duplicate ID")
            seen[qid] = True
    # gaps
    groups = {}
    for iid in seen:
        m = re.fullmatch(r"(.*?)(\d+)", iid)
        if m:
            groups.setdefault(m.group(1), []).append(int(m.group(2)))
    for pre, nums in groups.items():
        nums = sorted(nums)
        missing = sorted(set(range(1, nums[-1] + 1)) - set(nums))
        if missing:
            rep.warn("ids", f"{pre}: numbers {missing} are missing; removed items stay with status removed, IDs are never reused")


def dep_graph(docs, rep=None):
    idx = docs.item_index()
    graph = {}
    for iid, i in idx.items():
        deps = i.get("depends_on") or []
        if isinstance(deps, str):
            deps = [deps]
        graph[iid] = [str(d) for d in deps]
        if rep:
            for d in graph[iid]:
                if d not in idx:
                    rep.err("dependencies", f"{iid} depends on {d}, which is not in the tracker or a task block")
    return idx, graph


def compute_levels(docs, rep=None):
    idx, graph = dep_graph(docs, rep)
    WHITE, GREY, BLACK = 0, 1, 2
    color, level, cycles = {}, {}, []

    def visit(n, stack):
        color[n] = GREY
        stack.append(n)
        lv = 0
        for d in graph.get(n, []):
            if d not in idx:
                continue
            if color.get(d, WHITE) == GREY:
                cycles.append(stack[stack.index(d):] + [d])
                continue
            if color.get(d, WHITE) == WHITE:
                visit(d, stack)
            if idx[d].get("status") not in DONE_ROLES:
                lv = max(lv, level.get(d, 0) + 1)
        level[n] = lv
        color[n] = BLACK
        stack.pop()

    for n in sorted(idx):
        if color.get(n, WHITE) == WHITE:
            visit(n, [])
    if rep:
        for c in cycles:
            rep.err("dependencies", "cycle: " + " -> ".join(c))
    return level, cycles


def check_levels(docs, rep, fix):
    level, cycles = compute_levels(docs, rep)
    changed = {}
    for i in docs.items:
        iid = str(i.get("id"))
        if iid in level and i.get("status") not in DONE_ROLES:
            if i.get("dep_level") != level[iid]:
                if fix and not cycles:
                    i["dep_level"] = level[iid]
                    changed[iid] = level[iid]
                else:
                    rep.warn("tracker.yaml", f"{iid}: dep_level is {i.get('dep_level')}, computed {level[iid]} (run lint --fix)")
    return changed, level


def check_citations(docs, rep):
    defined = {k: set() for k in CITE}
    for p, d in docs.files.items():
        for k, (rx, owner) in CITE.items():
            if owner(p):
                defined[k].update(re.findall(rx, d["text"]))
    items = docs.item_index()
    for k in ("US",):
        defined[k].update(i for i in items if re.fullmatch(STORY, i))
    for p, d in docs.files.items():
        if not d["fm"]:
            continue
        for k, (rx, owner) in CITE.items():
            if owner(p):
                continue
            for ref in set(re.findall(rx, d["text"])):
                if ref not in defined[k]:
                    rep.err(p, f"cites {ref}, which is not defined in any {k} owner file")
        for ref in set(re.findall(rf"\b(?:{SCOPE})\b(?![\-.\w])", d["body"])):
            if ref not in items and not re.fullmatch(r"M00(\..*)?", ref):
                rep.warn(p, f"cites {ref}, which is not in the tracker (product map node?)")
        for ref in set(re.findall(rf"\b(?:Q|CR|BUG|HF|TD|UPG|SPK|CHR)-{H3}\b", d["text"])):
            known = items.keys() | {str(q.get('id')) for q in docs.tracker.get('queries') or []} | \
                {str(c.get('id')) for c in docs.tracker.get('change_requests') or []}
            if ref not in known:
                rep.err(p, f"cites {ref}, which is not in tracker.yaml")
        for ref in set(re.findall(rf"\bDEC-{H3}\b", d["text"])):
            if not any(f.startswith(f"decisions/{ref}") for f in docs.files):
                rep.err(p, f"cites {ref}, but decisions/{ref}-*.md does not exist")


def check_tracker_rules(docs, rep):
    idx = docs.item_index()
    design = docs.design_stage()
    chain = docs.chain_docs()
    for q in docs.tracker.get("queries") or []:
        qid = q.get("id")
        if q.get("status") not in ("open", "answered", "became_cr"):
            rep.err("tracker.yaml", f"{qid}: status must be open, answered, or became_cr")
        for a in q.get("about") or []:
            if str(a) not in idx:
                rep.err("tracker.yaml", f"{qid}: about {a}, which is not in the tracker")
        if q.get("status") == "open" and q.get("blocking"):
            for a in q.get("about") or []:
                it = idx.get(str(a))
                if it and it.get("type") == "story" and it.get("status") not in ("blocked", "removed"):
                    rep.warn("tracker.yaml", f"{qid} is open and blocking, but {a} is '{it.get('status')}', not blocked")
        if q.get("status") in ("answered", "became_cr") and not q.get("answer"):
            rep.err("tracker.yaml", f"{qid}: answered without an answer (file@version or CR)")
    scope_na = {}
    for ini, s in docs.scopes():
        scope_na[str(s["id"])] = (ini, s.get("na") or {})
    for i in docs.items:
        if i.get("type") != "story":
            continue
        iid, st, scope = str(i.get("id")), i.get("status"), str(i.get("scope", ""))
        src = str(i.get("source", "")).split("@")[0]
        if st in HANDED_OFF_ROLES | {"in_design"}:
            fm = (docs.files.get(src) or {}).get("fm") or {}
            if fm.get("status") != "approved":
                rep.err("tracker.yaml", f"{iid}: '{st}' but its stories file is not approved")
        if scope not in scope_na:
            rep.warn("tracker.yaml", f"{iid}: scope {scope} is not listed under its initiative's scopes")
        _, na = scope_na.get(scope, ("", {}))
        has_ui = "P03" not in na
        if design and has_ui and "G03" not in na and st in HANDED_OFF_ROLES:
            p, fm = docs.find("G03", scope=scope)
            if not fm or fm.get("status") != "approved":
                rep.err("tracker.yaml", f"{iid}: '{st}' but the scope's design handoff (G03) is not approved")
            body = (docs.files.get(src) or {}).get("text", "")
            m = re.search(re.escape(iid) + r".*?<!-- design-refs:start -->(.*?)<!-- design-refs:end -->", body, re.S)
            if not m or not m.group(1).strip():
                rep.err(src, f"{iid}: no design references, but the scope has screens and a design stage")
            elif re.search(r"\b(stale|not yet designed)\b", m.group(1)):
                rep.err(src, f"{iid}: design references are stale or not yet designed")
    # blocking items in files vs approval
    for p, d in chain.items():
        fm = d["fm"]
        if fm.get("status") == "approved" and fm.get("blocking"):
            rep.warn(p, f"approved with blocking Open items {fm.get('blocking')}")


EARS_RE = re.compile(
    r"^(?:(?:while|when|where|if)\b[^,]*,\s*)*(?:then\s+)?(?:the\s+)?[a-z][\w\s'-]*?\bshall\b(?:\s+not)?\s+\S",
    re.I)
EARS_ID = re.compile(rf"^(?:{FEAT}-(?:FR|BR){H2}|I-{H3}-NFR{H2})$")


def check_ears(docs, rep):
    """Every FR, BR, and NFR row in a PRD is one EARS sentence."""
    for p, d in docs.files.items():
        if not p.endswith("/02-prd.md"):
            continue
        for line in d["body"].splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.strip().startswith("|") else []
            if len(cells) < 2:
                continue
            rid = re.sub(r"[*`]", "", cells[0])
            if not EARS_ID.match(rid):
                continue
            text = re.sub(r"[*`_]", "", cells[1]).strip()
            if not EARS_RE.match(text):
                rep.err(p, f"{rid} is not an EARS sentence: '{text[:70]}'")
            elif re.search(r"\b(should|may|etc\.?|as appropriate|and/or)\b", text, re.I):
                rep.warn(p, f"{rid} uses a vague word (should, may, etc., as appropriate, and/or)")


def check_tests(docs, rep):
    """Every test case covers an AC, EC, TH, or EV; build plans keep a read map, reuse map, and budget."""
    for p, d in docs.files.items():
        if "/05-qa/" in "/" + p or (p.startswith("dev/releases/") and p.endswith("-qa.md")):
            for line in d["body"].splitlines():
                m = re.match(rf"^\|\s*\**({STORY}-TC{H2})\**\s*\|(.*)", line.strip())
                if m and not re.search(rf"{STORY}-AC{H2}|\bAC{H2}\b|{FEAT}-EC{H2}|\bTH{H2}\b|{FEAT}-EV{H2}", m.group(2)):
                    rep.err(p, f"{m.group(1)} covers no AC, EC, TH, or EV")
        if re.search(r"(^|/)04-build/.*-plan\.md$|^dev/maintenance/.*-plan\.md$", p):
            for need in ("Read map", "Reuse map", "budget"):
                if need.lower() not in d["text"].lower():
                    rep.warn(p, f"build plan has no {need}")


def check_gates(docs, rep):
    """Stories past ready-for-dev need the scope's approved test design (D05) and task file with its specification review (D03)."""
    scopes = {str(s["id"]): (ini, s.get("na") or {}) for ini, s in docs.scopes()}
    for i in docs.items:
        if i.get("type") != "story" or i.get("status") not in ("in_progress", "in_review", "in_qa", "done", "released"):
            continue
        sc = str(i.get("scope", ""))
        if sc not in scopes:
            continue
        ini, na = scopes[sc]
        for step, what in (("D05", "test design (dev-05)"), ("D03", "task file with its specification review (dev-03)")):
            if step in na:
                continue
            _, fm = docs.find(step, ini, sc)
            if not fm or fm.get("status") != "approved":
                rep.err("tracker.yaml", f"{i.get('id')}: '{i.get('status')}' but the scope's {what} is not approved")


def uncommitted(docs):
    try:
        out = subprocess.run(["git", "status", "--porcelain", "-uall", "--", "."], cwd=docs.root,
                             capture_output=True, text=True, timeout=20)
        if out.returncode != 0:
            return None
        top = subprocess.run(["git", "rev-parse", "--show-prefix"], cwd=docs.root,
                             capture_output=True, text=True, timeout=20).stdout.strip()
        res = []
        for line in out.stdout.splitlines():
            path = line[3:].strip().strip('"')
            if top and path.startswith(top):
                path = path[len(top):]
            if path.endswith(".md") and path != "tracker.md":
                res.append(path)
        return res
    except Exception:
        return None


def run_lint(docs, fix=False):
    rep = Report()
    if not docs.files and not os.path.exists(docs.tracker_path):
        rep.err(docs.root, "no docs found; is --root the product's docs path?")
        return rep, {}, 0
    if not os.path.exists(docs.tracker_path):
        rep.err("tracker.yaml", "missing (product-00-product-context creates it)")
    check_headers(docs, rep)
    stale = stale_map(docs, rep)
    for p, lst in stale.items():
        for path, pin, cur in lst:
            rep.warn(p, f"stale: built on {path}@{pin}, which is now {cur}")
    check_ids(docs, rep)
    changed, _ = check_levels(docs, rep, fix)
    check_citations(docs, rep)
    check_tracker_rules(docs, rep)
    check_ears(docs, rep)
    check_tests(docs, rep)
    check_gates(docs, rep)
    if fix and changed and not save_levels(docs, changed):
        rep.err("tracker.yaml", "could not write dependency levels in place; set them by hand: " +
                ", ".join(f"{k}={v}" for k, v in changed.items()))
    return rep, stale, len(changed)


def save_levels(docs, levels):
    """Write dep_level values into tracker.yaml in place, keeping its layout and comments."""
    with open(docs.tracker_path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    start = next((n for n, l in enumerate(lines) if re.match(r"^items:\s*(#.*)?$", l)), None)
    if start is None:
        return False
    end = next((n for n in range(start + 1, len(lines)) if re.match(r"^[A-Za-z_]", lines[n])), len(lines))
    for iid, lv in levels.items():
        done = False
        for n in range(start + 1, end):
            line = lines[n]
            flow = re.match(r"^(\s*-\s*)\{(.*)\}\s*$", line)
            if flow and re.search(r"(^|,)\s*id:\s*" + re.escape(iid) + r"\s*(,|$)", flow.group(2)):
                body = flow.group(2)
                if re.search(r"(^|,)\s*dep_level:", body):
                    body = re.sub(r"((?:^|,)\s*dep_level:\s*)[^,]*", lambda m: m.group(1) + str(lv), body)
                else:
                    body = body.rstrip() + f", dep_level: {lv}"
                lines[n] = f"{flow.group(1)}{{{body}}}"
                done = True
                break
            m = re.match(r"^(\s*)(-\s+)?id:\s*" + re.escape(iid) + r"\s*(#.*)?$", line)
            if m:
                key_ind = len(m.group(1)) + (len(m.group(2)) if m.group(2) else 0)
                k = n + 1
                while k < len(lines):
                    l2 = lines[k]
                    if l2.strip() and (len(l2) - len(l2.lstrip()) < key_ind or
                                       (len(l2) - len(l2.lstrip()) == key_ind - 2 and l2.lstrip().startswith("- "))):
                        break
                    if re.match(r"^\s{%d}dep_level:" % key_ind, l2):
                        lines[k] = " " * key_ind + f"dep_level: {lv}"
                        done = True
                        break
                    k += 1
                if not done:
                    lines.insert(n + 1, " " * key_ind + f"dep_level: {lv}")
                    end += 1
                    done = True
                break
        if not done:
            return False
    with open(docs.tracker_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return True


# ---------------------------------------------------------------- views


def cell(docs, stale, step, initiative=None, scope=None, na=None):
    if na and step in na:
        return f"n/a ({na[step]})"
    p, fm = docs.find(step, initiative, scope)
    if not fm:
        return "–"
    s = f"{fm.get('status')} {fm.get('doc_version')}"
    if p in stale:
        s = "stale " + str(fm.get("doc_version"))
    if fm.get("blocking"):
        s += f" ({len(fm['blocking'])} blocking)"
    return s


def scope_level(docs, scope, level):
    lv = [level.get(str(i.get("id")), 0) for i in docs.items
          if str(i.get("scope", "")) == scope and i.get("status") not in DONE_ROLES]
    if not lv:
        lv = [level.get(str(i.get("id")), 0) for i in docs.items
              if str(i.get("id", "")).startswith(scope) and i.get("type") == "feature"
              and i.get("status") not in DONE_ROLES]
    return min(lv) if lv else 0


def stories_of(docs, scope):
    return [i for i in docs.items if i.get("type") == "story" and str(i.get("scope", "")) == scope
            and i.get("status") != "removed"]


def compute_next(docs, team=None):
    level, _ = compute_levels(docs)
    stale = stale_map(docs)
    out = {t: [] for t in NEXT_TEAMS}
    P, G, D = out["product"], out["design"], out["dev"]
    Q, O, S = out["qa"], out["deploy"], out["security"]

    def ok(step, ini=None, scope=None):
        p, fm = docs.find(step, ini, scope)
        return bool(fm and fm.get("status") == "approved" and p not in stale)

    def exists(step, ini=None, scope=None):
        return docs.find(step, ini, scope)[1] is not None

    if not exists("P00"):
        P.append(("product-00-product-context", "product", "no product context yet"))
    for c in docs.tracker.get("change_requests") or []:
        if c.get("status") in ("draft", "approved"):
            P.append(("product-05-change-request", c.get("id"), f"CR is {c.get('status')}, not applied"))
    for q in docs.tracker.get("queries") or []:
        if q.get("status") == "open":
            who = q.get("to") if q.get("to") in NEXT_TEAMS else "product"
            out[who].append(("answer " + str(q.get("id")), ", ".join(map(str, q.get("about") or [])),
                             ("blocking " if q.get("blocking") else "") + "query: " + str(q.get("question", ""))[:80]))
    for p, lst in sorted(stale.items()):
        fm = docs.files[p]["fm"]
        step = str(fm.get("pdlc_step"))
        team_of = team_of_step(step)
        if step in SKILL and team_of in out:
            out[team_of].append((SKILL[step], f"{fm.get('initiative', '')} {fm.get('scope')}".strip(),
                                 f"update mode: {lst[0][0]} moved to {lst[0][2]}"))
    design = docs.design_stage()
    qa = docs.qa_stage()
    deploy = docs.deploy_stage()
    security = docs.security_stage()
    if design and not exists("G00"):
        G.append(("design-00-design-setup", "product", "design stage on, no setup file"))
    if design and exists("G00") and not exists("G04") and \
            str((docs.tracker.get("config") or {}).get("design_system", "")) == "planned":
        G.append(("design-04-design-system", "product", "design system planned, no audit or proposal yet"))
    if not exists("D00"):
        D.append(("dev-00-dev-setup", "product", "no dev setup yet"))
    if not docs.files.get("dev/architecture.md"):
        D.append(("dev-01-tech-design", "baseline", "no product-wide architecture yet"))
    if qa and not exists("Q00"):
        Q.append(("qa-00-qa-setup", "product", "QA stage on, no setup file"))
    if deploy and not exists("O00"):
        O.append(("deploy-00-deploy-setup", "product", "Deployment stage on, no setup file"))
    if security and not exists("S00"):
        S.append(("sec-00-engagement-scope", "product", "Security stage on, no engagement scoped yet"))

    for ini in docs.tracker["initiatives"]:
        if not isinstance(ini, dict) or ini.get("status") in DONE_ROLES:
            continue
        iid = str(ini.get("id"))
        if not exists("P02", iid):
            P.append(("product-02-prd" if exists("P01", iid) else "product-01-feature-brainstorm", iid,
                      "brainstorm done, PRD missing" if exists("P01", iid) else "new initiative"))
            continue
        if not ok("P02", iid):
            P.append(("product-02-prd", iid, "PRD not approved"))
            continue
        scopes = sorted((s for i2, s in docs.scopes() if i2 == iid),
                        key=lambda s: scope_level(docs, str(s["id"]), level))
        if not scopes:
            P.append(("product-03-ux-flows", iid, "no scopes recorded yet: pick the lowest-level scope"))
        handed = []
        for s in scopes:
            sid, na = str(s["id"]), s.get("na") or {}
            lv = scope_level(docs, sid, level)
            tag = f"{iid} / {sid} (level {lv})"
            if "P03" not in na and not ok("P03", iid, sid):
                P.append(("product-03-ux-flows", tag, "UX missing or not approved"))
                continue
            if not ok("P04", iid, sid):
                P.append(("product-04-user-stories", tag, "stories missing or not approved"))
                continue
            st = stories_of(docs, sid)
            ui = design and "P03" not in na
            if ui and any(x.get("status") == "in_design" for x in st):
                if not exists("G01", iid) and "G01" not in na:
                    G.append(("design-01-sitemap-flows", iid, "scopes waiting for design"))
                if not ok("G02", iid, sid):
                    G.append(("design-02-screen-mockups", tag, "stories in design"))
                elif not ok("G03", iid, sid):
                    G.append(("design-03-design-handoff", tag, "mockups done, handoff not approved"))
            if any(x.get("status") in HANDED_OFF_ROLES for x in st):
                handed.append((s, lv))
        if handed and not exists("D01", iid, iid):
            D.append(("dev-01-tech-design", iid, "handed-off scopes, no tech design for the initiative"))
            continue
        for s, lv in handed:
            sid, na = str(s["id"]), s.get("na") or {}
            tag = f"{iid} / {sid} (level {lv})"
            if "D02" not in na and not ok("D02", iid, sid):
                D.append(("dev-02-data-model", tag, "handed off, no approved data model"))
                continue
            if "D05" not in na and not exists("D05", iid, sid):
                D.append(("dev-05-test-qa", tag, "test design first: no test cases yet"))
                continue
            if "D05" not in na and not ok("D05", iid, sid):
                D.append(("dev-05-test-qa", tag, "test design not approved"))
                continue
            if not ok("D03", iid, sid):
                D.append(("dev-03-build-tasks", tag, "tasks and specification review not approved"))
                continue
            ready = [x for x in stories_of(docs, sid) if x.get("status") == "ready_for_dev" and
                     all((docs.item_index().get(str(d)) or {}).get("status") in DONE_ROLES
                         for d in x.get("depends_on") or [])]
            for x in sorted(ready, key=lambda x: level.get(str(x.get("id")), 0)):
                D.append(("dev-04-code-plan-build", str(x.get("id")),
                          f"ready for dev, dependencies done (level {level.get(str(x.get('id')), 0)})"))
            if any(x.get("status") == "in_qa" for x in stories_of(docs, sid)):
                if qa:
                    Q.append(("qa-02-test-execution", tag, "stories in QA (independent QA stage)"))
                else:
                    D.append(("dev-05-test-qa", tag, "stories in QA"))
            if qa and ok("P04", iid, sid) and not exists("Q01", iid, sid):
                Q.append(("qa-01-test-plan", tag, "stories approved; QA plan can start in parallel with build"))
    for i in docs.items:
        if i.get("type") in MAINT_TYPES and i.get("status") not in DONE_ROLES:
            D.append(("dev-07-maintenance" if i.get("status") in ("backlog",) else "dev-04-code-plan-build",
                      str(i.get("id")), f"{i.get('type')}: {i.get('title', '')}"))
        if i.get("type") == "bug" and i.get("status") not in DONE_ROLES | {"in_qa"}:
            D.append(("dev-04-code-plan-build", str(i.get("id")), f"bug: {i.get('title', '')}"))
    for v in docs.tracker.get("versions") or []:
        vid = str(v.get("id"))
        if v.get("status") in ("planned", "in_progress"):
            its = [i for i in docs.items if str(i.get("fix_version", "")) == vid]
            if its and all(i.get("status") in DONE_ROLES for i in its):
                if deploy:
                    O.append(("deploy-03-release", vid, "every item in the version is done; stage to pre-production"))
                else:
                    D.append(("dev-06-deploy", vid, "every item in the version is done"))
        if v.get("status") == "staged":
            if qa and not ok("Q03", None, vid) and not exists("Q03", None, vid):
                Q.append(("qa-03-release-signoff", vid, "version staged; release QA Go / No-go"))
            elif not qa:
                D.append(("dev-05-test-qa", vid, "version staged; developer version QA"))
            if security:
                S.append(("sec-05-retest-signoff", vid,
                          "Security stage on: confirm engagement sign-off before production promote"))
        if v.get("status") == "released":
            done = [i for i in docs.items if str(i.get("fix_version", "")) == vid
                    and i.get("type") == "story"]
            if done and not any(f.startswith("product/launch/") and vid in f for f in docs.files):
                P.append(("product-07-launch", vid, "released; no launch kit yet (if the team uses one)"))
    if team:
        return {team: out[team]}
    # Hide empty optional teams when their stage is off, keep product/dev always.
    if team is None:
        shown = {"product": out["product"], "design": out["design"], "dev": out["dev"]}
        if qa or out["qa"]:
            shown["qa"] = out["qa"]
        if deploy or out["deploy"]:
            shown["deploy"] = out["deploy"]
        if security or out["security"]:
            shown["security"] = out["security"]
        return shown
    return out


def render_next(nx):
    lines = []
    labels = {"product": "Product", "design": "Design", "dev": "Development",
              "qa": "QA", "deploy": "Deployment", "security": "Security"}
    for team, rows in nx.items():
        lines.append(f"### {labels.get(team, team.capitalize())}")
        if not rows:
            lines.append("Nothing waiting.")
        seen = set()
        for skill, scope, why in rows:
            if (skill, scope) in seen:
                continue
            seen.add((skill, scope))
            lines.append(f"- `{skill}` for {scope}: {why}")
        lines.append("")
    return "\n".join(lines)


def open_view(docs):
    rows = []
    for p, d in sorted(docs.chain_docs().items()):
        fm = d["fm"]
        n = fm.get("open_items") or 0
        if n:
            rows.append(f"| {p} | {fm.get('status')} {fm.get('doc_version')} | {n} | {', '.join(map(str, fm.get('blocking') or [])) or '–'} |")
    out = ["| File | Version | Open items | Blocking |", "|---|---|---|---|"] + (rows or ["| – | | | |"])
    out += ["", "| Query | Question | About | Raised by | Blocking | Status |", "|---|---|---|---|---|---|"]
    qs = [q for q in docs.tracker.get("queries") or [] if q.get("status") == "open"]
    for q in qs:
        out.append(f"| {q.get('id')} | {q.get('question', '')} | {', '.join(map(str, q.get('about') or []))} | "
                   f"{q.get('raised_by', '')} | {'yes' if q.get('blocking') else 'no'} | open |")
    if not qs:
        out.append("| – | | | | | |")
    return "\n".join(out)


def render_board(docs):
    rep, stale, _ = run_lint(docs)
    level, _ = compute_levels(docs)
    cfg = docs.tracker.get("config") or {}
    name = docs.tracker.get("product") or "product"
    o = []
    o.append("<!-- Generated by pdlc.py board from tracker.yaml and the file headers. Do not edit; edit tracker.yaml or the files. -->")
    o.append(f"# Tracker: {name}\n")
    stages = (f"design: {'on' if docs.design_stage() else 'off'} · "
              f"qa: {'on' if docs.qa_stage() else 'off'} · "
              f"deploy: {'on' if docs.deploy_stage() else 'off'} · "
              f"security: {'on' if docs.security_stage() else 'off'}")
    o.append(f"Generated {date.today().isoformat()} · lint: {len(rep.errors)} errors, {len(rep.warnings)} warnings · "
             f"{stages}\n")
    # 1 summary
    o.append("## 1. Summary")
    counts = {}
    for i in docs.items:
        if i.get("type") in ("module", "sub-module", "feature"):
            continue
        counts.setdefault(i.get("type"), {}).setdefault(i.get("status"), 0)
        counts[i.get("type")][i.get("status")] += 1
    tasks = [t for t in docs.tasks if "id" in t]
    for t in tasks:
        counts.setdefault("task", {}).setdefault(t.get("status"), 0)
        counts["task"][t.get("status")] += 1
    used = [r for r in ROLES if any(r in c for c in counts.values())]
    o.append("| Type | " + " | ".join(docs.status_name(r) for r in used) + " |")
    o.append("|---|" + "---|" * len(used))
    for typ, c in sorted(counts.items()):
        o.append(f"| {typ} | " + " | ".join(str(c.get(r, "")) for r in used) + " |")
    o.append("")
    # 2 initiative board
    o.append("## 2. Initiative board")
    o.append("| Initiative / scope | Level | P01 | P02 | G01 | D01 | P03 | P04 | G02 | G03 | Handoff | D02 | D03 | D04 | D05 | Released in |")
    o.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for ini in docs.tracker["initiatives"]:
        if not isinstance(ini, dict):
            continue
        iid = str(ini.get("id"))
        o.append(f"| **{iid} {ini.get('title', '')}** | | {cell(docs, stale, 'P01', iid)} | {cell(docs, stale, 'P02', iid)} | "
                 f"{cell(docs, stale, 'G01', iid) if docs.design_stage() else 'n/a'} | {cell(docs, stale, 'D01', iid, iid)} | | | | | | | | | | |")
        for s in ini.get("scopes") or []:
            sid, na = str(s.get("id")), s.get("na") or {}
            st = stories_of(docs, sid)
            built = sum(1 for x in st if x.get("status") in BUILT_ROLES)
            if any(x.get("status") in HANDED_OFF_ROLES for x in st):
                hand = f"handed off ({sum(1 for x in st if x.get('status') in HANDED_OFF_ROLES)}/{len(st)})"
            elif any(x.get("status") == "in_design" for x in st):
                hand = "in design"
            else:
                hand = "–"
            qa_p, qa = docs.find("D05", iid, sid)
            qa_cell = (str(qa.get("result")) if qa and qa.get("result") else cell(docs, stale, "D05", iid, sid, na))
            rel = sorted({str(x.get("fix_version")) for x in st if x.get("status") == "released" and x.get("fix_version")})
            g = (lambda step: cell(docs, stale, step, iid, sid, na)) if docs.design_stage() else (lambda step: "n/a")
            o.append(f"| {sid} | {scope_level(docs, sid, level)} | | | | | {cell(docs, stale, 'P03', iid, sid, na)} | "
                     f"{cell(docs, stale, 'P04', iid, sid, na)} | {g('G02')} | {g('G03')} | {hand} | "
                     f"{cell(docs, stale, 'D02', iid, sid, na)} | {cell(docs, stale, 'D03', iid, sid, na)} | "
                     f"{built}/{len(st)} built | {qa_cell} | {', '.join(rel) or '–'} |")
    o.append("")
    o.append("## 3. What next\n")
    o.append(render_next(compute_next(docs)))
    o.append("## 4. Open items and queries\n")
    o.append(open_view(docs))
    o.append("")
    o.append("## 5. Blocked\n")
    blocked = [i for i in docs.items if i.get("status") == "blocked"]
    o.append("\n".join(f"- {i.get('id')} {i.get('title', '')}" for i in blocked) or "Nothing blocked.")
    o.append("")
    o.append("## 6. Stale files and lint findings\n")
    for p, lst in sorted(stale.items()):
        for path, pin, cur in lst:
            o.append(f"- stale: `{p}` built on `{path}@{pin}`, now {cur}")
    nc = uncommitted(docs)
    for p in nc or []:
        o.append(f"- not committed: `{p}`")
    for w, m in rep.errors:
        o.append(f"- error: `{w}`: {m}")
    if not stale and not rep.errors and not nc:
        o.append("None.")
    o.append("")
    o.append("## 7. Items by dependency level\n")
    o.append("| Level | ID | Type | Title | Status | Depends on | Fix version | Tasks done |")
    o.append("|---|---|---|---|---|---|---|---|")
    open_items = [i for i in docs.items if i.get("type") not in ("module", "sub-module", "feature", "initiative")
                  and i.get("status") not in DONE_ROLES]
    for i in sorted(open_items, key=lambda i: (level.get(str(i.get("id")), 0), str(i.get("id")))):
        tk = [t for t in tasks if str(t.get("id", "")).startswith(str(i.get("id")) + "-T")]
        td = f"{sum(1 for t in tk if t.get('status') in DONE_ROLES)}/{len(tk)}" if tk else "–"
        o.append(f"| {level.get(str(i.get('id')), 0)} | {i.get('id')} | {i.get('type')} | {i.get('title', '')} | "
                 f"{docs.status_name(i.get('status'))} | {', '.join(map(str, i.get('depends_on') or [])) or '–'} | "
                 f"{i.get('fix_version') or '–'} | {td} |")
    o.append("")
    o.append("## 8. Versions\n")
    o.append("| Version | Goal | Status | Items | Done | File |")
    o.append("|---|---|---|---|---|---|")
    for v in docs.tracker.get("versions") or []:
        its = [i for i in docs.items if str(i.get("fix_version", "")) == str(v.get("id"))]
        o.append(f"| {v.get('id')} | {v.get('goal', '')} | {v.get('status')} | {len(its)} | "
                 f"{sum(1 for i in its if i.get('status') in DONE_ROLES)} | {v.get('file') or '–'} |")
    o.append("")
    o.append("## 9. Change requests\n")
    o.append("| CR | Title | Initiative | Status | File |")
    o.append("|---|---|---|---|---|")
    for c in docs.tracker.get("change_requests") or []:
        o.append(f"| {c.get('id')} | {c.get('title', '')} | {c.get('initiative', '')} | {c.get('status')} | {c.get('file') or '–'} |")
    o.append("")
    return "\n".join(o)

# ---------------------------------------------------------------- new-id

NEWID = {
    "initiative": (None, "I-", 3), "module": (None, "M", 2), "bug": (None, "BUG-", 3),
    "query": (None, "Q-", 3), "cr": (None, "CR-", 3), "dec": (None, "DEC-", 3),
    "hf": (None, "HF-", 3), "td": (None, "TD-", 3), "upg": (None, "UPG-", 3),
    "spk": (None, "SPK-", 3), "chr": (None, "CHR-", 3),
    "sub-module": ("module", ".S", 2), "feature": ("sub-module", ".F", 2),
    "story": ("feature", "-US", 2), "task": ("story", "-T", 2), "subtask": ("task", "-ST", 2),
    "fr": ("feature", "-FR", 2), "br": ("feature", "-BR", 2), "ec": ("feature", "-EC", 2),
    "ac": ("story", "-AC", 2), "ev": ("feature", "-EV", 2), "tc": ("story", "-TC", 2), "sc": ("scope", "-SC", 2),
    "fl": ("scope", "-FL", 2), "nfr": ("initiative", "-NFR", 2),
}


def new_id(docs, kind, parent=None):
    if kind not in NEWID:
        raise SystemExit(f"unknown kind '{kind}'. Kinds: {', '.join(NEWID)}")
    ptype, sep, width = NEWID[kind]
    if ptype and not parent:
        raise SystemExit(f"'{kind}' needs a parent ({ptype} ID)")
    base = (parent or "") + sep
    corpus = "\n".join(d["text"] for d in docs.files.values())
    if os.path.exists(docs.tracker_path):
        with open(docs.tracker_path, encoding="utf-8") as f:
            corpus += "\n" + f.read()
    nums = [int(n) for n in re.findall(re.escape(base) + r"(\d+)(?![\d.])", corpus)]
    if kind == "dec":
        nums += [int(m) for f in docs.files for m in re.findall(r"^decisions/DEC-(\d+)", f)]
    return f"{base}{(max(nums) + 1 if nums else 1):0{width}d}"

# ---------------------------------------------------------------- main


def find_root(arg):
    if arg:
        return arg
    for cand in ("docs/pdlc", "."):
        if os.path.exists(os.path.join(cand, "tracker.yaml")):
            return cand
    return "docs/pdlc"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pdlc.py", description=__doc__.split("\n")[0])
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd")
    for name in ("lint", "board", "next", "new-id", "open"):
        sp = sub.add_parser(name)
        sp.add_argument("--root", help="the product's docs path (default: docs/pdlc)")
        if name == "lint":
            sp.add_argument("--fix", action="store_true", help="write computed dependency levels")
            sp.add_argument("--strict", action="store_true", help="treat warnings as errors")
        if name == "next":
            sp.add_argument("--team", choices=list(NEXT_TEAMS))
        if name == "new-id":
            sp.add_argument("kind")
            sp.add_argument("parent", nargs="?")
    a = ap.parse_args(argv)
    if not a.cmd:
        ap.print_help()
        return 2
    docs = Docs(find_root(a.root))
    if a.cmd == "lint":
        rep, stale, changed = run_lint(docs, fix=a.fix)
        for w, m in rep.errors:
            print(f"ERROR   {w}: {m}")
        for w, m in rep.warnings:
            print(f"warning {w}: {m}")
        nc = uncommitted(docs)
        for p in nc or []:
            print(f"warning {p}: not committed")
        if changed:
            print(f"fixed   tracker.yaml: {changed} dependency levels updated")
        print(f"pdlc lint {VERSION}: {len(rep.errors)} errors, {len(rep.warnings)} warnings, "
              f"{len(docs.chain_docs())} files, {len(docs.items)} items, {len(docs.tasks)} tasks")
        return 1 if rep.errors or (a.strict and rep.warnings) else 0
    if a.cmd == "board":
        text = render_board(docs)
        with open(os.path.join(docs.root, "tracker.md"), "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"wrote {os.path.join(docs.root, 'tracker.md')}")
        return 0
    if a.cmd == "next":
        print(render_next(compute_next(docs, a.team)))
        return 0
    if a.cmd == "open":
        print(open_view(docs))
        return 0
    if a.cmd == "new-id":
        print(new_id(docs, a.kind, a.parent))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
