"""Print the HTML report to PDF with a headless Chromium (Chrome or Edge) and count the pages."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

CANDIDATES = [
    os.environ.get("EQR_CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_browser() -> str | None:
    for c in CANDIDATES:
        if c and Path(c).exists():
            return c
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"):
        w = shutil.which(name)
        if w:
            return w
    return None


def to_pdf(html_path: Path, pdf_path: Path, browser: str | None = None, timeout=180) -> Path:
    browser = browser or find_browser()
    if not browser:
        raise RuntimeError("no Chromium browser found – set EQR_CHROME to chrome.exe / msedge.exe, or build with --html-only")
    html_path, pdf_path = Path(html_path).resolve(), Path(pdf_path).resolve()
    with tempfile.TemporaryDirectory() as prof:
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-sandbox", "--disable-extensions", f"--user-data-dir={prof}",
               "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw", "--virtual-time-budget=8000",
               f"--print-to-pdf={pdf_path}", html_path.as_uri()]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if not pdf_path.exists():
        raise RuntimeError(f"PDF not written: {res.stderr[-500:]}")
    return pdf_path


def page_count(pdf_path: Path) -> int | None:
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf_path)).pages)
    except Exception:  # noqa: BLE001
        pass
    try:
        import fitz  # pymupdf
        with fitz.open(str(pdf_path)) as doc:
            return len(doc)
    except Exception:  # noqa: BLE001
        return None


def page_images(pdf_path: Path, out_dir: Path, pages=(1, 2), dpi=110) -> list[Path]:
    """PNG of selected pages (needs pymupdf). Used for the README screenshots."""
    import fitz
    out = []
    out_dir.mkdir(parents=True, exist_ok=True)
    with fitz.open(str(pdf_path)) as doc:
        for p in pages:
            if p - 1 < len(doc):
                f = out_dir / f"{pdf_path.stem}_p{p:02d}.png"
                doc[p - 1].get_pixmap(dpi=dpi).save(str(f))
                out.append(f)
    return out
