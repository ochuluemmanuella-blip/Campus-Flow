# AI Learning Log

## Fellow: Ochulu Agbenu

### Interaction #1: bool vs int, and validating affected_users

**Problem:** `affected_users` must be a positive whole number. I needed to know how Python treats `True`, text like `"15"`, and decimals, so `create_ticket` rejects bad input correctly.

**My initial understanding:** [[Write what you believed BEFORE running anything. For example: "I thought True is not a number, so isinstance(True, int) would be False."]]

**Prompt to AI:** I asked AI to guide me through the CampusFlow spec and what validation I'd need. AI suggested this topic and gave me a small experiment to run:
```python
print(isinstance(True, int))
print(True + 1)
print(int("15"), "15".isdigit())
print("-2".isdigit(), "3.5".isdigit())
int("3.5")
```

**Useful AI guidance:** In Python, `bool` is a subclass of `int`, so `True` behaves like `1` and `False` like `0`. This means an "is it an int?" check alone would accept `True` as `affected_users`. `str.isdigit()` returns False for `"-2"` and `"3.5"`, and `int("3.5")` raises `ValueError`.

**My independent experiment/test:** I ran the five lines myself. My first reported results were: line 1 `False`, line 2 `TypeError`, line 3 `False`, line 4 `False False`. [[Rerun them and paste the REAL terminal output here. If your first results differed from what Python printed, say so honestly. Note whether those were predictions or actual output.]]

**Verification source or result:** [[Add a reference you actually opened, for example the Python docs page on the bool type or on str.isdigit(), and write what it says in your own words. Add the link.]]

**Decision:** [[Accepted / improved / rejected, and why. Example: accepted — create_ticket will check for bool explicitly before checking for int.]]

**Related file/commit:** [[tickets.py / test name / PR link, filled in once Issue #2 is merged.]]

**What I can now explain without AI:** [[Your own words: why must create_ticket reject True for affected_users? Don't copy the explanation above.]]

---

### Interaction #2: JSON errors, wrong shapes and safe file writing

**Problem:** `load_tickets` must not silently erase data when `tickets.json` is broken, and `save_tickets` must not corrupt the file if the program crashes mid-write.

**My initial understanding:** I think while using json.load() to read a file, it may crash if the file is empty or if it's not a file it's reading in the first place.

**Prompt to AI:** "Explain json.load() and json.loads() errors with a five-line example unrelated to CampusFlow. Then explain why valid JSON of the wrong shape can still be a problem, and how to write a file safely so a crash doesn't corrupt it. Give me experiments to run, not my project's code. I want to write my own code."

**Useful AI guidance:** `json.loads` parses a string and `json.load` parses an open file; both raise `JSONDecodeError` on malformed text. A missing file fails earlier, in `open()`, with `FileNotFoundError`. Valid JSON of the wrong shape (such as `null` or a dict) parses without any error. Opening a file with `"w"` empties it immediately, so a crash mid-write can lose data. The safer pattern is to write a temp file and then swap it in with `os.replace`.

**My independent experiment/test:** I predicted first, then ran `examp.py` and `tryout.py`.

| Experiment | My prediction | Actual output |
|---|---|---|
| A: `json.loads` on 5 inputs | `'{"a": 1'`, `''` and `null` would raise errors; unsure of the result types | dict; JSONDecodeError; JSONDecodeError; list; NoneType. `null` parsed fine as `None` |
| B: `json.load(open("does_not_exist.json"))` | JSONDecodeError, because `.load()` takes files and `.loads()` takes strings | `FileNotFoundError` (raised by `open()`, before JSON ran) |
| C: file size before and after `open(..., "w")` | sizes in bytes; unsure what it means for a crash | `8` then `0` |
| D: `os.replace` of a temp file | `demo.json` is overwritten; `os.path.exists("demo.tmp")` would be True | `{"v": 2} False` (the temp file was renamed, so `demo.tmp` no longer exists) |
| E: `json.load` on an empty file | an error | `JSONDecodeError - Expecting value: line 1 column 1 (char 0)` |

Three predictions were wrong (`null`, B's error type, and `exists` in D). I corrected my understanding: B failed in `open()` before JSON was involved, `null` is valid JSON, and `os.replace` moves the temp file instead of copying it.

**Verification source or result:**
- Python docs, `json.JSONDecodeError`: https://docs.python.org/3/library/json.html#json.JSONDecodeError. It is a subclass of `ValueError` and carries `msg`, `pos`, `lineno` and `colno`. [[open the link and confirm]]
- Python docs, `os.replace`: https://docs.python.org/3/library/os.html#os.replace. It renames the file and silently replaces the destination, and a successful rename is atomic. [[open the link and confirm]]
- My own runs: the real outputs above, including `8` then `0` and `JSONDecodeError` on the empty file.

**Decision:** Accepted, with changes to how I'll use it:
- A missing file will give an empty list (a fresh start).
- Malformed JSON, or valid JSON that isn't a list, will raise `StorageError` and stop the program without overwriting the file.
- `save_tickets` will write a temp file in the same folder and then call `os.replace`.
- I will use `with open(...)` so files are closed, which my scratch scripts did not do.

**Related file/commit:** `campusflow/storage.py` and `tests/test_storage.py` (Issue #3). [[add the branch, commit SHA or PR link once it's merged]]

**What I can now explain without AI:** Reading and writing are different risks. When reading, a missing file and a broken file are different problems: the missing file fails in `open()` and is safe to treat as a fresh start, while a broken file fails in `json.load()` and means stop, because starting empty would let the next save overwrite whatever is in it. Valid JSON can also be the wrong shape, like `null`, so I check the type myself after loading. When writing, `open(path, "w")` empties the file straight away (my experiment went from 8 bytes to 0), so a crash at that moment leaves nothing. Writing to a temp file first and swapping it in with `os.replace` means `tickets.json` is always either the full old version or the full new one.

**Also learned:** the difference between `load`/`loads` and `dump`/`dumps` (file versus string), and what `os.path.exists`, `os.path.getsize` and `open().read()` do. I only ran the `load`/`loads` side in an experiment, not `dump`/`dumps`.

