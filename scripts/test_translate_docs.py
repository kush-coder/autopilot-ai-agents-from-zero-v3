"""Focused checks for the documentation translation integration (no API calls)."""

import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import json
import asyncio
import os
from types import SimpleNamespace, MethodType


MODULE_PATH = Path(__file__).with_name("translate_docs.py")
docs = None
if MODULE_PATH.exists():
    spec = importlib.util.spec_from_file_location("translate_docs", MODULE_PATH)
    docs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(docs)


class TranslationSafetyTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(docs, "The translation integration is not implemented yet")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "translations/en"
        self.output.mkdir(parents=True)

    def test_chinese_navigation_is_idempotent_and_preserves_the_body(self):
        original = '<div align="center">\n\n![Banner](image.png)\n\n</div>\n\nOriginal body.\n'
        result = docs.apply_language_switch(
            original, "zh", self.root / "README.md", self.output / "README.md"
        )
        self.assertIn("**简体中文** · [English](translations/en/README.md)", result)
        self.assertEqual(result.count(docs.NAV_START), 1)
        self.assertTrue(result.endswith("Original body.\n"))
        self.assertEqual(
            docs.apply_language_switch(result, "zh", self.root / "README.md", self.output / "README.md"),
            result,
        )

    def test_english_navigation_returns_to_the_chinese_readme(self):
        result = docs.apply_language_switch(
            "# Guide\n\nEnglish body.\n", "en", self.root / "README.md", self.output / "README.md"
        )
        self.assertIn("[简体中文](../../README.md) · **English**", result)

    def test_untranslated_links_fall_back_without_touching_code_or_existing_translations(self):
        (self.root / "FAQ.md").write_text("# FAQ\n")
        (self.root / "Other Guide.md").write_text("# Other guide\n")
        (self.output / "Chapter.md").write_text("# Chapter\n")
        text = (
            '[Help](FAQ.md#details) [English](Chapter.md)\n'
            '<a href="FAQ.md">Help</a>\n'
            '[reference]: <Other Guide.md> "Guide"\n'
            '`[literal](FAQ.md)`\n'
            '```md\n[example](FAQ.md)\n```\n'
        )
        result = docs.repair_local_links(text, self.output / "README.md", self.root)
        self.assertIn("[Help](../../FAQ.md#details)", result)
        self.assertIn("[English](Chapter.md)", result)
        self.assertIn('<a href="../../FAQ.md">', result)
        self.assertIn('<../../Other%20Guide.md>', result)
        self.assertIn('`[literal](FAQ.md)`', result)
        self.assertIn('```md\n[example](FAQ.md)\n```', result)
        self.assertEqual(docs.repair_local_links(result, self.output / "README.md", self.root), result)

    def test_changed_executable_code_is_rejected(self):
        source = self.root / "README.md"
        translated = self.output / "README.md"
        source.write_text("# 原文\n\n```python\nprint('hello')\n```\n")
        translated.write_text("# Translation\n\n```python\nprint('changed')\n```\n")
        with self.assertRaisesRegex(ValueError, "code"):
            docs.validate_document(source, translated, self.root)

    def test_missing_local_link_is_rejected(self):
        source = self.root / "README.md"
        translated = self.output / "README.md"
        source.write_text("# 原文\n\nText.\n")
        translated.write_text("# Translation\n\n[Broken](missing.md)\n")
        with self.assertRaisesRegex(ValueError, "link"):
            docs.validate_document(source, translated, self.root)

    def test_failed_validation_does_not_overwrite_existing_output(self):
        staged = self.root / "staging"
        (staged / "translations/en").mkdir(parents=True)
        (staged / "README.md").write_text("# 原文\n\n```sh\necho safe\n```\n")
        (staged / "translations/en/README.md").write_text("# English\n\n```sh\nrm danger\n```\n")
        existing = self.output / "README.md"
        existing.write_text("Existing accepted translation.\n")
        with self.assertRaises(ValueError):
            docs.publish_translations(staged, self.root, ["README.md"])
        self.assertEqual(existing.read_text(), "Existing accepted translation.\n")

    def test_concurrent_source_edit_is_detected_and_preserved(self):
        path = self.root / "README.md"
        path.write_text("Original.\n")
        snapshot = {"README.md": hashlib.sha256(path.read_bytes()).hexdigest()}
        path.write_text("A user's newer edit.\n")
        with self.assertRaisesRegex(RuntimeError, "changed"):
            docs.verify_sources_unchanged(self.root, snapshot)
        self.assertEqual(path.read_text(), "A user's newer edit.\n")

    def test_gateway_configuration_sends_openai_request_to_the_configured_url(self):
        import httpx
        from openai import AsyncOpenAI
        from openai.resources.chat.completions import AsyncCompletions
        requests = []

        def handle(request):
            requests.append(request)
            return httpx.Response(200, json={
                "id": "test", "object": "chat.completion", "created": 0,
                "model": "example-model", "choices": [{"index": 0,
                "message": {"role": "assistant", "content": "English"}, "finish_reason": "stop"}]})

        async def call():
            async with AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"],
                                   base_url=os.environ["OPENAI_BASE_URL"],
                                   http_client=httpx.AsyncClient(transport=httpx.MockTransport(handle))) as client:
                result = await client.chat.completions.create(
                    model=os.environ["OPENAI_CHAT_MODEL_ID"],
                    messages=[{"role": "user", "content": "Translate"}])
                self.assertEqual(result.choices[0].message.content, "English")

        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-gateway-key",
                                    "DEEPSEEK_BASE_URL": "https://gateway.example.invalid/",
                                    "DEEPSEEK_MODEL": "example-model"}, clear=True), \
             patch.object(AsyncCompletions, "create", AsyncCompletions.create):
            docs.configure_deepseek(self.root)
            asyncio.run(call())
        self.assertEqual(str(requests[0].url), "https://gateway.example.invalid/v1/chat/completions")
        self.assertEqual(requests[0].headers["Authorization"], "Bearer test-gateway-key")
        payload = json.loads(requests[0].content)
        self.assertEqual(payload["model"], "example-model")
        self.assertEqual(payload["thinking"], {"type": "disabled"})

    def test_official_api_defaults_remain_available(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(docs.translation_api_settings(),
                             ("https://api.deepseek.com/v1", "deepseek-flash"))

    def test_model_or_url_changes_invalidate_translation_cache(self):
        with patch.dict(os.environ, {"DEEPSEEK_BASE_URL": "https://gateway.example.invalid/v1",
                                    "DEEPSEEK_MODEL": "example-model"}, clear=True):
            original = docs.settings_digest()
            os.environ["DEEPSEEK_MODEL"] = "deepseek-flash"
            changed_model = docs.settings_digest()
            self.assertNotEqual(original, changed_model)
            os.environ["DEEPSEEK_BASE_URL"] = "https://api.deepseek.com/v1"
            self.assertNotEqual(changed_model, docs.settings_digest())

    def test_errors_do_not_reveal_private_connection_settings(self):
        private_url = "https://gateway.example.invalid/v1"
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-private-key",
                                    "DEEPSEEK_BASE_URL": private_url,
                                    "DEEPSEEK_MODEL": "example-private-model"}, clear=True):
            result = docs.redact_error(
                "Request to " + private_url + "/chat/completions at gateway.example.invalid "
                "failed for example-private-model using test-private-key")
        self.assertNotIn(private_url, result)
        self.assertNotIn("gateway.example.invalid", result)
        self.assertNotIn("example-private-model", result)
        self.assertNotIn("test-private-key", result)

    def test_discovery_covers_tracked_nested_docs_but_not_generated_or_local_files(self):
        names = ["README.md", "项目/指南.MD", "_sidebar.md", "_sidebar.en.md",
                 "translations/en/README.md", "scripts/translation-glossary.md"]
        for name in names + ["untracked.md"]:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# 文档\n")
        with patch.object(docs.subprocess, "check_output", return_value="\0".join(names).encode()):
            self.assertEqual(docs.discover_documents(self.root),
                             ("README.md", "_sidebar.md", "项目/指南.MD"))

    def test_nested_workspace_and_resource_directories_are_preserved(self):
        source = self.root / "项目/指南.md"
        source.parent.mkdir()
        (source.parent / "code").mkdir()
        source.write_text("# 指南\n\n[Code](code/)\n")
        staged = self.root / "staging"
        staged.mkdir()
        snapshots = docs.prepare_workspace(self.root, staged, ["项目/指南.md"])
        self.assertEqual((staged / "项目/指南.md").read_bytes(), source.read_bytes())
        self.assertTrue((staged / "项目/code").is_dir())
        self.assertIn("项目/指南.md", snapshots)

    def test_new_english_docs_replace_chinese_fallback_links_and_share_assets(self):
        (self.root / "FAQ.md").write_text("# FAQ\n")
        (self.root / "image.png").write_bytes(b"image")
        text = "[FAQ](../../FAQ.md) ![Image](../../image.png)\n"
        result = docs.repair_local_links(text, self.output / "README.md", self.root,
                                        translated_files={"README.md", "FAQ.md"})
        self.assertIn("[FAQ](FAQ.md)", result)
        self.assertIn("![Image](../../image.png)", result)

    def test_content_translation_links_use_the_source_location(self):
        text = '[FAQ](../FAQ.md) [Code](code/demo.py) ![Image](/image.png)\n'
        result = docs.repair_local_links(text, self.output / "项目/指南.md", self.root,
                                        source_path=self.root / "项目/指南.md",
                                        translated_files={"项目/指南.md", "FAQ.md"})
        self.assertIn("[FAQ](../FAQ.md)", result)
        self.assertIn("[Code](../../../项目/code/demo.py)".replace("项目", "%E9%A1%B9%E7%9B%AE"), result)
        self.assertIn("![Image](../../../image.png)", result)

    def test_backticks_inside_a_fence_do_not_hide_later_image_links(self):
        text = 'An unmatched ` before a fence.\n\n````text\n`unpaired\n````\n\n![Image](images/example.png)\n\n````text\nend\n````\n'
        result = docs.repair_local_links(text, self.output / "README.md", self.root,
                                        source_path=self.root / "README.md",
                                        translated_files={"README.md"})
        self.assertIn("![Image](../../images/example.png)", result)
        self.assertIn('````text\n`unpaired\n````', result)

    def test_existing_broken_source_link_is_preserved_but_new_broken_link_is_rejected(self):
        source = self.root / "README.md"
        target = self.output / "README.md"
        source.write_text("# 原文\n\n[Old](missing.md)\n")
        target.write_text("# English\n\n[Old](../../missing.md)\n")
        docs.validate_document(source, target, self.root)
        target.write_text("# English\n\n[New](../../different.md)\n")
        with self.assertRaisesRegex(ValueError, "link"):
            docs.validate_document(source, target, self.root)

    def test_generated_site_sidebar_uses_english_routes(self):
        text = "- [Home](README.md)\n- [Chapter](项目/指南.md)\n"
        result = docs.site_sidebar(text, self.root)
        self.assertIn("[Home](/translations/en/)", result)
        self.assertIn("[Chapter](/translations/en/", result)
        self.assertNotIn("../../", result)

    def test_translated_heading_links_follow_english_titles(self):
        source = self.root / "README.md"
        target = self.output / "README.md"
        source.write_text("# 中文指南\n\n[Section](FAQ.md#_4、配置)\n")
        (self.root / "FAQ.md").write_text("# 4、配置\n")
        (self.output / "FAQ.md").write_text("# 4. Configuration\n")
        text = "# English guide\n\n[Section](FAQ.md#_4、配置)\n"
        result = docs.repair_local_links(text, target, self.root, source_path=source,
                                        translated_files={"README.md", "FAQ.md"})
        self.assertIn("FAQ.md#_4-configuration", result)
        target.write_text(result)
        docs.validate_document(source, target, self.root)

    def test_same_page_heading_links_and_duplicate_titles_remain_valid(self):
        source = self.root / "README.md"
        target = self.output / "README.md"
        source.write_text("# 中文指南\n\n[Again](#中文指南-1)\n\n# 中文指南\n")
        target.write_text("# English guide\n\n[Again](#中文指南-1)\n\n# English guide\n")
        result = docs.repair_local_links(target.read_text(), target, self.root,
                                        source_path=source, translated_files={"README.md"})
        self.assertIn("[Again](#english-guide-1)", result)
        target.write_text(result)
        docs.validate_document(source, target, self.root)

    def test_cached_heading_links_can_be_rebased_without_an_api_call(self):
        source = self.root / "README.md"
        target = self.output / "README.md"
        (self.root / "FAQ.md").write_text("# 配置\n")
        (self.output / "FAQ.md").write_text("# New configuration\n")
        source.write_text("# 指南\n\n[Section](FAQ.md#配置)\n")
        target.write_text("# Guide\n\n[Section](FAQ.md#configuration)\n")
        result = docs.repair_local_links(target.read_text(), target, self.root,
                                        translated_files={"README.md", "FAQ.md"},
                                        previous_anchors={"FAQ.md": {"配置": "configuration"}})
        self.assertIn("FAQ.md#new-configuration", result)
        target.write_text(result)
        docs.validate_document(source, target, self.root)

    def test_incremental_sync_translates_new_and_changed_files_only(self):
        files = ["README.md", "_sidebar.md", "项目/指南.md"]
        for name in files:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# 文档\n\nText.\n")
        readme = self.root / "README.md"
        readme.write_text(docs.apply_language_switch(readme.read_text(), "zh", readme,
                                                   self.output / "README.md"))
        calls = []

        async def translate(text, language, options):
            calls.append(Path(options["source_path"]).name)
            return text.replace("# 文档", "# Guide")

        with patch.object(docs, "discover_documents", side_effect=lambda root: tuple(files)), \
             patch.object(docs, "configure_deepseek"), \
             patch("co_op_translator.api.translate_markdown_content", side_effect=translate):
            docs.sync_docs(self.root)
            self.assertCountEqual(calls, ["README.md", "_sidebar.md", "指南.md"])
            calls.clear()
            before = (self.output / "项目/指南.md").stat().st_mtime_ns
            docs.sync_docs(self.root)
            self.assertEqual(calls, [])
            self.assertEqual((self.output / "项目/指南.md").stat().st_mtime_ns, before)
            readme.write_text(readme.read_text() + "\nUpdated.\n")
            docs.sync_docs(self.root)
            self.assertEqual(calls, ["README.md"])
            calls.clear()
            files.append("New.md")
            (self.root / "New.md").write_text("# 文档\n")
            docs.sync_docs(self.root)
            self.assertEqual(calls, ["New.md"])
            files.remove("New.md")
            (self.root / "New.md").unlink()
            calls.clear()
            docs.sync_docs(self.root)
            self.assertEqual(calls, [])
            self.assertFalse((self.output / "New.md").exists())
            self.assertNotIn("New.md", json.loads((self.output / docs.METADATA).read_text()))

    def test_lost_code_marker_is_retried_by_the_existing_chunk_recovery(self):
        from co_op_translator.core.llm.markdown_translator import MarkdownTranslator
        chunk = "Use @@INLINE_CODE_240@@ and @@LINK_DESTINATION_0@@.\n"
        calls = []

        async def provider(self, content, *args, **kwargs):
            calls.append(content)
            return content.replace("@@INLINE_CODE_240@@", "") if len(calls) == 1 else content

        with patch.object(MarkdownTranslator, "_translate_chunk_once", provider):
            docs.install_placeholder_guard()
            instance = SimpleNamespace(CHUNK_RETRY_ATTEMPTS=1)
            instance._translate_chunk_once = MethodType(MarkdownTranslator._translate_chunk_once, instance)
            result = asyncio.run(MarkdownTranslator._translate_chunk_with_recovery(
                instance, chunk, "en", "English", False, self.root / "Guide.md", "1", 1, 1, 0))
        self.assertEqual(result, chunk)
        self.assertEqual(len(calls), 2)

    def test_backticks_added_around_a_placeholder_are_retried_before_restoration(self):
        from co_op_translator.core.llm.markdown_translator import MarkdownTranslator
        from co_op_translator.utils.markdown import SPLIT_DELIMITER
        original = "# Guide\n\nUse `safe()` and `argument`.\n"
        calls = []

        async def provider(self, prompt, index, total):
            content = prompt.split(SPLIT_DELIMITER, 1)[1]
            calls.append(content)
            if len(calls) == 1:
                return content.replace("@@INLINE_CODE_0@@", "`@@INLINE_CODE_0@@`")
            return content

        with patch.object(MarkdownTranslator, "_translate_chunk_once", MarkdownTranslator._translate_chunk_once), \
                patch.object(MarkdownTranslator, "_run_prompt", provider):
            docs.install_placeholder_guard()
            translator = type("Translator", (MarkdownTranslator,), {"_run_prompt": provider})()
            result = asyncio.run(translator.translate_markdown(original, "en", self.root / "Guide.md"))
        self.assertEqual(len(calls), 2)
        self.assertEqual(result, original)
        docs.validate_raw_translation(original, result, "Guide.md")

    def test_new_inline_code_is_retried_without_retranslating_completed_chunks(self):
        from co_op_translator.core.llm.markdown_translator import MarkdownTranslator
        from co_op_translator.utils.markdown import SPLIT_DELIMITER
        chunks = ["First paragraph.\n", "Second paragraph with @@INLINE_CODE_0@@.\n"]
        calls = []

        async def provider(self, prompt, index, total):
            content = prompt.split(SPLIT_DELIMITER, 1)[1]
            calls.append(index)
            if index == 2 and calls.count(2) == 1:
                return content.replace("Second paragraph", "Second `paragraph`")
            return content

        with patch.object(MarkdownTranslator, "_translate_chunk_once", MarkdownTranslator._translate_chunk_once), \
                patch.object(MarkdownTranslator, "_run_prompt", provider):
            docs.install_placeholder_guard()
            translator = type("Translator", (MarkdownTranslator,), {"_run_prompt": provider})()
            result = asyncio.run(translator._translate_chunks_with_recovery(
                chunks, "en", "English", False, self.root / "Guide.md"))
        self.assertEqual(calls, [1, 2, 2])
        self.assertEqual(result, chunks)

    def test_natural_english_can_reorder_inline_code_within_the_same_sentence(self):
        from co_op_translator.core.llm.markdown_translator import MarkdownTranslator
        from co_op_translator.utils.markdown import SPLIT_DELIMITER
        original = "输入 `question`，得到 `answer`。\n"
        english = "The `answer` is produced from the `question`.\n"
        calls = []

        async def provider(self, prompt, index, total):
            content = prompt.split(SPLIT_DELIMITER, 1)[1]
            calls.append(content)
            return content.replace("输入 @@INLINE_CODE_0@@，得到 @@INLINE_CODE_1@@。",
                                   "The @@INLINE_CODE_1@@ is produced from the @@INLINE_CODE_0@@.")

        with patch.object(MarkdownTranslator, "_translate_chunk_once", MarkdownTranslator._translate_chunk_once), \
                patch.object(MarkdownTranslator, "_run_prompt", provider):
            docs.install_placeholder_guard()
            translator = type("Translator", (MarkdownTranslator,), {"_run_prompt": provider})()
            result = asyncio.run(translator.translate_markdown(original, "en", self.root / "Guide.md"))
        self.assertEqual(len(calls), 1)
        self.assertEqual(result, english)
        docs.validate_raw_translation(original, result, "Guide.md")
        (self.root / "Guide.md").write_text(original)
        (self.output / "Guide.md").write_text(result)
        docs.validate_document(self.root / "Guide.md", self.output / "Guide.md", self.root)

    def test_inline_code_cannot_move_between_paragraphs_or_table_cells(self):
        pairs = [
            ("Use `first`.\n\nThen `second`.\n", "Use `second`.\n\nThen `first`.\n"),
            ("| Input | Output |\n| --- | --- |\n| `question` | `answer` |\n",
             "| Input | Output |\n| --- | --- |\n| `answer` | `question` |\n"),
        ]
        for source, translated in pairs:
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, "inline_code"):
                docs.validate_raw_translation(source, translated, "Guide.md")

    def test_changed_html_code_is_rejected(self):
        for element in ("pre", "code"):
            source = f"<{element}>print('safe')</{element}>\n"
            translated = source.replace("'safe'", "'changed'")
            with self.subTest(element=element), self.assertRaisesRegex(ValueError, "html.*code"):
                docs.validate_raw_translation(source, translated, "Guide.md")

    def test_html_code_is_hidden_from_translation_and_restored_verbatim(self):
        original = ('# 文档\n\n<details>\n<summary>中文说明</summary>\n'
                    '<pre><code style="white-space: pre-wrap;">{\n'
                    '  "content": "中文数据",\n  "role": "assistant"\n}\n</code></pre>\n'
                    '</details>\n\n使用 <code>保持原样</code>。\n')
        (self.root / "Guide.md").write_text(original)
        inputs = []

        async def provider(text, *args, **kwargs):
            inputs.append(text)
            return text.replace("中文说明", "Explanation").replace("中文数据", "damaged data").replace(
                "保持原样", "damaged literal")

        with patch("co_op_translator.api.translate_markdown_content", provider):
            asyncio.run(docs.translate_documents(self.root, ("Guide.md",), "settings",
                                                self.root / "checkpoints", "cache"))
        result = (self.output / "Guide.md").read_text()
        self.assertNotIn("中文数据", inputs[0])
        self.assertNotIn("保持原样", inputs[0])
        self.assertEqual(result, original.replace("中文说明", "Explanation"))
        docs.validate_raw_translation(original, result, "Guide.md")

    def test_html_code_examples_keep_their_literal_link_destinations(self):
        (self.root / "Guide.md").write_text("# Guide\n")
        text = '<pre><code>[example](Guide.md)</code></pre>\n'
        result = docs.repair_local_links(text, self.output / "README.md", self.root)
        self.assertEqual(result, text)

    def test_indented_list_fragment_can_translate_prose_without_becoming_code(self):
        from co_op_translator.core.llm.markdown_translator import MarkdownTranslator
        from co_op_translator.utils.markdown import SPLIT_DELIMITER
        chunk = "    这是列表中的说明。\n"

        async def provider(self, prompt, index, total):
            return prompt.split(SPLIT_DELIMITER, 1)[1].replace("这是列表中的说明。", "Explanation in a list.")

        with patch.object(MarkdownTranslator, "_translate_chunk_once", MarkdownTranslator._translate_chunk_once):
            docs.install_placeholder_guard()
            translator = type("Translator", (MarkdownTranslator,), {"_run_prompt": provider})()
            result = asyncio.run(translator._translate_chunk_with_recovery(
                chunk, "en", "English", False, self.root / "Guide.md", "1", 1, 1, 0))
        self.assertEqual(result, "    Explanation in a list.\n")

    def test_html_tags_inside_markdown_code_are_not_protected_twice(self):
        text = '`<code>literal</code>`\n\n```html\n<pre>示例</pre>\n```\n'
        protected, literals = docs.protect_html_code(text)
        self.assertEqual(protected, text)
        self.assertEqual(literals, {})

    def test_html_accessibility_labels_can_translate_without_changing_structure(self):
        source = '<div role="region" aria-label="中文说明" style="overflow-x: auto;">正文</div>\n'
        translated = source.replace("中文说明", "English description").replace("正文", "Body")
        docs.validate_raw_translation(source, translated, "Guide.md")
        (self.root / "Guide.md").write_text(source)
        (self.output / "Guide.md").write_text(translated)
        docs.validate_document(self.root / "Guide.md", self.output / "Guide.md", self.root)

    def test_html_accessibility_labels_and_layout_attributes_cannot_be_removed(self):
        source = '<div role="region" aria-label="说明" style="overflow-x: auto;">Body</div>\n'
        for translated in (source.replace(' aria-label="说明"', ''),
                           source.replace('role="region"', 'role="button"'),
                           source.replace('overflow-x: auto;', 'overflow-x: hidden;')):
            with self.subTest(translated=translated), self.assertRaisesRegex(ValueError, "html"):
                docs.validate_raw_translation(source, translated, "Guide.md")

    def test_code_markers_cannot_move_between_source_lines(self):
        from co_op_translator.core.llm.markdown_translator import MarkdownTranslator
        from co_op_translator.utils.markdown import SPLIT_DELIMITER
        original = "First `input`.\n\nSecond `output`.\n"
        calls = []

        async def provider(self, prompt, index, total):
            content = prompt.split(SPLIT_DELIMITER, 1)[1]
            calls.append(content)
            if len(calls) == 1:
                return content.replace("@@INLINE_CODE_0@@", "@@SWAP@@").replace(
                    "@@INLINE_CODE_1@@", "@@INLINE_CODE_0@@").replace("@@SWAP@@", "@@INLINE_CODE_1@@")
            return content

        with patch.object(MarkdownTranslator, "_translate_chunk_once", MarkdownTranslator._translate_chunk_once):
            docs.install_placeholder_guard()
            translator = type("Translator", (MarkdownTranslator,), {"_run_prompt": provider})()
            result = asyncio.run(translator.translate_markdown(original, "en", self.root / "Guide.md"))
        self.assertEqual(len(calls), 2)
        self.assertEqual(result, original)

    def test_probe_reuses_checkpoints_and_never_publishes_unvalidated_results(self):
        files = ("Good.md", "Bad.md")
        for name in files:
            (self.root / name).write_text("# Guide\n\nUse `safe`.\n")
        (self.output / "Good.md").write_text("Accepted English.\n")
        calls = []

        async def provider(text, language, options):
            name = options["source_path"].name
            calls.append(name)
            if name == "Bad.md":
                raise RuntimeError("simulated provider failure")
            return text

        with patch.object(docs, "discover_documents", return_value=files), \
                patch.object(docs, "configure_deepseek"), \
                patch("co_op_translator.api.translate_markdown_content", provider):
            docs.probe_docs(self.root, ("Good.md",), self.root / "checkpoints")
            calls.clear()
            with self.assertRaisesRegex(RuntimeError, "Bad.md"):
                docs.probe_docs(self.root, files, self.root / "checkpoints")
        self.assertEqual(calls, ["Bad.md"])
        self.assertEqual((self.output / "Good.md").read_text(), "Accepted English.\n")
        self.assertTrue((self.root / "checkpoints/Good.md.json").exists())
        self.assertFalse((self.output / "Bad.md").exists())

    def test_rejected_samples_redact_secrets_and_preserve_accepted_outputs(self):
        source = "# Guide\n\nUse `safe`.\nprivate-key https://private.invalid/v1 private-model\n"
        (self.root / "Guide.md").write_text(source)
        (self.output / "Guide.md").write_text("Accepted English.\n")

        async def provider(text, *args, **kwargs):
            return text.replace("`safe`", "`changed`")

        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "private-key",
                                    "DEEPSEEK_BASE_URL": "https://private.invalid/v1",
                                    "DEEPSEEK_MODEL": "private-model"}), \
                patch.object(docs, "FILE_ATTEMPTS", 1), \
                patch("co_op_translator.api.translate_markdown_content", provider):
            with self.assertRaises(RuntimeError):
                asyncio.run(docs.translate_documents(self.root, ("Guide.md",), "settings",
                                                    self.root / "checkpoints", "cache"))
        sample = (self.root / "checkpoints/_rejected/Guide.md/document.json").read_text()
        for private in ("private-key", "private.invalid", "private-model"):
            self.assertNotIn(private, sample)
        self.assertIn("[redacted]", sample)
        self.assertEqual((self.output / "Guide.md").read_text(), "Accepted English.\n")
        self.assertFalse((self.root / "checkpoints/Guide.md.json").exists())

    def test_complete_rejected_translation_can_be_recovered_after_validator_correction(self):
        source = '<div aria-label="中文说明">正文</div>\n'
        translated = '<div aria-label="English description">Body</div>\n'
        directory = self.root / "checkpoints"
        sample = directory / "_rejected/Guide.md/document.json"
        docs.write_atomic(sample, json.dumps({"file": "Guide.md", "chunk": "document",
                                             "source": source, "result": translated}))
        self.assertIsNone(docs.recover_rejected_checkpoint(directory, "Guide.md", source, "cache"))
        self.assertIsNone(docs.recover_rejected_checkpoint(directory, "Guide.md", source, "cache", "other"))
        record = docs.recover_rejected_checkpoint(directory, "Guide.md", source, "cache", "cache")
        self.assertEqual(record["text"], translated)
        self.assertEqual(docs.load_checkpoint(directory, "Guide.md", source, "cache"), record)
        self.assertFalse((self.output / "Guide.md").exists())

    def test_recovery_rejects_stale_sources_redactions_and_damaged_code(self):
        source = "# Guide\n\nUse `safe`.\n"
        directory = self.root / "checkpoints"
        sample = directory / "_rejected/Guide.md/document.json"
        for changed in ({"source": "Old source"}, {"result": source + "[redacted]"},
                        {"result": source.replace("`safe`", "`changed`")}, {"cache_hash": "other"}):
            record = {"file": "Guide.md", "chunk": "document", "source": source,
                      "result": source, "cache_hash": "cache", **changed}
            docs.write_atomic(sample, json.dumps(record))
            with self.subTest(changed=changed):
                self.assertIsNone(docs.recover_rejected_checkpoint(directory, "Guide.md", source, "cache"))
        self.assertFalse((directory / "Guide.md.json").exists())

    def test_malformed_rejected_samples_do_not_abort_translation_recovery(self):
        directory = self.root / "checkpoints"
        sample = directory / "_rejected/Guide.md/document.json"
        for content in ('{"broken":', '[]'):
            docs.write_atomic(sample, content)
            with self.subTest(content=content):
                self.assertIsNone(docs.recover_rejected_checkpoint(directory, "Guide.md", "# Guide\n", "cache"))

    def test_damaged_markers_cause_smaller_chunks_after_bounded_retries(self):
        from co_op_translator.core.llm.markdown_translator import MarkdownTranslator
        chunk = "@@INLINE_CODE_0@@\n@@INLINE_CODE_1@@\n"
        calls = []

        async def provider(self, content, *args, **kwargs):
            calls.append(content)
            return content.replace("@@INLINE_CODE_0@@", "") if content == chunk else content

        with patch.object(MarkdownTranslator, "_translate_chunk_once", provider):
            docs.install_placeholder_guard()
            instance = SimpleNamespace(CHUNK_RETRY_ATTEMPTS=1)
            instance._translate_chunk_once = MethodType(MarkdownTranslator._translate_chunk_once, instance)
            instance._translate_chunk_with_recovery = MethodType(MarkdownTranslator._translate_chunk_with_recovery, instance)
            instance._split_failed_chunk = lambda content, depth: ["@@INLINE_CODE_0@@\n", "@@INLINE_CODE_1@@\n"]
            result = asyncio.run(instance._translate_chunk_with_recovery(
                chunk, "en", "English", False, self.root / "Guide.md", "1", 1, 1, 0))
        self.assertEqual(result, chunk)
        self.assertEqual(calls, [chunk, chunk, "@@INLINE_CODE_0@@\n", "@@INLINE_CODE_1@@\n"])

    def test_failed_batch_keeps_valid_checkpoints_and_resumes_only_the_failed_file(self):
        files = ("README.md", "Good.md", "Bad.md", "Later.md")
        for name in files:
            (self.root / name).write_text("# 文档\n\nUse `safe`.\n")
        readme = self.root / "README.md"
        readme.write_text(docs.apply_language_switch(readme.read_text(), "zh", readme, self.output / "README.md"))
        (self.output / "Good.md").write_text("Existing accepted translation.\n")
        checkpoint = self.root / "checkpoint"
        calls = []
        fail = True

        async def provider(text, language, options):
            name = Path(options["source_path"]).name
            calls.append(name)
            if name == "Bad.md" and fail:
                raise RuntimeError("simulated provider failure")
            return text.replace("# 文档", "# Guide")

        with patch.object(docs, "discover_documents", return_value=files), \
             patch.object(docs, "configure_deepseek"), \
             patch("co_op_translator.api.translate_markdown_content", side_effect=provider):
            with self.assertRaisesRegex(RuntimeError, "Bad.md"):
                docs.sync_docs(self.root, checkpoint_dir=checkpoint)
            self.assertEqual((self.output / "Good.md").read_text(), "Existing accepted translation.\n")
            self.assertCountEqual([p.name for p in checkpoint.glob("*.json")],
                                  ["README.md.json", "Good.md.json", "Later.md.json"])
            self.assertFalse((checkpoint / "Bad.md.json").exists())
            fail = False
            calls.clear()
            docs.sync_docs(self.root, checkpoint_dir=checkpoint)
            self.assertEqual(calls, ["Bad.md"])
            docs.check_outputs(self.root, files)

    def test_cached_text_is_revalidated_and_source_changes_invalidate_it(self):
        files = ("README.md", "Guide.md")
        for name in files:
            (self.root / name).write_text("# 文档\n\nUse `safe`.\n")
        readme = self.root / "README.md"
        readme.write_text(docs.apply_language_switch(readme.read_text(), "zh", readme, self.output / "README.md"))
        checkpoint = self.root / "checkpoint"
        calls = []

        async def provider(text, language, options):
            calls.append(Path(options["source_path"]).name)
            return text.replace("# 文档", "# Guide")

        with patch.object(docs, "discover_documents", return_value=files), \
             patch.object(docs, "configure_deepseek"), \
             patch("co_op_translator.api.translate_markdown_content", side_effect=provider):
            docs.sync_docs(self.root, checkpoint_dir=checkpoint)
            record_path = checkpoint / "Guide.md.json"
            record = json.loads(record_path.read_text())
            record["text"] = record["text"].replace("`safe`", "`danger`")
            record["text_hash"] = hashlib.sha256(record["text"].encode()).hexdigest()
            record_path.write_text(json.dumps(record))
            for name in files:
                (self.output / name).unlink()
            calls.clear()
            docs.sync_docs(self.root, checkpoint_dir=checkpoint)
            self.assertEqual(calls, ["Guide.md"])
            (self.root / "Guide.md").write_text("# 文档\n\nUse `new`.\n")
            calls.clear()
            docs.sync_docs(self.root, checkpoint_dir=checkpoint)
            self.assertEqual(calls, ["Guide.md"])

    def test_invalid_code_output_is_retried_and_never_checkpointed(self):
        files = ("README.md",)
        source = self.root / "README.md"
        source.write_text(docs.apply_language_switch("# 文档\n\nUse `safe`.\n", "zh", source, self.output / "README.md"))
        checkpoint = self.root / "checkpoint"
        calls = []

        async def provider(text, language, options):
            calls.append(text)
            return text.replace("`safe`", "`danger`")

        with patch.object(docs, "discover_documents", return_value=files), \
             patch.object(docs, "configure_deepseek"), patch.object(docs.asyncio, "sleep"), \
             patch("co_op_translator.api.translate_markdown_content", side_effect=provider):
            with self.assertRaisesRegex(RuntimeError, "README.md.*code"):
                docs.sync_docs(self.root, checkpoint_dir=checkpoint)
        self.assertEqual(len(calls), 3)
        self.assertFalse((checkpoint / "README.md.json").exists())
        self.assertFalse((self.output / "README.md").exists())

    def test_model_changes_and_force_do_not_reuse_old_checkpoints(self):
        files = ("README.md",)
        source = self.root / "README.md"
        source.write_text(docs.apply_language_switch("# 文档\n\nUse `safe`.\n", "zh", source, self.output / "README.md"))
        checkpoint = self.root / "checkpoint"
        calls = []

        async def provider(text, language, options):
            calls.append(text)
            return text.replace("# 文档", "# Guide")

        with patch.dict(os.environ, {"DEEPSEEK_BASE_URL": "https://gateway.example.invalid/v1",
                                    "DEEPSEEK_MODEL": "example-model", "DEEPSEEK_API_KEY": "test-key"}, clear=True), \
             patch.object(docs, "discover_documents", return_value=files), \
             patch.object(docs, "configure_deepseek"), \
             patch("co_op_translator.api.translate_markdown_content", side_effect=provider):
            docs.sync_docs(self.root, checkpoint_dir=checkpoint)
            os.environ["DEEPSEEK_MODEL"] = "different-model"
            calls.clear()
            docs.sync_docs(self.root, checkpoint_dir=checkpoint)
            self.assertEqual(len(calls), 1)
            calls.clear()
            docs.sync_docs(self.root, force=True, checkpoint_dir=checkpoint)
            self.assertEqual(len(calls), 1)
            content = (checkpoint / "README.md.json").read_text()
            self.assertNotIn("gateway.example.invalid", content)
            self.assertNotIn("different-model", content)
            self.assertNotIn("test-key", content)

    def test_public_checkpoint_fingerprints_require_the_private_key(self):
        with patch.dict(os.environ, {"DEEPSEEK_BASE_URL": "https://gateway.example.invalid/v1",
                                    "DEEPSEEK_MODEL": "example-model", "DEEPSEEK_API_KEY": "test-key-one"}, clear=True):
            first = docs.checkpoint_digest()
            os.environ["DEEPSEEK_API_KEY"] = "test-key-two"
            self.assertNotEqual(first, docs.checkpoint_digest())
            os.environ["DEEPSEEK_API_KEY"] = "test-key-one"
            self.assertEqual(first, docs.checkpoint_digest())

    def test_local_dotenv_credentials_keep_checkpoint_and_output_hashes_consistent(self):
        from openai.resources.chat.completions import AsyncCompletions
        files = ("README.md",)
        source = self.root / "README.md"
        source.write_text(docs.apply_language_switch("# 文档\n\nUse `safe`.\n", "zh", source, self.output / "README.md"))
        (self.root / ".env").write_text("deepseek-api=local-test-key\n")
        checkpoint = self.root / "checkpoint"

        async def provider(text, language, options):
            return text.replace("# 文档", "# Guide")

        with patch.dict(os.environ, {}, clear=True), \
             patch.object(AsyncCompletions, "create", AsyncCompletions.create), \
             patch.object(docs, "discover_documents", return_value=files), \
             patch("co_op_translator.api.translate_markdown_content", side_effect=provider):
            docs.sync_docs(self.root, checkpoint_dir=checkpoint)
            docs.check_outputs(self.root, files)
            record = docs.load_checkpoint(checkpoint, "README.md", source.read_text(),
                                          docs.checkpoint_digest(self.root))
            self.assertIsNotNone(record)
            self.assertNotIn("local-test-key", (checkpoint / "README.md.json").read_text())

    def test_duplicate_code_and_link_markers_trigger_chunk_recovery(self):
        from co_op_translator.core.llm.markdown_translator import MarkdownTranslator
        chunk = "@@CODE_BLOCK_0@@\n[Link](@@LINK_DESTINATION_0@@)\n"
        for marker in ["@@CODE_BLOCK_0@@", "@@LINK_DESTINATION_0@@"]:
            with self.subTest(marker=marker):
                calls = []

                async def provider(self, content, *args, **kwargs):
                    calls.append(content)
                    return content.replace(marker, marker + marker) if len(calls) == 1 else content

                with patch.object(MarkdownTranslator, "_translate_chunk_once", provider):
                    docs.install_placeholder_guard()
                    instance = SimpleNamespace(CHUNK_RETRY_ATTEMPTS=1)
                    instance._translate_chunk_once = MethodType(MarkdownTranslator._translate_chunk_once, instance)
                    result = asyncio.run(MarkdownTranslator._translate_chunk_with_recovery(
                        instance, chunk, "en", "English", False, self.root / "Guide.md", "1", 1, 1, 0))
                self.assertEqual(result, chunk)
                self.assertEqual(len(calls), 2)


if __name__ == "__main__":
    unittest.main()
