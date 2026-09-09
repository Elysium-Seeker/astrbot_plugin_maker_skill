"""Exercise the shipped commands and generated plugins in fresh directories."""

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".github" / "skills" / "astrbot-plugin-maker"
SCAFFOLD = SKILL / "scripts" / "scaffold_plugin.py"
VALIDATOR = SKILL / "scripts" / "validate_plugin.py"


def run_python(*args, cwd=ROOT):
    return subprocess.run(
        [sys.executable, *map(str, args)],
        cwd=cwd,
        env={**os.environ, "PYTHONUTF8": "1"},
        text=True,
        encoding="utf-8",
        capture_output=True,
        timeout=90,
        check=False,
    )


def assert_success(result):
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.fixture
def make_plugin(tmp_path):
    def make(*extra, name="astrbot_plugin_test"):
        destination = tmp_path / name
        result = run_python(
            SCAFFOLD,
            destination,
            "--author",
            "Example Author",
            "--description",
            "A plugin for workflow verification",
            *extra,
        )
        assert_success(result)
        return destination

    return make


@pytest.mark.parametrize("with_openapi", [False, True])
def test_generated_plugin_workflow(make_plugin, with_openapi):
    plugin = make_plugin(*(["--with-openapi"] if with_openapi else []))
    assert_success(run_python(VALIDATOR, plugin))
    assert_success(run_python("-m", "pytest", "-q", cwd=plugin))
    assert_success(run_python("-m", "ruff", "check", ".", cwd=plugin))
    assert_success(run_python("-m", "ruff", "format", "--check", ".", cwd=plugin))
    assert (plugin / "requirements.txt").exists() is with_openapi
    assert (plugin / "openapi_client.py").exists() is with_openapi
    assert (plugin / "runtime_tests" / "test_plugin_runtime.py").is_file()


def test_user_metadata_is_preserved_without_template_injection(make_plugin):
    description = '中文: "quoted"\nsecond line {{command}} {{repo_line}}'
    plugin = make_plugin("--description", description, "--command", "welcome")
    metadata = yaml.safe_load((plugin / "metadata.yaml").read_text(encoding="utf-8"))
    assert metadata["desc"] == description
    assert "repo" not in metadata
    assert_success(run_python(VALIDATOR, plugin))


def test_existing_directory_is_untouched(make_plugin):
    plugin = make_plugin()
    files_before = {
        p.relative_to(plugin): p.read_bytes() for p in plugin.rglob("*") if p.is_file()
    }
    result = run_python(
        SCAFFOLD, plugin, "--author", "Other", "--description", "Changed"
    )
    assert result.returncode != 0
    files_after = {
        p.relative_to(plugin): p.read_bytes() for p in plugin.rglob("*") if p.is_file()
    }
    assert files_after == files_before


@pytest.mark.parametrize(
    ("name", "command"),
    [("bad name", "greet"), ("astrbot_plugin_ok", 'greet"); broken("')],
)
def test_invalid_scaffold_input_leaves_no_directory(tmp_path, name, command):
    destination = tmp_path / name
    result = run_python(
        SCAFFOLD,
        destination,
        "--author",
        "Author",
        "--description",
        "Test",
        "--command",
        command,
    )
    assert result.returncode != 0
    assert not destination.exists()


@pytest.mark.parametrize(
    ("filename", "content"),
    [
        ("main.py", "def broken(:\n"),
        ("metadata.yaml", "name: [unfinished\n"),
        ("metadata.yaml", "name: demo\nname: other\n"),
        ("metadata.yaml", "name: demo\ndesc: Example\nauthor: Author\nversion: 1.0\n"),
        ("_conf_schema.json", '{"limit": {"type": "int", "default": true}}'),
        ("_conf_schema.json", '{"nested": {"type": "object"}}'),
        (
            "_conf_schema.json",
            '{"choices": {"type": "template_list", "templates": []}}',
        ),
    ],
)
def test_static_validation_rejects_broken_files(make_plugin, filename, content):
    plugin = make_plugin()
    (plugin / filename).write_text(content, encoding="utf-8")
    assert run_python(VALIDATOR, plugin).returncode != 0


def test_missing_entrypoint_is_rejected(make_plugin):
    plugin = make_plugin()
    (plugin / "main.py").unlink()
    assert run_python(VALIDATOR, plugin).returncode != 0


def test_missing_metadata_is_reported(make_plugin):
    plugin = make_plugin()
    (plugin / "metadata.yaml").unlink()
    result = run_python(VALIDATOR, plugin)
    assert result.returncode != 0
    assert "metadata.yaml or metadata.yml is missing" in result.stdout


@pytest.mark.parametrize("constraint", [">=v4.28.0", "4.28 or newer", ""])
def test_invalid_compatibility_constraint(make_plugin, constraint):
    plugin = make_plugin()
    metadata_path = plugin / "metadata.yaml"
    metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    metadata["astrbot_version"] = constraint
    metadata_path.write_text(yaml.safe_dump(metadata), encoding="utf-8")
    assert run_python(VALIDATOR, plugin).returncode != 0


def test_optional_metadata_and_legacy_alias_are_preserved(make_plugin):
    plugin = make_plugin()
    path = plugin / "metadata.yaml"
    metadata = yaml.safe_load(path.read_text(encoding="utf-8"))
    metadata["description"] = metadata.pop("desc")
    metadata["support_platforms"] = ["webchat", "qq_official_webhook"]
    metadata["social_link"] = "https://example.com/author"
    metadata["tags"] = ["example"]
    metadata["future_extension"] = {"enabled": True}
    path.unlink()
    (plugin / "metadata.yml").write_text(yaml.safe_dump(metadata), encoding="utf-8")
    assert_success(run_python(VALIDATOR, plugin))


def test_release_check_needs_repo_only_when_requested(make_plugin):
    plugin = make_plugin()
    assert_success(run_python(VALIDATOR, plugin))
    assert run_python(VALIDATOR, plugin, "--require-repo").returncode != 0
    with (plugin / "metadata.yaml").open("a", encoding="utf-8") as stream:
        stream.write("repo: https://github.com/example/astrbot_plugin_test\n")
    assert_success(run_python(VALIDATOR, plugin, "--require-repo"))


@pytest.mark.parametrize("with_openapi", [False, True])
def test_generated_tests_detect_production_regression(make_plugin, with_openapi):
    plugin = make_plugin(*(["--with-openapi"] if with_openapi else []))
    if with_openapi:
        source = plugin / "openapi_client.py"
        content = source.read_text(encoding="utf-8").replace(
            "return bot_ids", "return []"
        )
    else:
        source = plugin / "plugin_logic.py"
        content = source.read_text(encoding="utf-8").replace(
            'return f"{greeting}, {display_name}!"', 'return "wrong reply"'
        )
    source.write_text(content, encoding="utf-8")
    result = run_python("-m", "pytest", "-q", cwd=plugin)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "failed" in result.stdout


def test_skill_frontmatter_and_local_resource_links():
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = yaml.safe_load(skill_text.split("---", 2)[1])
    assert frontmatter["name"] == SKILL.name
    assert isinstance(frontmatter["description"], str)
    for source in SKILL.rglob("*.md"):
        for link in re.findall(
            r"\[[^\]]+\]\(([^)]+)\)", source.read_text(encoding="utf-8")
        ):
            if "://" in link or link.startswith("#"):
                continue
            target = (source.parent / link.split("#")[0]).resolve()
            assert target.is_relative_to(SKILL), (source, link)
            assert target.is_file(), (source, link)
