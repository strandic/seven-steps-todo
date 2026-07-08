"""Runnable checks for todo.py — `python3 test_todo.py` (no pytest needed)."""
import tempfile
from pathlib import Path

import todo


def test_add_and_id_increment():
    tasks = []
    t1 = todo.add(tasks, "first")
    t2 = todo.add(tasks, "second")
    assert (t1.id, t2.id) == (1, 2)
    assert [t.text for t in tasks] == ["first", "second"]


def test_done_and_missing():
    tasks = []
    todo.add(tasks, "x")
    todo.mark_done(tasks, 1)
    assert tasks[0].done is True
    try:
        todo.mark_done(tasks, 99)
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError for a missing id")


def test_storage_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        db = Path(d) / "todo.json"
        tasks = []
        todo.add(tasks, "persist me")
        todo.mark_done(tasks, 1)
        todo.save(db, tasks)
        loaded = todo.load(db)
        assert loaded == tasks  # dataclass field equality
        assert loaded[0].done is True


if __name__ == "__main__":
    test_add_and_id_increment()
    test_done_and_missing()
    test_storage_roundtrip()
    print("ok")
