#!/usr/bin/env python3
"""todo — a tiny JSON-backed todo CLI.

The "before" state for the seven-steps walkthrough (see README): one-off tasks
only — add, list, done. The article adds *recurring* tasks on top of this.

Standard library only, no dependencies. Run with `python3 todo.py ...`.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


def default_db() -> Path:
    """Where tasks live. Override with $TODO_DB (handy for tests and demos)."""
    return Path(os.environ.get("TODO_DB") or Path.home() / ".todo.json")


# --- model ---------------------------------------------------------------

@dataclass
class Task:
    id: int
    text: str
    done: bool = False


# --- storage -------------------------------------------------------------

def load(db: Path) -> list[Task]:
    if not db.exists():
        return []
    return [Task(**row) for row in json.loads(db.read_text())]


def save(db: Path, tasks: list[Task]) -> None:
    db.write_text(json.dumps([asdict(t) for t in tasks], indent=2))


# --- behaviour (pure over a list[Task]) ----------------------------------

def add(tasks: list[Task], text: str) -> Task:
    task = Task(id=max((t.id for t in tasks), default=0) + 1, text=text)
    tasks.append(task)
    return task


def mark_done(tasks: list[Task], task_id: int) -> Task:
    for t in tasks:
        if t.id == task_id:
            t.done = True
            return t
    raise KeyError(f"no task with id {task_id}")


def render(tasks: list[Task]) -> str:
    if not tasks:
        return "(no tasks)"
    return "\n".join(
        f"{t.id:>3}  [{'x' if t.done else ' '}]  {t.text}" for t in tasks
    )


# --- CLI -----------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="todo", description="A tiny todo CLI.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("text", help="what to do")

    sub.add_parser("list", help="list tasks")

    p_done = sub.add_parser("done", help="mark a task done")
    p_done.add_argument("id", type=int, help="task id")

    args = parser.parse_args(argv)
    db = default_db()
    tasks = load(db)

    if args.cmd == "add":
        task = add(tasks, args.text)
        save(db, tasks)
        print(f"added {task.id}: {task.text}")
    elif args.cmd == "list":
        print(render(tasks))
    elif args.cmd == "done":
        try:
            task = mark_done(tasks, args.id)
        except KeyError:
            print(f"no task with id {args.id}", file=sys.stderr)
            return 1
        save(db, tasks)
        print(f"done {task.id}: {task.text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
