"""Sync all Git-tracked Markdown docs to English without changing the originals."""

import argparse
import asyncio
from collections import Counter
from contextvars import ContextVar
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import hmac
from html import escape, unescape
from html.parser import HTMLParser
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import parse_qsl, quote, unquote, urlencode, urlsplit

from markdown_it import MarkdownIt
from markdown_it.helpers.parse_link_destination import parseLinkDestination


OUTPUT = Path("translations/en")
VERSION = "0.23.0"
GLOSSARY = Path(__file__).with_name("translation-glossary.md")
METADATA = ".co-op-translator.json"
SETTINGS = ".translation-settings.json"
NAV_START = "<!-- language-switch:start -->"
NAV_END = "<!-- language-switch:end -->"
NAV_PATTERN = re.compile(re.escape(NAV_START) + r".*?" + re.escape(NAV_END), re.S)
PARSER = MarkdownIt("commonmark").enable("table")
GENERATED_SIDEBAR = "_sidebar.en.md"
PLACEHOLDERS = re.compile(r"@@(?:INLINE_CODE|CODE_BLOCK|HTML_CODE|LINK_DESTINATION)_\d+@@")
HTML_CODE = re.compile(r"<(?P<tag>pre|code)\b[^>]*>.*?</(?P=tag)\s*>", re.I | re.S)
DIAGNOSTICS = ContextVar("translation_diagnostics", default=None)
FILE_ATTEMPTS = 3


class TranslationValidationError(ValueError):
    pass


def is_source_document(name):
    path = Path(name)
    return (not path.is_absolute() and ".." not in path.parts
            and path.suffix.lower() == ".md"
            and path.parts[0] != "translations"
            and name not in {GENERATED_SIDEBAR, "scripts/translation-glossary.md"}
            and not any(part in {"node_modules", ".venv", "venv", ".git"} for part in path.parts))


def discover_documents(root):
    # Git is the publication boundary: local notes, caches and ignored files stay out.
    names = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode("utf-8").split("\0")
    files = tuple(sorted(name for name in names if is_source_document(name)
                         and (root / name).is_file() and not (root / name).is_symlink()
                         and (root / name).resolve().is_relative_to(root.resolve())))
    if not files:
        raise ValueError("No Git-tracked Markdown documents found")
    return files


def apply_language_switch(text, language, source_path, translated_path):
    source_path = source_path.resolve()
    translated_path = translated_path.resolve()
    if len(NAV_PATTERN.findall(text)) > 1:
        raise ValueError("Duplicate language-switch blocks")
    if language == "zh":
        link = Path(os.path.relpath(translated_path, source_path.parent)).as_posix()
        label = f"**简体中文** · [English]({link})"
    else:
        link = Path(os.path.relpath(source_path, translated_path.parent)).as_posix()
        label = f"[简体中文]({quote(link, safe='/')}) · **English**"
    block = f"{NAV_START}\n\n{label}\n\n{NAV_END}"
    if NAV_PATTERN.search(text):
        return NAV_PATTERN.sub(lambda _: block, text)
    anchor = '<div align="center">'
    position = text.find(anchor)
    if position >= 0:
        position += len(anchor)
    else:
        heading = re.search(r"^# .*$", text, re.M)
        position = heading.end() if heading else 0
    return text[:position] + "\n\n" + block + text[position:]


class HtmlContent(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = 0
        self.structure = []

    def handle_starttag(self, tag, attrs):
        self.images += tag == "img"
        self.links.extend(value for key, value in attrs if key in {"src", "href"} and value)
        self.structure.append((tag, [(key, None if key == "aria-label" else value) for key, value in attrs
                                     if key not in {"src", "href", "alt", "title"}]))

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        self.structure.append(("/" + tag, []))


def html_code_matches(text):
    matches = list(HTML_CODE.finditer(text))
    if not matches:
        return []
    from co_op_translator.utils.markdown.spans import markdown_code_spans
    spans = markdown_code_spans(text)
    return [match for match in matches if not any(
        span.start <= match.start() < span.end for span in spans)]


def protect_html_code(text):
    literals = {}
    for match in reversed(html_code_matches(text)):
        index = len(literals)
        marker = f"@@HTML_CODE_{index}@@"
        while marker in text or marker in literals:
            index += 1
            marker = f"@@HTML_CODE_{index}@@"
        literals[marker] = match.group()
        text = text[:match.start()] + marker + text[match.end():]
    return text, literals


def restore_html_code(text, literals):
    for marker, literal in literals.items():
        if text.count(marker) != 1:
            raise TranslationValidationError(f"HTML code placeholder {marker} was lost or duplicated")
        text = text.replace(marker, literal, 1)
    return text


def document_parts(text):
    text = NAV_PATTERN.sub("", text)
    tokens = PARSER.parse(text)
    html_code = html_code_matches(text)
    html = HtmlContent()
    links, inline_code, images = [], [], 0
    inline_code_groups = []
    for token in tokens:
        if token.type == "inline":
            # English word order may change within a paragraph or table cell,
            # but literals must not move to another Markdown text block.
            inline_code_groups.append(Counter(child.content for child in token.children or []
                                              if child.type == "code_inline"))
        if token.type == "html_block":
            html.feed(token.content)
        for child in token.children or []:
            if child.type == "code_inline":
                inline_code.append(child.content)
            elif child.type == "link_open":
                links.append(child.attrGet("href"))
            elif child.type == "image":
                images += 1
                links.append(child.attrGet("src"))
            elif child.type == "html_inline":
                html.feed(child.content)
    return {
        "headings": [t.tag for t in tokens if t.type == "heading_open"],
        "code": [(t.type, t.info, t.content) for t in tokens if t.type in {"fence", "code_block"}],
        "inline_code": inline_code,
        "inline_code_groups": inline_code_groups,
        "html_code": [match.group() for match in html_code if match['tag'].lower() == "pre"],
        "html_inline_code": Counter(match.group() for match in html_code
                                    if match['tag'].lower() == "code"),
        "table_rows": sum(t.type == "tr_open" for t in tokens),
        "images": images + html.images,
        "html": html.structure,
        "links": links + html.links,
    }


def protected_ranges(text):
    offsets = [0]
    for line in text.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    ranges = [(offsets[t.map[0]], offsets[t.map[1]]) for t in PARSER.parse(text)
              if t.type in {"fence", "code_block"} and t.map]
    # Fence delimiters must not be mistaken for multiline inline-code delimiters.
    inline_text = list(text)
    for start, end in ranges:
        inline_text[start:end] = " " * (end - start)
    # Markdown inline code can span lines and use more than one backtick.
    for match in re.finditer(r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)", "".join(inline_text), re.S):
        ranges.append(match.span())
    ranges.extend(match.span() for match in html_code_matches(text))
    return ranges


def edit_link_destinations(text, destination):
    """Edit Markdown/reference/HTML URLs while preserving code and link titles."""
    ranges = protected_ranges(text)

    def protected(position):
        return any(start <= position < end for start, end in ranges)

    edits = []
    patterns = (r"\]\([ \t]*", r"^[ \t]{0,3}\[[^\]\n]+\]:[ \t]*")
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.M):
            if protected(match.start()):
                continue
            parsed = parseLinkDestination(text, match.end(), len(text))
            if not parsed.ok:
                continue
            old = text[match.end():parsed.pos]
            new = destination(parsed.str)
            if new != parsed.str:
                edits.append((match.end(), parsed.pos, f"<{new}>" if old.startswith("<") else new))
    for match in re.finditer(r"\b(?:href|src)\s*=\s*(['\"])(?P<url>.*?)\1", text):
        if not protected(match.start()):
            new = destination(unescape(match.group("url")))
            if new != unescape(match.group("url")):
                edits.append((*match.span("url"), escape(new, quote=True)))
    for start, end, replacement in sorted(set(edits), reverse=True):
        text = text[:start] + replacement + text[end:]
    return text


def local_target(url, document, root):
    parts = urlsplit(url)
    if parts.scheme or parts.netloc:
        return None
    if not parts.path:
        return document.resolve() if parts.fragment or parts.query else None
    base = root if parts.path.startswith("/") else document.parent
    return (base / unquote(parts.path).lstrip("/")).resolve()


@lru_cache(maxsize=256)
def heading_anchors(source_text, translated_text):
    def ids(text):
        tokens = PARSER.parse(NAV_PATTERN.sub("", text))
        counts, result = {}, []
        for index, token in enumerate(tokens):
            if token.type != "heading_open":
                continue
            title = PARSER.renderInline(tokens[index + 1].content)
            # Match the slug rules used by the site's pinned Docsify 4.13.1.
            slug = re.sub(r"<[^>]+>", "", title.strip().lower())
            slug = re.sub(r'''[\u2000-\u206f\u2e00-\u2e7f\\'!"#$%&()*+,./:;<=>?@\[\]^`{|}~]''', "", slug)
            slug = re.sub(r"-+", "-", re.sub(r"\s", "-", slug))
            slug = re.sub(r"^(\d)", r"_\1", slug)
            count = counts.get(slug, 0)
            counts[slug] = count + 1
            result.append(slug + (f"-{count}" if count else ""))
        return result
    mapping = dict(zip(ids(source_text), ids(translated_text)))
    # GitHub-style numeric anchors omit Docsify's leading underscore.
    mapping.update({re.sub(r"^_(\d)", r"\1", old): re.sub(r"^_(\d)", r"\1", new)
                    for old, new in list(mapping.items())})
    return mapping


def map_anchor_parts(parts, mapping):
    fragment = mapping.get(unquote(parts.fragment), parts.fragment)
    query = parts.query
    if any(key == "id" for key, value in parse_qsl(query)):
        query = urlencode([(key, mapping.get(value, value) if key == "id" else value)
                           for key, value in parse_qsl(query, keep_blank_values=True)])
    return query, fragment


def repair_local_links(text, doc_path, source_root, source_path=None, translated_files=None,
                       previous_anchors=None):
    doc_path = doc_path.resolve()
    source_root = source_root.resolve()
    translated_root = source_root / OUTPUT
    translated_files = set(translated_files or ())
    previous_anchors = previous_anchors or {}

    def destination(url):
        parts = urlsplit(url)
        target = local_target(url, source_path or doc_path, source_root)
        if target is None:
            return url
        if target.is_relative_to(translated_root):
            original = source_root / target.relative_to(translated_root)
        else:
            original = target
        if original.is_relative_to(source_root) and original.relative_to(source_root).as_posix() in translated_files:
            target = translated_root / original.relative_to(source_root)
        elif source_path is not None or (target.is_relative_to(translated_root) and not target.exists()):
            target = original
        query, fragment = parts.query, parts.fragment
        if target.is_relative_to(translated_root) and original.is_file() and target.is_file():
            name = original.relative_to(source_root).as_posix()
            mapping = heading_anchors(original.read_text(), target.read_text())
            if source_path is None:
                old = previous_anchors.get(name, {})
                query, fragment = map_anchor_parts(parts, {new: old for old, new in old.items()})
            query, fragment = map_anchor_parts(parts._replace(query=query, fragment=fragment), mapping)
        relative = quote(Path(os.path.relpath(target, doc_path.parent)).as_posix(), safe="/@-._~&") if parts.path else ""
        return relative + ("?" + query if query else "") + ("#" + fragment if fragment else "")

    return edit_link_destinations(text, destination)


def site_sidebar(text, root):
    root = root.resolve()

    def destination(url):
        parts = urlsplit(url)
        if not parts.path:
            return url
        target = local_target(url, root / OUTPUT / "_sidebar.md", root)
        if target is None or not target.is_relative_to(root):
            return url
        path = target.relative_to(root).as_posix()
        if path == (OUTPUT / "README.md").as_posix():
            path = OUTPUT.as_posix() + "/"
        return "/" + quote(path, safe="/") + ("?" + parts.query if parts.query else "") + ("#" + parts.fragment if parts.fragment else "")
    return edit_link_destinations(text, destination)


def validate_document(source_path, translated_path, root):
    root = root.resolve()
    before = document_parts(source_path.read_text())
    text = translated_path.read_text()
    after = document_parts(text)
    for name in ("headings", "code", "inline_code_groups", "html_code", "html_inline_code", "table_rows", "images", "html"):
        if before[name] != after[name]:
            label = "inline_code" if name == "inline_code_groups" else name
            raise ValueError(f"{source_path.name}: translated {label} changed")
    external = lambda links: Counter(url for url in links if url and
                                     (urlsplit(url).scheme or urlsplit(url).netloc))
    if external(before["links"]) != external(after["links"]):
        raise ValueError(f"{source_path.name}: external link destinations changed")
    if "@@COOP_" in text:
        raise ValueError(f"{source_path.name}: unfinished translation markers")
    # Local destinations must still identify the same source files. Existing
    # broken source links are preserved, rather than blocking the whole corpus.
    def canonical(url, document):
        target = local_target(url, document, root)
        if target is None:
            return None
        if target.is_relative_to(root / OUTPUT):
            original = root / target.relative_to(root / OUTPUT)
            if original.is_file() and target.is_file():
                mapping = heading_anchors(original.read_text(), target.read_text())
                parts = urlsplit(url)
                query, fragment = map_anchor_parts(parts, {new: old for old, new in mapping.items()})
                target = original
                return (target, query, unquote(fragment))
            target = original
        parts = urlsplit(url)
        query, fragment = map_anchor_parts(parts, {})
        return (target, query, unquote(fragment))

    original_links = Counter(item for url in before["links"]
                             if (item := canonical(url, source_path)) is not None)
    translated_links = Counter(item for url in after["links"]
                               if (item := canonical(url, translated_path)) is not None)
    if original_links != translated_links:
        raise ValueError(f"{source_path.name}: local link destinations changed")
    navigation = NAV_PATTERN.search(text)
    if navigation:
        after["links"] += document_parts(navigation.group().replace(NAV_START, "").replace(NAV_END, ""))["links"]
    for url in after["links"]:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        target = local_target(url, translated_path, root)
        original = canonical(url, translated_path)[0]
        if not target.exists() and (original.exists() or canonical(url, translated_path) not in original_links):
            raise ValueError(f"{source_path.name}: invalid local link {url}")


def verify_sources_unchanged(root, snapshots):
    for name, digest in snapshots.items():
        path = root / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"Source changed during translation: {name}; no output was published")


def write_atomic(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text() == content:
        return
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    try:
        temporary.chmod(0o644)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def read_json(path):
    return json.loads(path.read_text()) if path.exists() else {}


def publish_translations(staging_root, destination_root, files):
    # Validate the entire batch before replacing any accepted English file.
    for name in files:
        validate_document(staging_root / name, staging_root / OUTPUT / name, staging_root)
    staged_metadata = read_json(staging_root / OUTPUT / METADATA)
    metadata = read_json(destination_root / OUTPUT / METADATA)
    for name in files:
        if name not in staged_metadata:
            raise ValueError(f"Missing translation metadata: {name}")
        expected = hashlib.md5((staging_root / name).read_bytes()).hexdigest()
        if staged_metadata[name].get("original_hash") != expected:
            raise ValueError(f"Stale translation metadata: {name}")
    for name in files:
        write_atomic(destination_root / OUTPUT / name, (staging_root / OUTPUT / name).read_text())
        metadata[name] = staged_metadata[name]
    write_atomic(destination_root / OUTPUT / METADATA, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")


def translation_api_settings():
    base_url = (os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com/v1").strip().rstrip("/")
    model = (os.getenv("DEEPSEEK_MODEL") or "deepseek-flash").strip()
    parts = urlsplit(base_url)
    if (parts.scheme not in {"http", "https"} or not parts.hostname
            or parts.username or parts.password or parts.query or parts.fragment):
        raise ValueError("DEEPSEEK_BASE_URL must be an HTTP(S) API base URL without credentials, query or fragment")
    if not parts.path:
        base_url += "/v1"
    if not model:
        raise ValueError("DEEPSEEK_MODEL must be a nonempty model name")
    return base_url, model


def private_configuration_digest(content, root=None):
    from dotenv import dotenv_values
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key and root is not None:
        key = dotenv_values(root / ".env").get("deepseek-api")
    # Public artifacts must not expose a guessable fingerprint of private URL/model pairs.
    if key:
        return hmac.new(key.encode(), content, hashlib.sha256).hexdigest()
    return hashlib.sha256(content).hexdigest()


def settings_digest(root=None):
    configuration = json.dumps(translation_api_settings(), ensure_ascii=False).encode()
    return private_configuration_digest(Path(__file__).read_bytes() + GLOSSARY.read_bytes() + configuration, root)


def check_outputs(root, files=None):
    root = root.resolve()
    files = files or discover_documents(root)
    metadata = read_json(root / OUTPUT / METADATA)
    if read_json(root / OUTPUT / SETTINGS).get("settings_hash") != settings_digest(root):
        raise ValueError("Translation settings changed; run the translation script")
    for name in files:
        source, target = root / name, root / OUTPUT / name
        validate_document(source, target, root)
        if metadata.get(name, {}).get("original_hash") != hashlib.md5(source.read_bytes()).hexdigest():
            raise ValueError(f"Translation is stale: {name}")
    source = root / "README.md"
    target = root / OUTPUT / "README.md"
    for path, language in ((source, "zh"), (target, "en")):
        text = path.read_text()
        if not NAV_PATTERN.search(text) or apply_language_switch(text, language, source, target) != text:
            raise ValueError(f"Invalid language switch: {path}")
    sidebar = root / OUTPUT / "_sidebar.md"
    if sidebar.is_file() and (root / GENERATED_SIDEBAR).read_text() != site_sidebar(sidebar.read_text(), root):
        raise ValueError("English website sidebar is stale")
    print(f"{len(files)} English docs passed: structure, code, links, navigation and freshness.")


def prepare_workspace(root, staging, files):
    root = root.resolve()
    snapshots = {}
    references = set()
    for name in files:
        source = root / name
        data = source.read_bytes()
        snapshots[name] = hashlib.sha256(data).hexdigest()
        destination = staging / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        for url in document_parts(data.decode())["links"]:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            reference = local_target(url, source, root)
            if reference.is_relative_to(root) and reference.exists() and not reference.is_relative_to(root / OUTPUT):
                references.add(reference)
    for reference in references:
        destination = staging / reference.relative_to(root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if reference.is_dir():
            destination.mkdir(exist_ok=True)
        elif not destination.exists():
            shutil.copyfile(reference, destination)
    for name in (*files, METADATA):
        existing = root / OUTPUT / name
        if existing.is_file():
            destination = staging / OUTPUT / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(existing, destination)
    return snapshots


def configure_deepseek(root):
    from dotenv import dotenv_values
    key = os.getenv("DEEPSEEK_API_KEY") or dotenv_values(root / ".env").get("deepseek-api")
    if not key:
        raise ValueError("Set DEEPSEEK_API_KEY or configure deepseek-api in the local .env")
    base_url, model = translation_api_settings()
    for name in list(os.environ):
        if name.startswith(("OPENAI_", "AZURE_", "ANTHROPIC_", "CO_OP_TRANSLATOR_")):
            del os.environ[name]
    os.environ.update(OPENAI_API_KEY=key, OPENAI_CHAT_MODEL_ID=model,
                      OPENAI_BASE_URL=base_url)
    from openai.resources.chat.completions import AsyncCompletions
    original_create = AsyncCompletions.create

    async def create(self, *args, **kwargs):
        extra = dict(kwargs.get("extra_body") or {})
        extra["thinking"] = {"type": "disabled"}
        kwargs["extra_body"] = extra
        return await original_create(self, *args, **kwargs)

    AsyncCompletions.create = create


def save_rejected_translation(label, source, result, reason):
    context = DIAGNOSTICS.get()
    if context is None:
        return
    directory, name, cache_digest = context
    label = re.sub(r"[^A-Za-z0-9_.-]", "_", label)
    record = {"file": name, "chunk": label, "cache_hash": cache_digest, "reason": redact_error(reason),
              "source": redact_error(source), "result": redact_error(result)}
    write_atomic(directory / f"{label}.json", json.dumps(record, ensure_ascii=False, indent=2) + "\n")


def install_placeholder_guard():
    # Check literals before Co-op leaves its chunk-recovery loop. The upstream
    # final restore raises ValueError too late to retry or split a damaged chunk.
    from co_op_translator.core.llm.markdown_translator import MarkdownTranslator, TranslationIncompleteError
    original = MarkdownTranslator._translate_chunk_once
    if getattr(original, "_checks_translation_placeholders", False):
        return

    async def guarded(self, chunk, language_code, language_name, is_rtl, md_file_path,
                      chunk_label, index, total):
        result = await original(self, chunk, language_code, language_name, is_rtl,
                                md_file_path, chunk_label, index, total)
        expected = Counter(PLACEHOLDERS.findall(chunk))
        actual = Counter(PLACEHOLDERS.findall(result))
        reason = None
        if expected != actual:
            changed = sorted(marker for marker in expected.keys() | actual.keys()
                             if expected[marker] != actual[marker])
            reason = f"changed protected placeholders: {', '.join(changed)}"
        else:
            # Preserve block-code order and each literal's source line, while
            # allowing natural English word order within the same sentence.
            blocks = re.compile(r"@@CODE_BLOCK_\d+@@")
            marker_lines = lambda text: [Counter(PLACEHOLDERS.findall(line)) for line in text.splitlines()]
            if blocks.findall(chunk) != blocks.findall(result):
                reason = "reordered protected code blocks"
            elif marker_lines(chunk) != marker_lines(result):
                reason = "protected placeholders moved between source lines"
            else:
                # A fragment can start inside a list or HTML element. Parsing
                # it as a complete Markdown document gives false code blocks.
                ticks = lambda text: [Counter(re.findall(r"`+", line)) for line in text.splitlines()]
                if ticks(chunk) != ticks(result):
                    reason = "changed unprotected backtick syntax"
        if reason:
            # Do not print provider content or private connection settings.
            save_rejected_translation(chunk_label, chunk, result, reason)
            print(f"Rejected translation chunk {md_file_path.name} ({chunk_label}): {reason}", flush=True)
            raise TranslationIncompleteError(f"{md_file_path.name}: chunk {chunk_label} {reason}")
        return result

    guarded._checks_translation_placeholders = True
    MarkdownTranslator._translate_chunk_once = guarded


def validate_raw_translation(source_text, translated_text, name):
    before, after = document_parts(source_text), document_parts(translated_text)
    for part in ("headings", "code", "inline_code_groups", "html_code", "html_inline_code", "table_rows", "images", "html"):
        if before[part] != after[part]:
            detail = ""
            if part == "inline_code_groups":
                missing = sum((Counter(before["inline_code"]) - Counter(after["inline_code"])).values())
                added = sum((Counter(after["inline_code"]) - Counter(before["inline_code"])).values())
                detail = (f" (source={len(before['inline_code'])}, translated={len(after['inline_code'])}, "
                          f"missing={missing}, unexpected={added}, block_scope_changed={not missing and not added})")
            label = "inline_code" if part == "inline_code_groups" else part
            raise TranslationValidationError(f"{name}: translated {label} changed{detail}")
    if Counter(before["links"]) != Counter(after["links"]):
        raise TranslationValidationError(f"{name}: translator changed link destinations")
    original_markers = Counter(PLACEHOLDERS.findall(source_text))
    if Counter(PLACEHOLDERS.findall(translated_text)) != original_markers:
        raise TranslationValidationError(f"{name}: unfinished literal placeholders")


def checkpoint_directory(root):
    if (root / ".git").is_file():
        path = subprocess.check_output(["git", "rev-parse", "--git-path", "translation-checkpoints"], cwd=root).decode().strip()
        return (root / path).resolve()
    return root / ".git" / "translation-checkpoints"


def checkpoint_digest(root=None):
    # Raw translations survive changes to retries, logging and link rewriting.
    # A changed connection, glossary or translator version invalidates them.
    content = json.dumps(["raw-en-v1", VERSION, *translation_api_settings()], ensure_ascii=False).encode()
    return private_configuration_digest(content + GLOSSARY.read_bytes(), root)


def load_checkpoint(directory, name, source_text, cache_digest):
    path = directory / (name + ".json")
    if not path.is_file():
        return None
    try:
        record = read_json(path)
        text = record["text"]
        if (record.get("schema_version") != 1 or record.get("cache_hash") != cache_digest
                or record.get("source_hash") != hashlib.sha256(source_text.encode()).hexdigest()
                or record.get("text_hash") != hashlib.sha256(text.encode()).hexdigest()
                or not isinstance(record.get("translation_date"), str)):
            return None
        validate_raw_translation(source_text, text, name)
        return record
    except (ValueError, KeyError, TypeError, AttributeError):
        print(f"Ignoring invalid checkpoint: {name}", flush=True)
        return None


def recover_rejected_checkpoint(directory, name, source_text, cache_digest, legacy_digest=None):
    path = directory / "_rejected" / name / "document.json"
    if not path.is_file():
        return None
    try:
        record = read_json(path)
    except ValueError:
        return None
    if not isinstance(record, dict):
        return None
    text = record.get("result")
    if (record.get("cache_hash", legacy_digest) != cache_digest or record.get("file") != name
            or record.get("chunk") != "document" or record.get("source") != source_text
            or not isinstance(text, str) or "[redacted]" in text):
        return None
    try:
        validate_raw_translation(source_text, text, name)
    except ValueError:
        return None
    recovered = {"schema_version": 1, "cache_hash": cache_digest,
                 "source_hash": hashlib.sha256(source_text.encode()).hexdigest(),
                 "text_hash": hashlib.sha256(text.encode()).hexdigest(), "text": text,
                 "translation_date": datetime.now(timezone.utc).isoformat()}
    write_atomic(directory / (name + ".json"), json.dumps(recovered, ensure_ascii=False, indent=2) + "\n")
    print(f"Recovered validated rejected translation: {name}", flush=True)
    return recovered


async def translate_documents(staging, pending, digest, checkpoint_dir, cache_digest, force=False):
    # Use Co-op's content API: the wrapper owns file discovery and URL rewriting,
    # including Markdown under .github/ and other paths the upstream CLI excludes.
    from co_op_translator.api import translate_markdown_content
    install_placeholder_guard()
    semaphore = asyncio.Semaphore(3)
    metadata = read_json(staging / OUTPUT / METADATA)
    failures = {}

    async def translate(name):
        async with semaphore:
            DIAGNOSTICS.set((checkpoint_dir / "_rejected" / name, name, cache_digest))
            source = staging / name
            source_text = source.read_text()
            record = None if force else load_checkpoint(checkpoint_dir, name, source_text, cache_digest)
            if not force and record is None:
                record = recover_rejected_checkpoint(checkpoint_dir, name, source_text, cache_digest)
            if record:
                text = record["text"]
                print(f"Restored checkpoint: {name}", flush=True)
            else:
                for attempt in range(1, FILE_ATTEMPTS + 1):
                    text = None
                    try:
                        protected, html_literals = protect_html_code(source_text)
                        context = (GLOSSARY.read_text() + "\nKeep each @@HTML_CODE_n@@ marker exactly once on its source line. "
                                   "Do not put backticks around any placeholder.\n")
                        text = await translate_markdown_content(protected, "en", options={
                            "source_path": source, "context": context})
                        text = restore_html_code(text, html_literals)
                        validate_raw_translation(source_text, text, name)
                        record = {"schema_version": 1, "cache_hash": cache_digest,
                                  "source_hash": hashlib.sha256(source_text.encode()).hexdigest(),
                                  "text_hash": hashlib.sha256(text.encode()).hexdigest(), "text": text,
                                  "translation_date": datetime.now(timezone.utc).isoformat()}
                        write_atomic(checkpoint_dir / (name + ".json"),
                                     json.dumps(record, ensure_ascii=False, indent=2) + "\n")
                        print(f"Translated and checkpointed: {name}", flush=True)
                        break
                    except Exception as error:
                        if text is not None:
                            save_rejected_translation("document", source_text, text, str(error))
                        retryable = isinstance(error, TranslationValidationError) or (
                            isinstance(error, ValueError) and "Expected code placeholder" in str(error))
                        if retryable and attempt < FILE_ATTEMPTS:
                            print(f"Retrying document {name} ({attempt + 1}/{FILE_ATTEMPTS}): {redact_error(str(error))}", flush=True)
                            await asyncio.sleep(attempt)
                            continue
                        failures[name] = redact_error(str(error))
                        print(f"Failed document: {name}: {failures[name]}", file=sys.stderr, flush=True)
                        return
            write_atomic(staging / OUTPUT / name, text)
            metadata[name] = {"original_hash": hashlib.md5(source.read_bytes()).hexdigest(),
                              "translation_date": record["translation_date"],
                              "source_file": name, "language_code": "en", "settings_hash": digest,
                              "anchors": heading_anchors(source_text, text)}

    await asyncio.gather(*(translate(name) for name in pending))
    write_atomic(staging / OUTPUT / METADATA, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    if failures:
        details = "\n".join(f"{name}: {message}" for name, message in sorted(failures.items()))
        raise RuntimeError(f"Translation failed for {len(failures)} document(s); valid checkpoints were retained.\n{details}")


def prune_translations(root, files):
    metadata = read_json(root / OUTPUT / METADATA)
    for name in list(metadata):
        if is_source_document(name) and name not in files:
            (root / OUTPUT / name).unlink(missing_ok=True)
            del metadata[name]
    write_atomic(root / OUTPUT / METADATA, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")


def probe_docs(root, names, checkpoint_dir=None):
    """Validate representative translations without publishing English files."""
    root = root.resolve()
    if importlib.metadata.version("co-op-translator") != VERSION:
        raise ValueError(f"Install scripts/translation-requirements.txt (Co-op Translator {VERSION})")
    files = tuple(dict.fromkeys(names))
    managed = set(discover_documents(root))
    if not files or any(name not in managed for name in files):
        raise ValueError("Probe documents must be Git-tracked source Markdown files")
    directory = Path(checkpoint_dir).resolve() if checkpoint_dir is not None else checkpoint_directory(root)
    digest = settings_digest(root)
    print(f"Representative document preflight: {len(files)} document(s).", flush=True)
    with tempfile.TemporaryDirectory(prefix="translate-docs-probe-") as temporary:
        staging = Path(temporary).resolve()
        snapshots = prepare_workspace(root, staging, files)
        configure_deepseek(root)
        asyncio.run(translate_documents(staging, files, digest, directory, checkpoint_digest(root)))
        verify_sources_unchanged(root, snapshots)
        if settings_digest(root) != digest:
            raise RuntimeError("Translation settings changed during preflight")
    print(f"Representative preflight passed: {len(files)} document(s); validated checkpoints retained, no English files published.", flush=True)


def sync_docs(root, dry_run=False, force=False, checkpoint_dir=None):
    root = root.resolve()
    if importlib.metadata.version("co-op-translator") != VERSION:
        raise ValueError(f"Install scripts/translation-requirements.txt (Co-op Translator {VERSION})")
    digest = settings_digest(root)
    files = discover_documents(root)
    metadata = read_json(root / OUTPUT / METADATA)
    pending = [name for name in files if force or not (root / OUTPUT / name).is_file()
               or metadata.get(name, {}).get("settings_hash") != digest
               or metadata.get(name, {}).get("original_hash") != hashlib.md5((root / name).read_bytes()).hexdigest()]
    print(f"Managed Markdown: {len(files)}; pending output updates: {len(pending)}.")
    if dry_run:
        directory = Path(checkpoint_dir).resolve() if checkpoint_dir is not None else checkpoint_directory(root)
        cache_digest = checkpoint_digest(root)
        cached = [name for name in pending if not force and
                  load_checkpoint(directory, name, (root / name).read_text(), cache_digest) is not None]
        print(f"Valid checkpoints: {len(cached)}; need API translation: {len(pending) - len(cached)}.")
        print(f"Pending source bytes: {sum((root / name).stat().st_size for name in pending):,}.")
        for name in pending:
            print(f"  {name}")
        print("Preview only: no API calls or repository files written.")
        return
    source_readme = root / "README.md"
    readme_text = source_readme.read_text()
    if not NAV_PATTERN.search(readme_text) or apply_language_switch(
            readme_text, "zh", source_readme, root / OUTPUT / "README.md") != readme_text:
        raise ValueError("Invalid Chinese README language switch; no output was published")
    checkpoint_dir = Path(checkpoint_dir).resolve() if checkpoint_dir is not None else checkpoint_directory(root)
    with tempfile.TemporaryDirectory(prefix="translate-docs-") as directory:
        staging = Path(directory).resolve()
        snapshots = prepare_workspace(root, staging, files)
        if pending:
            configure_deepseek(root)
            asyncio.run(translate_documents(staging, pending, digest, checkpoint_dir, checkpoint_digest(root), force))
        for name in files:
            path = staging / OUTPUT / name
            text = repair_local_links(path.read_text(), path, staging,
                                      source_path=staging / name if name in pending else None,
                                      translated_files=files,
                                      previous_anchors={name: item.get("anchors", {}) for name, item in metadata.items()
                                                        if isinstance(item, dict)})
            if name == "README.md":
                text = apply_language_switch(text, "en", staging / name, path)
            path.write_text(text)
        verify_sources_unchanged(root, snapshots)
        if settings_digest(root) != digest or discover_documents(root) != files:
            raise RuntimeError("Translation settings or file list changed during the run; no output was published")
        publish_translations(staging, root, files)
        prune_translations(root, files)
        sidebar = root / OUTPUT / "_sidebar.md"
        if sidebar.is_file():
            write_atomic(root / GENERATED_SIDEBAR, site_sidebar(sidebar.read_text(), root))
        write_atomic(root / OUTPUT / SETTINGS, json.dumps({"settings_hash": digest,
                     "translator_version": VERSION, "files": list(files)}, ensure_ascii=False, indent=2) + "\n")
    check_outputs(root, files)
    if not pending:
        print("Source unchanged; no translation API calls needed.")


def redact_error(message):
    values = set()
    for variable in ("DEEPSEEK_API_KEY", "OPENAI_API_KEY", "DEEPSEEK_BASE_URL",
                     "OPENAI_BASE_URL", "DEEPSEEK_MODEL", "OPENAI_CHAT_MODEL_ID"):
        value = os.getenv(variable)
        if not value:
            continue
        values.add(value)
        if variable.endswith("BASE_URL"):
            try:
                hostname = urlsplit(value).hostname
                if hostname:
                    values.add(hostname)
            except ValueError:
                pass
    for value in sorted(values, key=len, reverse=True):
        message = message.replace(value, "[redacted]")
    return message


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    modes = args.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="Validate English docs without API calls")
    modes.add_argument("--dry-run", action="store_true", help="Preview translation volume without writing files")
    modes.add_argument("--probe", nargs="+", metavar="SOURCE", help="Validate selected tracked documents and retain checkpoints without publishing")
    modes.add_argument("--recover-rejected", nargs="+", metavar="SOURCE", help="Revalidate reviewed rejected documents without API calls or publication")
    args.add_argument("--legacy-cache-hash", help="Verified original configuration fingerprint for diagnostics created before provenance tracking")
    args.add_argument("--force", action="store_true", help="Regenerate all managed English docs")
    args.add_argument("--checkpoint-dir", type=Path, help="Persist validated raw translations for interrupted-run recovery")
    options = args.parse_args()
    try:
        root = options.root.resolve()
        if options.check:
            check_outputs(root)
        elif options.probe:
            probe_docs(root, options.probe, options.checkpoint_dir)
        elif options.recover_rejected:
            directory = options.checkpoint_dir.resolve() if options.checkpoint_dir else checkpoint_directory(root)
            managed = set(discover_documents(root))
            for name in options.recover_rejected:
                if name not in managed or recover_rejected_checkpoint(
                        directory, name, (root / name).read_text(), checkpoint_digest(root), options.legacy_cache_hash) is None:
                    raise ValueError(f"Cannot safely recover rejected translation: {name}")
        else:
            sync_docs(root, options.dry_run, options.force, options.checkpoint_dir)
    except Exception as error:
        message = redact_error(str(error))
        print(f"Translation stopped: {message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
