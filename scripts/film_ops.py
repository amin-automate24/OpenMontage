#!/usr/bin/env python3
"""film_ops — safe, reversible helpers for a film project (complements film_studio.py).

Never overwrites: new files get a numbered suffix; edited CSVs are backed up first
to <project>/_backups/<date>/. Read-only commands: status, ledger show.

  film_ops.py contact-sheet OUT.jpg IMG... [--cols 2]
  film_ops.py ledger add --tool Magnific --credits 855 --item "S1-02 video" [--balance N] [--note ..]
  film_ops.py ledger show
  film_ops.py shot set S1-02 --status VALIDE [--video ID] [--cost N] [--note ..]
  film_ops.py status [--write]        (--write: PRODUCTION_STATUS_AUTO.md)
  film_ops.py queue show | approve --cap N   (grouped director approval)
  film_ops.py guard S1-04 video --est 855     (refuses duplicates/unapproved/over budget)
  film_ops.py check                           (consistency lint of the CSVs)
  film_ops.py backup FILE...
  film_ops.py sync "commit message"
"""
from __future__ import annotations
import argparse, csv, datetime as dt, shutil, subprocess, sys, time
from pathlib import Path

DEFAULT_PROJECT = Path(__file__).resolve().parents[1] / "films" / "LE_SECRET_BOITE_FER_BLANC"
TRAILER = ("Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\n"
           "Claude-Session: https://claude.ai/code/session_01TVkBnsL678GGwzqRjwJut7")


def versioned(path: Path) -> Path:
    """Return path, or path with _v2/_v3... if it already exists (never overwrite)."""
    if not path.exists():
        return path
    n = 2
    while path.with_name(f"{path.stem}_v{n}{path.suffix}").exists():
        n += 1
    return path.with_name(f"{path.stem}_v{n}{path.suffix}")


def backup(project: Path, files) -> list[Path]:
    out = []
    day = project / "_backups" / dt.date.today().isoformat()
    day.mkdir(parents=True, exist_ok=True)
    for f in files:
        f = Path(f)
        dest = versioned(day / f.name)
        shutil.copy2(f, dest)
        out.append(dest)
    return out


def contact_sheet(out: Path, images, cols=2, cell=(1024, 573)) -> Path:
    from PIL import Image, ImageDraw
    rows = -(-len(images) // cols)
    sheet = Image.new("RGB", (cols * (cell[0] + 10) + 10, rows * (cell[1] + 10) + 10), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, p in enumerate(images):
        im = Image.open(p).convert("RGB").resize(cell)
        x, y = 10 + (i % cols) * (cell[0] + 10), 10 + (i // cols) * (cell[1] + 10)
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 50, y + 50], fill=(0, 0, 0))
        d.text((x + 18, y + 16), str(i + 1), fill=(255, 255, 255))
    dest = versioned(out)
    sheet.save(dest, quality=88)
    return dest


def read_csv(p: Path):
    with open(p, newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def write_csv(p: Path, fields, rows):
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    tmp.replace(p)


def balances(rows, tool="Magnific"):
    """Chain balance: use balance_after when given, else subtract spend."""
    bal = None
    for r in rows:
        if r["tool"] != tool:
            continue
        spent = float(r["credits_spent"] or 0)
        if r["balance_after"].strip():
            bal = float(r["balance_after"])
        elif bal is not None:
            bal -= spent
    return bal


def ledger_add(project, tool, credits, item, balance=None, note=""):
    p = project / "BUDGET.csv"
    fields, rows = read_csv(p)
    backup(project, [p])
    prev = balances(rows, tool)
    if balance is None and prev is not None and tool == "Magnific":
        balance = prev - credits
    rows.append({"date": dt.date.today().isoformat(), "item": item, "tool": tool,
                 "credits_spent": str(credits), "balance_after": "" if balance is None else f"{balance:g}",
                 "note": note})
    write_csv(p, fields, rows)
    return balance


def shot_set(project, shot, **kw):
    p = project / "SHOT_LIST.csv"
    fields, rows = read_csv(p)
    for r in rows:
        if r["shot"] == shot:
            backup(project, [p])
            for k, v in kw.items():
                if v is not None:
                    r[k] = str(v)
            write_csv(p, fields, rows)
            return r
    raise SystemExit(f"unknown shot {shot}")


def status(project) -> str:
    _, shots = read_csv(project / "SHOT_LIST.csv")
    _, bud = read_csv(project / "BUDGET.csv")
    counts = {}
    for s in shots:
        counts[s["status"]] = counts.get(s["status"], 0) + 1
    spent = sum(float(r["credits_spent"] or 0) for r in bud if r["tool"] == "Magnific")
    return (f"shots: {counts}\nMagnific spent (ledger): {spent:g} | balance (chained): {balances(bud)}\n"
            f"pending decisions: {[s['shot'] for s in shots if s['status'].startswith('EN_ATTENTE')]}")


ALLOWED_STATUS = {"A_FAIRE", "EN_COURS", "EN_ATTENTE", "EN_ATTENTE_DECISION", "VALIDE", "VALIDE_PLAN_LARGE", "REFUSE"}


def queue_rows(project):
    p = project / "QUEUE.csv"
    return read_csv(p) if p.exists() else (["id", "shot", "kind", "model", "est_credits", "approved", "status"], [])


def queue_show(project):
    _, rows = queue_rows(project)
    pend = [r for r in rows if r["status"] == "PENDING"]
    tot = sum(float(r["est_credits"]) for r in pend)
    app = sum(float(r["est_credits"]) for r in pend if r["approved"] == "1")
    return f"pending: {len(pend)} items | estimated {tot:g} cr | approved {app:g} cr | balance {balances(read_csv(project / 'BUDGET.csv')[1])}"


def queue_approve(project, cap):
    """Approve pending items in order until the cumulative estimate reaches cap (director's grouped approval)."""
    fields, rows = queue_rows(project)
    backup(project, [project / "QUEUE.csv"])
    run = 0.0
    for r in rows:
        if r["status"] == "PENDING" and r["approved"] != "1":
            if run + float(r["est_credits"]) > cap:
                break
            r["approved"] = "1"; run += float(r["est_credits"])
    write_csv(project / "QUEUE.csv", fields, rows)
    return run


def guard(project, shot, kind, est):
    """Duplicate / budget / approval check BEFORE any paid generation. Returns (ok, reason)."""
    _, shots = read_csv(project / "SHOT_LIST.csv")
    row = next((r for r in shots if r["shot"] == shot), None)
    if row is None:
        return False, f"unknown shot {shot}"
    if kind == "video" and row["status"].startswith("VALIDE"):
        return False, f"{shot} already validated ({row['video']}): no regeneration without explicit reason"
    bal = balances(read_csv(project / "BUDGET.csv")[1])
    if bal is not None and est > bal:
        return False, f"estimate {est:g} exceeds balance {bal:g}"
    _, q = queue_rows(project)
    item = next((r for r in q if r["shot"] == shot and r["kind"] == kind and r["status"] == "PENDING"), None)
    if item is None:
        return False, f"{shot}/{kind} not in QUEUE.csv"
    if item["approved"] != "1":
        return False, f"{shot}/{kind} not approved by the director"
    return True, "ok"


def check(project):
    problems = []
    _, assets = read_csv(project / "ASSET_REGISTER.csv")
    ids = [a["id"] for a in assets]
    problems += [f"duplicate asset id {i}" for i in set(ids) if ids.count(i) > 1]
    mg = {a["magnific_id"] for a in assets if a["magnific_id"]}
    _, shots = read_csv(project / "SHOT_LIST.csv")
    for s in shots:
        if s["status"] not in ALLOWED_STATUS:
            problems.append(f"{s['shot']}: unknown status {s['status']}")
        v = s["video"].split(" ")[0]
        if v and v != "a" and v not in mg:
            problems.append(f"{s['shot']}: video {v} missing from ASSET_REGISTER")
    _, bud = read_csv(project / "BUDGET.csv")
    for r in bud:
        try:
            float(r["credits_spent"])
        except ValueError:
            problems.append(f"budget row not numeric: {r['item']}")
    return problems


def status_write(project):
    p = project / "PRODUCTION_STATUS_AUTO.md"
    if p.exists():
        backup(project, [p])
    p.write_text("# PRODUCTION_STATUS_AUTO (genere par film_ops status --write, ne pas editer)\n\n```\n"
                 + status(project) + "\n```\n\n" + queue_show(project) + "\n")
    return p


def sync(root: Path, message: str):
    def run(*a):
        return subprocess.run(a, cwd=root, capture_output=True, text=True)
    run("git", "add", "-A", "films")
    if run("git", "diff", "--cached", "--quiet").returncode == 0:
        return "nothing to commit"
    c = run("git", "commit", "-m", message, "-m", TRAILER)
    if c.returncode:
        raise SystemExit(c.stderr)
    branch = run("git", "branch", "--show-current").stdout.strip()
    for wait in (0, 2, 4, 8, 16):
        time.sleep(wait)
        if run("git", "push", "-u", "origin", branch).returncode == 0:
            return f"pushed {branch}"
    raise SystemExit("push failed after retries")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("contact-sheet"); c.add_argument("out", type=Path); c.add_argument("images", nargs="+"); c.add_argument("--cols", type=int, default=2)
    l = sub.add_parser("ledger"); ls = l.add_subparsers(dest="sub", required=True)
    la = ls.add_parser("add"); la.add_argument("--tool", required=True); la.add_argument("--credits", type=float, required=True); la.add_argument("--item", required=True); la.add_argument("--balance", type=float); la.add_argument("--note", default="")
    ls.add_parser("show")
    s = sub.add_parser("shot"); ss = s.add_subparsers(dest="sub", required=True)
    st = ss.add_parser("set"); st.add_argument("shot"); st.add_argument("--status"); st.add_argument("--video"); st.add_argument("--cost"); st.add_argument("--notes")
    sw = sub.add_parser("status"); sw.add_argument("--write", action="store_true")
    q = sub.add_parser("queue"); qs = q.add_subparsers(dest="sub", required=True); qs.add_parser("show"); qa = qs.add_parser("approve"); qa.add_argument("--cap", type=float, required=True)
    g = sub.add_parser("guard"); g.add_argument("shot"); g.add_argument("kind", choices=["image", "video"]); g.add_argument("--est", type=float, required=True)
    sub.add_parser("check")
    b = sub.add_parser("backup"); b.add_argument("files", nargs="+")
    y = sub.add_parser("sync"); y.add_argument("message")
    a = ap.parse_args(argv)
    if a.cmd == "contact-sheet":
        print(contact_sheet(a.out, a.images, a.cols))
    elif a.cmd == "ledger" and a.sub == "add":
        print("balance:", ledger_add(a.project, a.tool, a.credits, a.item, a.balance, a.note))
    elif a.cmd == "ledger":
        print((a.project / "BUDGET.csv").read_text())
    elif a.cmd == "shot":
        print(shot_set(a.project, a.shot, status=a.status, video=a.video, cost_credits=a.cost, notes=a.notes))
    elif a.cmd == "status":
        print(status_write(a.project) if a.write else status(a.project))
    elif a.cmd == "queue":
        print(queue_show(a.project) if a.sub == "show" else f"approved {queue_approve(a.project, a.cap):g} cr")
    elif a.cmd == "guard":
        ok, why = guard(a.project, a.shot, a.kind, a.est); print(("OK" if ok else "REFUSED") + ": " + why); sys.exit(0 if ok else 2)
    elif a.cmd == "check":
        pr = check(a.project); print("\n".join(pr) or "no problems"); sys.exit(1 if pr else 0)
    elif a.cmd == "backup":
        print(*backup(a.project, a.files), sep="\n")
    elif a.cmd == "sync":
        print(sync(a.project.parents[1], a.message))


if __name__ == "__main__":
    main()
