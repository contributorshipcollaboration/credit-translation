#!/usr/bin/env python3
"""Validate the CRediT translation files in translations/.

Usage:
    pip install -r scripts/requirements.txt
    python scripts/validate.py [--base GIT_REF]

Every translation is checked against the JSON schema it declares in "$schema"
(schemas live in the repository root as credit_translation_schema-X.Y.Z.json).
Files that were changed since --base (default: the merge base with origin/main)
must use the NEWEST schema; untouched files may stay on an older one.

On top of the schema, the script checks things a schema cannot express:
ISO 639 / ISO 15924 codes, the file name, ORCID checksums, duplicate JSON keys,
and file encoding; and that each schema lists the roles of credit_roles.json. Whitespace oddities are
reported as warnings only. Exit status is 1 if any error was found.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pycountry
from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parent.parent
TRANSLATIONS = ROOT / "translations"
SCHEMA_RE = re.compile(r"^credit_translation_schema-(\d+)\.(\d+)\.(\d+)\.json$")
ORCID_RE = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")
ROLE_PREFIX = "https://credit.niso.org/contributor-roles/"
ON_GITHUB = os.environ.get("GITHUB_ACTIONS") == "true"

counts = {"error": 0, "warning": 0}


def _gh_escape(text, prop=False):
    text = text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    return text.replace(":", "%3A").replace(",", "%2C") if prop else text


def report(level, file, message, line=None):
    """Print a problem; on GitHub Actions emit an annotation shown in the PR."""
    counts[level] += 1
    if ON_GITHUB:
        loc = f"file={_gh_escape(file, True)}" if file else ""
        if line:
            loc += f",line={line}"
        print(f"::{level} {loc}::{_gh_escape(message)}")
    else:
        where = f"{file}" + (f":{line}" if line else "") if file else "(repository)"
        print(f"{level.upper():7} {where}: {message}")


def error(file, message, line=None):
    report("error", file, message, line)


def warn(file, message, line=None):
    report("warning", file, message, line)


def fmt_path(path):
    out = ""
    for part in path:
        if isinstance(part, int):
            out += f"[{part}]"
        elif part.startswith(ROLE_PREFIX):
            out += f"[{part[len(ROLE_PREFIX):].rstrip('/')}]"
        else:
            out += ("." if out else "") + part
    return out or "(top level)"


def no_duplicate_keys(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f'duplicate key "{key}" (a key may appear only once per object)')
        seen[key] = value
    return seen


def check_schema_roles(name, schema, role_urls):
    required = set(schema.get("properties", {}).get("translations", {}).get("required", []))
    if required != role_urls:
        error(name, "roles required by the schema differ from credit_roles.json "
                    f"(missing: {sorted(role_urls - required) or 'none'}; "
                    f"unexpected: {sorted(required - role_urls) or 'none'})")


def load_schemas():
    """Return ({file name: (schema, validator)}, name of the newest schema)."""
    found = {}
    for path in ROOT.glob("credit_translation_schema-*.json"):
        match = SCHEMA_RE.match(path.name)
        if not match:
            continue
        rel = path.name
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft7Validator.check_schema(schema)
        except Exception as exc:  # unreadable or not a valid Draft-07 schema
            error(rel, f"schema is not valid: {str(exc).splitlines()[0]}")
            continue
        if not str(schema.get("$id", "")).endswith("/" + path.name):
            error(rel, f'"$id" must end with the file name "{path.name}"')
        found[path.name] = (schema, Draft7Validator(schema), tuple(map(int, match.groups())))
    if not found:
        error(None, "no credit_translation_schema-X.Y.Z.json found in the repository root")
        sys.exit(1)
    newest = max(found, key=lambda n: found[n][2])
    return found, newest


def changed_files(base):
    """Paths (relative to the repo root) changed since base, or None if unknown."""
    def git(*args):
        return subprocess.run(["git", "-c", "core.quotepath=false", *args],
                              cwd=ROOT, capture_output=True, text=True)
    if not base:
        result = git("merge-base", "origin/main", "HEAD")
        base = result.stdout.strip() if result.returncode == 0 else None
    if not base or set(base) == {"0"} or git("cat-file", "-e", base + "^{commit}").returncode:
        return None
    changed = git("diff", "--name-only", "--diff-filter=d", base).stdout.splitlines()
    changed += git("ls-files", "--others", "--exclude-standard").stdout.splitlines()
    return set(changed)


def strings_to_lint(data):
    meta = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    for key in ("languageName", "translationProcedure"):
        if isinstance(meta.get(key), str):
            yield f"metadata.{key}", meta[key]
    for i, tr in enumerate(meta.get("translators") or []):
        if isinstance(tr, dict):
            for key in ("firstName", "middleName", "lastName"):
                if isinstance(tr.get(key), str):
                    yield f"metadata.translators[{i}].{key}", tr[key]
    roles = data.get("translations") if isinstance(data.get("translations"), dict) else {}
    for url, role in roles.items():
        if isinstance(role, dict):
            for key in ("name", "description"):
                if isinstance(role.get(key), str):
                    yield fmt_path(["translations", url, key]), role[key]


def orcid_checksum_ok(orcid):
    total = 0
    for digit in orcid.replace("-", "")[:15]:
        total = (total + int(digit)) * 2
    check = (12 - total % 11) % 11
    return orcid[-1] == ("X" if check == 10 else str(check))


def lookup_language(code):
    try:
        if len(code) == 2:
            return pycountry.languages.get(alpha_2=code)
        if len(code) == 3:
            return pycountry.languages.get(alpha_3=code)
    except KeyError:
        pass
    return None


def check_file(path, schemas, newest, changed, pairs_seen):
    rel = f"translations/{path.name}"
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        error(rel, "file starts with a byte-order mark (BOM); save it as plain UTF-8")
    if b"\r" in raw:
        error(rel, "file uses Windows line endings (CRLF); use Unix line endings (LF)")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        error(rel, f"file is not valid UTF-8 (problem near byte {exc.start})")
        return
    if not text.endswith("\n"):
        warn(rel, "file does not end with a newline")
    try:
        data = json.loads(text, object_pairs_hook=no_duplicate_keys)
    except json.JSONDecodeError as exc:
        error(rel, f"not valid JSON: {exc.msg}", exc.lineno)
        return
    except ValueError as exc:
        error(rel, str(exc))
        return
    if not isinstance(data, dict):
        error(rel, "the top level of the file must be a JSON object")
        return

    # --- which schema applies -------------------------------------------------
    touched = changed is not None and rel in changed
    declared = data.get("$schema")
    chosen = newest
    if not isinstance(declared, str):
        error(rel, f'missing "$schema". Add this as the first line inside the braces: '
                   f'"$schema": "{schemas[newest][0]["$id"]}",')
    else:
        match = [n for n, (s, _, _) in schemas.items() if s["$id"] == declared]
        if not match:
            error(rel, f'"$schema" ({declared}) is not a schema of this repository. '
                       f'Use "{schemas[newest][0]["$id"]}"')
        elif match[0] != newest and touched:
            error(rel, f'this file was changed, so it must use the latest schema ({newest}). '
                       f'Set "$schema" to "{schemas[newest][0]["$id"]}" and fix anything reported below')
        elif match[0] != newest:
            chosen = match[0]
    if touched:
        chosen = newest

    # --- JSON schema ----------------------------------------------------------
    validator = schemas[chosen][1]
    for err in sorted(validator.iter_errors(data), key=lambda e: [str(p) for p in e.absolute_path]):
        own = err.validator in ("pattern", "minLength", "type", "enum", "const", "format")
        hint = err.schema.get("description") if own and isinstance(err.schema, dict) else None
        msg = err.message if len(err.message) <= 220 else err.message[:217] + "..."
        error(rel, f"{fmt_path(err.absolute_path)}: {msg}" + (f" [{hint}]" if hint else ""))

    # --- checks a schema cannot express -----------------------------------------
    meta = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    code, script = meta.get("languageCode"), meta.get("scriptCode")
    if isinstance(code, str) and re.fullmatch(r"[a-z]{2,3}", code):
        language = lookup_language(code)
        if language is None:
            error(rel, f'languageCode "{code}" is not an ISO 639 code')
        elif len(code) == 3 and getattr(language, "alpha_2", None):
            error(rel, f'languageCode "{code}" has a two-letter ISO 639-1 code; use "{language.alpha_2}"')
    if isinstance(script, str) and re.fullmatch(r"[A-Z][a-z]{3}", script):
        if pycountry.scripts.get(alpha_4=script) is None:
            error(rel, f'scriptCode "{script}" is not an ISO 15924 code')
    if isinstance(code, str) and isinstance(script, str):
        if path.stem != f"{code}_{script}":
            error(rel, f'file name must be "{code}_{script}.json" to match languageCode and scriptCode')
        if (code, script) in pairs_seen:
            error(rel, f"same language and script as {pairs_seen[(code, script)]}")
        pairs_seen.setdefault((code, script), path.name)
    for i, tr in enumerate(meta.get("translators") or []):
        orcid = tr.get("ORCID") if isinstance(tr, dict) else None
        if isinstance(orcid, str) and ORCID_RE.match(orcid) and not orcid_checksum_ok(orcid):
            error(rel, f"metadata.translators[{i}].ORCID {orcid} has an invalid checksum (typo?)")
    # --- warnings ---------------------------------------------------------------
    for where, value in strings_to_lint(data):
        if value != value.strip():
            warn(rel, f"{where} has leading or trailing whitespace")
        if "  " in value.strip():
            warn(rel, f"{where} contains a double space")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--base", help="git ref to compare with; files changed since then must use the newest schema")
    args = parser.parse_args()

    schemas, newest = load_schemas()
    role_urls = set(json.loads((ROOT / "credit_roles.json").read_text(encoding="utf-8")))
    for name, (schema, _, _) in schemas.items():
        check_schema_roles(name, schema, role_urls)
    changed = changed_files(args.base)
    files = sorted(TRANSLATIONS.glob("*.json"))
    print(f"Newest schema: {newest}. Checking {len(files)} translation files.")
    if changed is None:
        print("Note: could not determine which files changed; every file is checked against the schema it declares.")
    else:
        touched = [f.name for f in files if f"translations/{f.name}" in changed]
        print(f"Files changed since base (must use the newest schema): {len(touched)}")
    pairs_seen = {}
    for path in files:
        check_file(path, schemas, newest, changed, pairs_seen)
    print(f"\nDone: {counts['error']} error(s), {counts['warning']} warning(s).")
    sys.exit(1 if counts["error"] else 0)


if __name__ == "__main__":
    main()
