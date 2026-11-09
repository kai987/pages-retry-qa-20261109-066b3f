"""Verify and package the only page in the isolated deployment fixture."""
import hashlib
import json
import os
from pathlib import Path

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")

commit = os.environ["GITHUB_SHA"]
page = Path("index.html").read_bytes()
assert b"Isolated Pages deployment recovery fixture." in page
assert b"noindex, nofollow" in page
assert len(page) < 1024
root = Path("output/site")
(root / "runtime").mkdir(parents=True)
(root / "index.html").write_bytes(page)
files = {"index.html": {"bytes": len(page), "sha256": hashlib.sha256(page).hexdigest()}}
encoded = (json.dumps(files, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
write_json(root / "runtime/build.json", {
    "schema": "tk2-static-build-v1",
    "commit": commit,
    "content_sha256": hashlib.sha256(encoded).hexdigest(),
    "files": files,
})
write_json(Path("output/test-plan.json"), {
    "schema": "tk2-test-plan-v1",
    "head": commit,
    "publish": os.environ["REQUEST_PUBLICATION"] == "true",
    "docs_only": False,
})
