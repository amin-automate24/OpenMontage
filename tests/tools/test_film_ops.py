import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("film_ops", Path(__file__).resolve().parents[2] / "scripts" / "film_ops.py")
fo = importlib.util.module_from_spec(spec); sys.modules["film_ops"] = fo; spec.loader.exec_module(fo)


def proj(tmp_path):
    (tmp_path / "BUDGET.csv").write_text("date,item,tool,credits_spent,balance_after,note\n2026-11-05,a,Magnific,100,1000,\n")
    (tmp_path / "SHOT_LIST.csv").write_text("shot,status,video,cost_credits,notes\nS1-01,A_FAIRE,,0,\nS1-02,EN_ATTENTE_DECISION,,0,\n")
    return tmp_path


def test_versioned_never_overwrites(tmp_path):
    f = tmp_path / "a.txt"; f.write_text("x")
    assert fo.versioned(f).name == "a_v2.txt"


def test_ledger_chain_and_backup(tmp_path):
    p = proj(tmp_path)
    assert fo.ledger_add(p, "Magnific", 855, "video") == 145
    assert list((p / "_backups").rglob("BUDGET.csv"))
    assert fo.balances(fo.read_csv(p / "BUDGET.csv")[1]) == 145


def test_shot_set_and_status(tmp_path):
    p = proj(tmp_path)
    fo.shot_set(p, "S1-02", status="VALIDE", video="abc")
    assert "S1-02" not in fo.status(p).split("pending decisions:")[1]
    assert list((p / "_backups").rglob("SHOT_LIST.csv"))


def test_contact_sheet_versions(tmp_path):
    from PIL import Image
    im = tmp_path / "i.jpg"; Image.new("RGB", (100, 60), "red").save(im)
    a = fo.contact_sheet(tmp_path / "s.jpg", [im, im, im])
    b = fo.contact_sheet(tmp_path / "s.jpg", [im])
    assert a.name == "s.jpg" and b.name == "s_v2.jpg"


def proj2(tmp_path):
    p = proj(tmp_path)
    (p / "SHOT_LIST.csv").write_text("shot,status,video,cost_credits,notes\nS1-01,VALIDE,abc,0,\nS1-04,A_FAIRE,,0,\n")
    (p / "ASSET_REGISTER.csv").write_text("id,type,name,status,magnific_id,midjourney_image_id,notes\nV1,video,x,VALIDE,abc,,\n")
    (p / "QUEUE.csv").write_text("id,shot,kind,model,est_credits,approved,status\nQ1,S1-04,video,kling,855,0,PENDING\n")
    return p


def test_guard_blocks_unapproved_duplicate_and_budget(tmp_path):
    p = proj2(tmp_path)
    assert fo.guard(p, "S1-01", "video", 855)[0] is False       # already validated
    assert fo.guard(p, "S1-04", "video", 855)[0] is False       # not approved
    fo.queue_approve(p, 10000)
    assert fo.guard(p, "S1-04", "video", 1500)[0] is False      # over balance (1000)
    assert fo.guard(p, "S1-04", "video", 500)[0] is True


def test_queue_cap_and_check(tmp_path):
    p = proj2(tmp_path)
    assert fo.queue_approve(p, 100) == 0
    assert fo.check(p) == []
    assert fo.status_write(p).name == "PRODUCTION_STATUS_AUTO.md"


def test_malformed_csv_is_detected(tmp_path):
    import pytest
    (tmp_path / "x.csv").write_text("a,b\n1,2,3\n")
    with pytest.raises(SystemExit):
        fo.read_csv(tmp_path / "x.csv")


def test_queue_done(tmp_path):
    p = proj2(tmp_path)
    assert fo.queue_done(p, "S1-04", "video") == 1
    assert fo.queue_done(p, "S1-04", "video") == 0
