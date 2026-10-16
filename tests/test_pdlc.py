"""Tests for tools/pdlc.py against the sample product. Run: python -m unittest discover tests"""
import os, re, shutil, sys, tempfile, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import pdlc  # noqa: E402

SAMPLE = os.path.join(HERE, "..", "examples", "sample-product", "docs", "pdlc")


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, "pdlc")
        shutil.copytree(SAMPLE, self.root)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def edit(self, rel, old, new):
        p = os.path.join(self.root, rel)
        t = open(p).read()
        self.assertIn(old, t, f"{old!r} not in {rel}")
        open(p, "w").write(t.replace(old, new, 1))

    def lint(self):
        rep, stale, _ = pdlc.run_lint(pdlc.Docs(self.root))
        return [m for _, m in rep.errors], [m for _, m in rep.warnings], stale


TR = "tracker.yaml"
STORIES = "product/I-001-bulk-invoicing/04-stories/M01.S02-bulk-actions.md"
PRD = "product/I-001-bulk-invoicing/02-prd.md"
QA = "dev/I-001-bulk-invoicing/05-qa/M01.S02-bulk-actions.md"
TASKS = "dev/I-001-bulk-invoicing/03-tasks/M01.S02-bulk-actions.md"


class TestLint(Base):
    def test_sample_is_clean(self):
        e, w, s = self.lint()
        self.assertEqual(e, [])
        self.assertEqual(s, {})

    def test_cycle(self):
        self.edit(TR, "depends_on: []\n    dep_level: 0", "depends_on: [M01.S02.F01-US02]\n    dep_level: 0")
        e, _, _ = self.lint()
        self.assertTrue(any(m.startswith("cycle:") for m in e), e)

    def test_stale_on_minor_bump(self):
        self.edit(PRD, "doc_version: 1.2.0", "doc_version: 1.3.0")
        _, w, s = self.lint()
        self.assertIn("product/I-001-bulk-invoicing/03-ux/M01.S02-bulk-actions.md", s)
        self.assertTrue(any("stale" in m for m in w))

    def test_patch_bump_not_stale(self):
        self.edit(PRD, "doc_version: 1.2.0", "doc_version: 1.2.1")
        _, _, s = self.lint()
        self.assertEqual(s, {})

    def test_pin_ahead_is_error(self):
        self.edit(PRD, "doc_version: 1.2.0", "doc_version: 1.1.0")
        e, _, _ = self.lint()
        self.assertTrue(any("pins" in m for m in e), e)

    def test_unknown_citation(self):
        self.edit(STORIES, "Implements M01.S02.F01-FR02,", "Implements M01.S02.F01-FR09,")
        e, _, _ = self.lint()
        self.assertTrue(any("M01.S02.F01-FR09" in m for m in e), e)

    def test_unknown_dec(self):
        self.edit("dev/architecture.md", "DEC-001", "DEC-007")
        e, _, _ = self.lint()
        self.assertTrue(any("DEC-007" in m for m in e), e)

    def test_ready_needs_approved_stories(self):
        self.edit(STORIES, "status: approved", "status: draft")
        e, _, _ = self.lint()
        self.assertTrue(any("stories file is not approved" in m for m in e), e)

    def test_design_refs_required(self):
        self.edit(STORIES, "· approved\n<!-- design-refs:end -->\n## 8", "· stale\n<!-- design-refs:end -->\n## 8")
        e, _, _ = self.lint()
        self.assertTrue(any("stale or not yet designed" in m for m in e), e)

    def test_g03_required(self):
        self.edit("design/I-001-bulk-invoicing/03-handoff/M01.S02-bulk-actions.md", "status: approved", "status: draft")
        e, _, _ = self.lint()
        self.assertTrue(any("G03" in m for m in e), e)

    def test_duplicate_id(self):
        self.edit(TR, "{id: TD-001,", "{id: M01.S02.F01, type: feature, parent: M01.S02, title: dup, status: backlog}\n  - {id: TD-001,")
        e, _, _ = self.lint()
        self.assertTrue(any("duplicate" in m for m in e), e)

    def test_bad_header(self):
        self.edit("dev/00-dev-setup.md", "doc_version: 1.0.0", "doc_version: one")
        e, _, _ = self.lint()
        self.assertTrue(any("doc_version" in m for m in e), e)

    def test_unknown_dependency(self):
        self.edit(TR, "depends_on: [M01.S02.F01-US01]", "depends_on: [M01.S02.F01-US09]")
        e, _, _ = self.lint()
        self.assertTrue(any("US09" in m for m in e), e)

    def test_blocking_query_warns(self):
        self.edit(TR, "blocking: false\n    status: answered", "blocking: true\n    status: open")
        _, w, _ = self.lint()
        self.assertTrue(any("not blocked" in m for m in w), w)

    def test_task_under_unknown_story(self):
        self.edit("dev/I-001-bulk-invoicing/03-tasks/M01.S02-bulk-actions.md", "M01.S02.F01-US01-T01\n  title", "M01.S02.F01-US07-T01\n  title")
        e, _, _ = self.lint()
        self.assertTrue(any("US07" in m for m in e), e)

    def test_ears_required(self):
        self.edit(PRD, "When the account owner confirms a bulk send, the product shall send", "The account owner can send")
        e, _, _ = self.lint()
        self.assertTrue(any("FR02 is not an EARS sentence" in m for m in e), e)

    def test_ears_vague_word_warns(self):
        self.edit(PRD, "shall send every selected invoice", "shall send every selected invoice as appropriate")
        _, w, _ = self.lint()
        self.assertTrue(any("vague" in m for m in w), w)

    def test_test_case_must_cover_something(self):
        self.edit(QA, "| M01.S02.F01-US02-TC01 | M01.S02.F01-US02-AC01 |", "| M01.S02.F01-US02-TC01 | general check |")
        e, _, _ = self.lint()
        self.assertTrue(any("TC01 covers no AC" in m for m in e), e)

    def test_build_needs_test_design(self):
        self.edit(QA, "status: approved", "status: draft")
        e, _, _ = self.lint()
        self.assertTrue(any("test design (dev-05) is not approved" in m for m in e), e)

    def test_build_needs_spec_review(self):
        self.edit(TASKS, "status: approved", "status: draft")
        e, _, _ = self.lint()
        self.assertTrue(any("specification review" in m for m in e), e)

    def test_plan_without_maps_warns(self):
        p = os.path.join(self.root, "dev/I-001-bulk-invoicing/04-build/M01.S02.F01-US02-plan.md")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write("---\npdlc_step: \"D04\"\ninitiative: I-001\nscope: M01.S02.F01-US02\ndoc_version: 1.0.0\n"
                           "status: draft\ndepends_on: []\nupdated: 2026-10-09\n---\n# Plan\n## Change log\n")
        _, w, _ = self.lint()
        self.assertTrue(any("no Reuse map" in m for m in w), w)


class TestLevelsNextIds(Base):
    def test_levels(self):
        level, cycles = pdlc.compute_levels(pdlc.Docs(self.root))
        self.assertEqual(cycles, [])
        self.assertEqual(level["M01.S02.F01-US02"], 1)
        self.assertEqual(level["M01.S02.F01-US01"], 0)

    def test_done_dependency_lowers_level(self):
        self.edit(TR, "status: in_review", "status: done")
        level, _ = pdlc.compute_levels(pdlc.Docs(self.root))
        self.assertEqual(level["M01.S02.F01-US02"], 0)
        nx = pdlc.compute_next(pdlc.Docs(self.root), "dev")["dev"]
        self.assertIn(("dev-04-code-plan-build", "M01.S02.F01-US02"), [(a, b) for a, b, _ in nx])

    def test_next_test_design_before_tasks(self):
        os.remove(os.path.join(self.root, QA))
        self.edit(TASKS, "dev/I-001-bulk-invoicing/05-qa/M01.S02-bulk-actions.md@1.0.0", "")
        self.edit(TR, "status: in_review", "status: ready_for_dev")
        nx = pdlc.compute_next(pdlc.Docs(self.root), "dev")["dev"]
        self.assertEqual(nx[0][0], "dev-05-test-qa", nx)

    def test_next_product_when_stories_draft(self):
        self.edit(STORIES, "status: approved", "status: draft")
        nx = pdlc.compute_next(pdlc.Docs(self.root), "product")["product"]
        self.assertTrue(any(s == "product-04-user-stories" for s, _, _ in nx), nx)

    def test_new_ids(self):
        d = pdlc.Docs(self.root)
        self.assertEqual(pdlc.new_id(d, "story", "M01.S02.F01"), "M01.S02.F01-US03")
        self.assertEqual(pdlc.new_id(d, "ec", "M01.S02.F01"), "M01.S02.F01-EC02")
        self.assertEqual(pdlc.new_id(d, "dec"), "DEC-002")
        self.assertEqual(pdlc.new_id(d, "module"), "M02")
        self.assertEqual(pdlc.new_id(d, "sub-module", "M01"), "M01.S03")

    def test_board_renders(self):
        text = pdlc.render_board(pdlc.Docs(self.root))
        self.assertIn("## 2. Initiative board", text)
        self.assertIn("n/a (no data change)", text)
        self.assertIn("1/2 built", text)

    def test_fix_writes_levels_in_place(self):
        before = open(os.path.join(self.root, TR)).read()
        self.edit(TR, "dep_level: 1", "dep_level: 5")
        d = pdlc.Docs(self.root)
        pdlc.run_lint(d, fix=True)
        after = open(os.path.join(self.root, TR)).read()
        self.assertIn("# tracker.yaml", after)
        self.assertIn("dep_level: 1", after)
        e, w, _ = self.lint()
        self.assertEqual(e, [])
        self.assertFalse(any("dep_level" in m for m in w), w)
        self.assertIn("{id: TD-001,", after)


class TestMiniYaml(unittest.TestCase):
    def test_matches_pyyaml(self):
        if not pdlc._yaml:
            self.skipTest("PyYAML not installed")
        texts = [open(os.path.join(SAMPLE, "tracker.yaml")).read()]
        for dp, _, fns in os.walk(SAMPLE):
            for fn in fns:
                if fn.endswith(".md") and fn != "tracker.md":
                    t = open(os.path.join(dp, fn)).read()
                    m = re.match(r"^---\s*\n(.*?)\n---", t, re.S)
                    if m:
                        texts.append(m.group(1))
                    for blk in re.findall(r"```ya?ml pdlc-tasks\s*\n(.*?)```", t, re.S):
                        texts.append(blk)
        norm = lambda o: {k: norm(v) for k, v in o.items()} if isinstance(o, dict) else \
            [norm(v) for v in o] if isinstance(o, list) else (o.isoformat() if hasattr(o, "isoformat") else o)
        for t in texts:
            self.assertEqual(pdlc._mini_load(t), norm(pdlc._yaml.safe_load(t)), t[:80])

    def test_dump_roundtrip(self):
        data = pdlc._mini_load(open(os.path.join(SAMPLE, "tracker.yaml")).read())
        self.assertEqual(pdlc._mini_load(pdlc.ydump(data)), data)


if __name__ == "__main__":
    unittest.main()
