#!/usr/bin/env python3
"""Rebuild components.json from programs, plugins, and contracts.

    python3 web/components/update.py
    python3 web/components/update.py --watch

The explorer reloads that file while it is open.
"""

import argparse
import json
import re
import time
from pathlib import Path

KIND_ORDER = [
    "program",
    "contract",
    "plugin",
    "action",
    "table",
    "notify",
    "option",
    "interface",
    "class",
    "file",
]
PROGRAM_ORDER = ["humanityd", "humanity", "humanity-keyd", "humanity-util"]
PROGRAM_DOCS = {
    "humanityd": "docs/01_humanityd/index.md",
    "humanity": "docs/02_humanity/index.md",
    "humanity-keyd": "docs/03_humanity-keyd/index.md",
    "humanity-util": "docs/10_utilities/index.md",
}
PROGRAM_TALKS = {"humanity": ["humanityd", "humanity-keyd"]}
CLASS_RE = re.compile(r'class\s+\[\[eosio::contract\("([^"]+)"\)\]\]\s*(\w+)')
ACTION_RE = re.compile(r'\[\[eosio::action\]\]\s*(?:void\s+)?(\w+)\s*\(|\bACTION\s+(\w+)\s*\(')
NOTIFY_RE = re.compile(r'\[\[eosio::on_notify\("([^"]+)"\)\]\]\s*(?:void\s+)?(\w+)\s*\(')
TABLE_RE = re.compile(r'(?:struct|class)\s+\[\[([^\]]+)\]\]\s*(\w+)')
INDEX_RE = re.compile(r'(?:multi_index|singleton)\s*<\s*"([^"]+)"_n\s*,\s*(\w+)')
TABLE_MACRO_RE = re.compile(r"\bTABLE\s+(\w+)\s*\{")
OPTION_RE = re.compile(r'\(\s*"([a-z][a-z0-9-]*-[a-z0-9-]*(?:,[A-Za-z])?)"')
PLUGIN_CLASS_RE = re.compile(r'class\s+(\w+)\s*:\s*public\s+(?:appbase::)?plugin\s*<')


def first_sentence(text):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""
    out = ""
    for part in re.split(r"(?<=[.])\s+", text):
        out = f"{out} {part}".strip()
        if len(out) >= 12 and out.endswith(".") and not re.search(r"\b(?:e\.g|i\.e|vs)\.$", out):
            break
        if len(out) > 320:
            break
    return out[:320].rstrip()


def usable(summary):
    return bool(summary) and "===" not in summary and sum(ch.isalpha() for ch in summary) >= 8


def clean_comment(raw):
    if not raw or any(token in raw for token in ("Copyright", "SPDX", "License")):
        return ""
    lines = []
    for line in raw.splitlines():
        line = re.sub(r"^\s*\*\s?", "", line).strip()
        if "===" in line:
            continue
        if line.startswith(("@param", "@pre", "@return")):
            if lines:
                break
            continue
        line = re.sub(r"^@(notice|dev|brief)\s+", "", line)
        if not line or line.startswith("@") or line.startswith("```") or line.startswith("#"):
            if lines and not line:
                break
            continue
        lines.append(line)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", " ".join(lines))
    return first_sentence(text.replace("`", ""))


def comment_before(text, index):
    before = text[:index].rstrip()
    blocks = list(re.finditer(r"/\*\*(.*?)\*/|/\*(.*?)\*/", before, re.S))
    if blocks and blocks[-1].end() == len(before):
        raw = blocks[-1].group(1) if blocks[-1].group(1) is not None else blocks[-1].group(2)
        return clean_comment(raw)
    lines = []
    for line in reversed(before.splitlines()):
        stripped = line.strip()
        if not stripped.startswith("//"):
            break
        body = re.sub(r"/+$", "", re.sub(r"^/+\s*", "", stripped)).strip()
        if "===" in body or not re.search(r"[A-Za-z]", body):
            continue
        if body.startswith(("@param", "@pre", "@return")):
            continue
        body = re.sub(r"^@(notice|dev|brief)\s+", "", body)
        if body.startswith("@"):
            continue
        lines.append(body)
    return first_sentence(" ".join(reversed(lines)))


def plain_paragraph(body):
    body = re.sub(r"^---\n.*?\n---\n", "", body, count=1, flags=re.S)
    buf = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("[[") or stripped.startswith("[//]") or stripped.startswith("```"):
            if buf:
                break
            continue
        if not stripped or stripped[:1] in "#!*|-":
            if buf:
                break
            continue
        buf.append(stripped)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", " ".join(buf))
    return first_sentence(text.replace("`", ""))


def section_paragraph(text, heading):
    found = re.search(rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s|\Z)", text, re.S | re.M)
    return plain_paragraph(found.group(1) if found else text)


def hidden(text, index):
    line = text.rfind("\n", 0, index) + 1
    return "//" in text[line:index] or text[:index].count("/*") > text[:index].count("*/")


def looks_like_help(text):
    if not 20 <= len(text) <= 320:
        return False
    if any(token in text for token in ("::", "/*", "*/", "->", "==", "${")):
        return False
    return sum(ch.isalpha() for ch in text) >= 16


def sort_contains(items):
    rank = {kind: i for i, kind in enumerate(KIND_ORDER)}
    items.sort(key=lambda item: (rank.get(item["kind"], 99), item["name"]))


def struct_fields(text, index):
    start = text.find("{", index)
    if start < 0:
        return []
    depth = 0
    end = min(len(text), start + 4000)
    body = text[start + 1 : end]
    for i, ch in enumerate(text[start:end]):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                body = text[start + 1 : start + i]
                break
    fields = []
    for line in body.splitlines():
        if "primary_key" in line:
            break
        found = re.match(r"\s*[\w:<>,&\s]+?\s+(\w+)\s*(?:=[^;]*)?;(?:\s*//.*)?\s*$", line)
        if found and found.group(1) not in {"public", "private", "protected"}:
            fields.append(found.group(1))
    return fields[:12]


def read_sources(directory):
    sources = []
    for path in sorted(directory.rglob("*")):
        if path.suffix not in {".hpp", ".h", ".cpp"}:
            continue
        if any(part in {"tests", "test", "unittests", "alcor-exchange"} for part in path.parts):
            continue
        sources.append((path, path.read_text(errors="replace")))
    return sources


def parse_contracts(root):
    nodes = {}
    classes_at = {}
    base = root / "contracts"
    for directory in sorted(path for path in base.iterdir() if path.is_dir()):
        if directory.name == "test_contracts":
            continue
        folder = f"contracts/{directory.name}"
        for path, text in read_sources(directory):
            classes = []
            for found in CLASS_RE.finditer(text):
                if hidden(text, found.start()):
                    continue
                classes.append((found.start(), found.group(1), found.group(2)))
                classes_at.setdefault(found.group(1), folder)
                node = nodes.setdefault(
                    found.group(1),
                    {
                        "id": f"contract:{found.group(1)}",
                        "name": found.group(1),
                        "kind": "contract",
                        "path": folder,
                        "summary": "",
                        "contains": [],
                    },
                )
                summary = comment_before(text, found.start())
                if len(summary) > len(node["summary"]):
                    node["summary"] = summary

            def owner(index, explicit=""):
                if explicit:
                    return explicit
                chosen = ""
                for start, name, _class_name in classes:
                    if start <= index:
                        chosen = name
                if chosen:
                    return chosen
                names = {name for _start, name, _class_name in classes}
                return next(iter(names)) if len(names) == 1 else ""

            index_of = {}
            for found in INDEX_RE.finditer(text):
                index_of.setdefault(found.group(2), found.group(1))
            for found in TABLE_RE.finditer(text):
                if hidden(text, found.start()) or "eosio::table" not in found.group(1):
                    continue
                explicit = re.search(r'eosio::table\(\s*"([^"]+)"\s*\)', found.group(1))
                contract = re.search(r'eosio::contract\(\s*"([^"]+)"\s*\)', found.group(1))
                name = owner(found.start(), contract.group(1) if contract else "")
                if not name or name not in nodes:
                    continue
                table = explicit.group(1) if explicit else index_of.get(found.group(2), found.group(2))
                summary = comment_before(text, found.start())
                fields = struct_fields(text, found.end())
                if not summary and fields:
                    summary = "Fields: " + ", ".join(fields) + "."
                add_item(nodes[name], "table", table, summary)
            for found in TABLE_MACRO_RE.finditer(text):
                if hidden(text, found.start()):
                    continue
                name = owner(found.start())
                if not name or name not in nodes:
                    continue
                summary = comment_before(text, found.start())
                fields = struct_fields(text, found.end() - 1)
                if not summary and fields:
                    summary = "Fields: " + ", ".join(fields) + "."
                add_item(nodes[name], "table", index_of.get(found.group(1), found.group(1)), summary)
            for found in ACTION_RE.finditer(text):
                if hidden(text, found.start()):
                    continue
                name = owner(found.start())
                action = found.group(1) or found.group(2)
                if name and action and name in nodes:
                    add_item(nodes[name], "action", action, comment_before(text, found.start()))
            for found in NOTIFY_RE.finditer(text):
                if hidden(text, found.start()):
                    continue
                name = owner(found.start())
                if name and name in nodes:
                    add_item(nodes[name], "notify", found.group(2), found.group(1))
        if (directory / "alcor-exchange").is_dir() and "flex.token" in nodes:
            add_item(
                nodes["flex.token"],
                "interface",
                "alcor-exchange",
                "Headers under contracts/ra.pure/alcor-exchange for the external alcorswap contract.",
            )
    for name, node in nodes.items():
        if not usable(node["summary"]):
            actions = [item["name"] for item in node["contains"] if item["kind"] == "action"]
            shown = ", ".join(actions[:10])
            node["summary"] = (f"Actions: {shown}{'…' if len(actions) > 10 else '.'}") if actions else f"Contract {name}."
        node["path"] = classes_at.get(name, node["path"])
        sort_contains(node["contains"])
    by_path = {}
    for node in nodes.values():
        by_path.setdefault(node["path"], []).append(node)
    for folder, group in by_path.items():
        if len(group) < 2:
            continue
        primary = next((node for node in group if node["name"] == folder.split("/")[-1]), group[0])
        for other in group:
            if other is not primary:
                add_item(primary, "contract", other["name"], other["summary"], other["id"])
        sort_contains(primary["contains"])
    return [nodes[name] for name in sorted(nodes)]


def add_item(node, kind, name, summary, item_id=""):
    for item in node["contains"]:
        if item["kind"] == kind and item["name"] == name:
            if len(summary) > len(item["summary"]):
                item["summary"] = summary
            if item_id and not item["id"]:
                item["id"] = item_id
            return
    node["contains"].append({"id": item_id, "kind": kind, "name": name, "summary": summary})


def plugin_doc(root, directory):
    for candidate in (
        root / "docs/01_humanityd/03_plugins" / directory / "index.md",
        root / "docs/03_humanity-keyd/15_plugins" / directory / "index.md",
        root / "docs/03_humanity-keyd/15_plugins" / f"{directory}.md",
    ):
        if candidate.is_file():
            text = candidate.read_text(errors="replace")
            summary = section_paragraph(text, "Description") or plain_paragraph(text)
            if summary:
                return summary
    return ""


def option_items(sources):
    items = []
    seen = set()
    for _path, text in sources:
        found = list(OPTION_RE.finditer(text))
        for index, match in enumerate(found):
            name = match.group(1).split(",")[0]
            if name in seen:
                continue
            end = found[index + 1].start() if index + 1 < len(found) else match.end() + 700
            window = text[match.end() : min(end, match.end() + 700)]
            summary = ""
            for literal in re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', window):
                literal = literal.replace('\\"', '"').replace("\\n", " ")
                if looks_like_help(literal):
                    summary = first_sentence(literal)
                    break
            if not summary:
                continue
            seen.add(name)
            items.append({"id": "", "kind": "option", "name": name, "summary": summary})
    return items


def parse_plugins(root):
    nodes = []
    for directory in sorted(path for path in (root / "plugins").iterdir() if path.is_dir()):
        sources = read_sources(directory)
        classes = []
        for path, text in sources:
            for found in PLUGIN_CLASS_RE.finditer(text):
                if not hidden(text, found.start()):
                    classes.append((found.group(1), text, found.start(), path))
        if not classes:
            continue
        doc = plugin_doc(root, directory.name)
        options = option_items([(path, text) for path, text in sources if path.suffix == ".cpp"])
        primary = directory.name if any(name == directory.name for name, *_rest in classes) else classes[0][0]
        for name, text, index, path in classes:
            requires = re.search(r"APPBASE_PLUGIN_REQUIRES\(([^;]*)\)", text[index : index + 1500])
            req_names = re.findall(r"\((\w+)\)", requires.group(1) if requires else "")
            own = comment_before(text, index)
            if name == directory.name and doc:
                summary = doc
            elif usable(own):
                summary = own
            else:
                summary = doc or f"Plugin {name}."
            node = {
                "id": f"plugin:{name}",
                "name": name,
                "kind": "plugin",
                "path": f"plugins/{directory.name}",
                "summary": summary,
                "contains": [],
            }
            for req in dict.fromkeys(req_names):
                add_item(node, "plugin", req, "", f"plugin:{req}")
            if name == primary:
                node["contains"].extend(options)
                for other, _text, _index, _path in classes:
                    if other != name:
                        add_item(node, "plugin", other, "", f"plugin:{other}")
            if not node["contains"]:
                for src, _text in sources:
                    if src.suffix in {".cpp", ".hpp", ".h"}:
                        add_item(node, "file", src.name, str(src.relative_to(directory)))
                    if sum(item["kind"] == "file" for item in node["contains"]) >= 8:
                        break
            sort_contains(node["contains"])
            nodes.append(node)
    nodes.sort(key=lambda node: node["name"])
    return nodes


def parse_programs(root):
    nodes = []
    base = root / "programs"
    names = [name for name in PROGRAM_ORDER if (base / name).is_dir()]
    for path in sorted(base.iterdir()):
        if path.is_dir() and path.name not in names:
            names.append(path.name)
    for name in names:
        doc = PROGRAM_DOCS.get(name)
        summary = ""
        if doc and (root / doc).is_file():
            text = (root / doc).read_text(errors="replace")
            summary = section_paragraph(text, "Introduction") or plain_paragraph(text)
        cmake = (base / name / "CMakeLists.txt").read_text(errors="replace") if (base / name / "CMakeLists.txt").is_file() else ""
        node = {
            "id": f"program:{name}",
            "name": name,
            "kind": "program",
            "path": f"programs/{name}",
            "summary": summary or f"Program {name}.",
            "contains": [],
        }
        for other in PROGRAM_TALKS.get(name, []):
            add_item(node, "program", other, "", f"program:{other}")
        for token in dict.fromkeys(re.findall(r"\b([A-Za-z0-9_]+_plugin)\b", cmake)):
            add_item(node, "plugin", token, "", f"plugin:{token}")
        sort_contains(node["contains"])
        nodes.append(node)
    return nodes


def fill_summaries(nodes):
    by_id = {node["id"]: node for node in nodes}
    for node in nodes:
        kept = []
        for item in node["contains"]:
            target = by_id.get(item["id"])
            if item["id"] and target is None:
                item["id"] = ""
            elif target and not item["summary"]:
                item["summary"] = target["summary"]
            if not item["summary"]:
                item["summary"] = item["name"]
            kept.append(item)
        node["contains"] = kept


def build(root):
    root = Path(root).resolve()
    programs = parse_programs(root)
    contracts = parse_contracts(root)
    plugins = parse_plugins(root)
    nodes = programs + contracts + plugins
    fill_summaries(nodes)
    if len(programs) < 4 or len(contracts) < 8 or len(plugins) < 10:
        raise SystemExit(
            f"catalog looks incomplete: programs={len(programs)} contracts={len(contracts)} plugins={len(plugins)}"
        )
    overview = (root / "docs/index.md").read_text(errors="replace") if (root / "docs/index.md").is_file() else ""
    root_node = {
        "id": "humanity-pro",
        "name": "Humanity Pro",
        "kind": "platform",
        "path": "",
        "summary": plain_paragraph(overview) or "Humanity Pro programs, contracts, and plugins.",
        "contains": [
            {"id": node["id"], "kind": node["kind"], "name": node["name"], "summary": node["summary"]}
            for node in nodes
        ],
    }
    sort_contains(root_node["contains"])
    return {
        "updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "root": root_node,
        "groups": [
            {"id": "programs", "name": "Programs", "color": "#22c55e", "nodes": programs},
            {"id": "contracts", "name": "Contracts", "color": "#8b5cf6", "nodes": contracts},
            {"id": "plugins", "name": "Plugins", "color": "#f97316", "nodes": plugins},
        ],
    }


def write(root, out):
    catalog = build(root)
    out = Path(out)
    fresh = {key: value for key, value in catalog.items() if key != "updated"}
    if out.is_file():
        try:
            previous = json.loads(out.read_text())
        except json.JSONDecodeError:
            previous = None
        if previous and {key: value for key, value in previous.items() if key != "updated"} == fresh:
            return False
    out.parent.mkdir(parents=True, exist_ok=True)
    temporary = out.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(catalog, indent=2) + "\n")
    temporary.replace(out)
    counts = {group["id"]: len(group["nodes"]) for group in catalog["groups"]}
    print(f"wrote {out} {counts}", flush=True)
    return True


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Rewrite components.json from the Humanity Pro tree.")
    parser.add_argument("--root", type=Path, default=here.parent.parent)
    parser.add_argument("--out", type=Path, default=here / "components.json")
    parser.add_argument("--watch", action="store_true", help="Rebuild every 2 seconds while sources change.")
    args = parser.parse_args()
    if not args.watch:
        write(args.root, args.out)
        return
    while True:
        try:
            write(args.root, args.out)
        except Exception as exc:
            print(exc, flush=True)
        time.sleep(2)


if __name__ == "__main__":
    main()
