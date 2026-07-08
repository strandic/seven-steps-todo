# seven-steps-todo

A tiny JSON-backed todo CLI — the worked example for the **seven-steps** method
walkthrough on [blog.strandic.com](https://blog.strandic.com).

This repo is the **"before" state**: one-off tasks only. The article walks
through adding *recurring tasks* to it, one human-cleared gate at a time.

## Use it

No dependencies — Python 3.10+ standard library only.

```sh
python3 todo.py add "Pay rent"
python3 todo.py add "Write the blog post"
python3 todo.py list
python3 todo.py done 1
```

Tasks are stored in `~/.todo.json` (override with `TODO_DB=./todo.json`).

Run the checks:

```sh
python3 test_todo.py      # prints "ok"
```

## The feature the article adds: recurring tasks

```sh
todo add "Standup" --every weekday
todo add "Rent"    --every monthly:1
```

Instead of a one-off, a recurring task generates due instances on a schedule.

### Why this is a seven-steps fit

The method is tuned for *one medium, structural* change — not a one-liner, not a
milestone. Recurrence qualifies:

- **Structural, multi-site.** It touches the model (a recurrence rule on `Task`),
  storage, the "what's due" listing, and the CLI — a real change surface, not an
  edit in one place.
- **A recon-worthy technique.** The obvious approach — advance a due date by a
  fixed `timedelta` — is subtly wrong at month boundaries ("monthly on the 1st"),
  and across DST for time-of-day rules. Only mocking it against real dates
  reveals the calendar-correct mechanism. (Step 4.)
- **A real invariant.** Regenerating due instances must never double-create the
  same occurrence — the generation has to be idempotent. That is a pre-agreed
  ruling worth enforcing, not a nice-to-have. (Step 5.)

A wrong design here is expensive; the change is small enough that the gates don't
smother it. That's the sweet spot the method is built for.

## Layout

- `todo.py` — model (`Task`), storage (`load`/`save`), behaviour (`add`,
  `mark_done`, `render`), and the argparse CLI. Behaviour is pure over a
  `list[Task]`; storage is separate — the seams the method builds on.
- `test_todo.py` — runnable assert-based checks.
