# build.py
#!/usr/bin/env python3
from pathlib import Path
from markdown import Markdown
from weasyprint import HTML

PROJECT_ROOT = Path(__file__).resolve().parent
INPUT = PROJECT_ROOT / "README.md"
HTML_OUTPUT = PROJECT_ROOT / "cv_raw_html.html"
PDF_OUTPUT = PROJECT_ROOT / "cv.pdf"
PDF_STYLE = PROJECT_ROOT / "pdf_style.css"
HTML_OUTPUT_TEMP = PROJECT_ROOT / "cv_raw_html.html.tmp"
PDF_OUTPUT_TEMP = PROJECT_ROOT / "cv.pdf.tmp"


REQUIRED_FONTS = [
    "fonts/LiberationSans-Regular.ttf",
    "fonts/LiberationSans-Italic.ttf",
    "fonts/LiberationSans-Bold.ttf",
    "fonts/LiberationSans-BoldItalic.ttf",
    "fonts/Inter-Regular.ttf",
    "fonts/Inter-Italic.ttf",
    "fonts/Inter-Bold.ttf",
    "fonts/Inter-BoldItalic.ttf",
]


def assert_dependency_files():
    if not INPUT.exists():
        raise SystemExit(f"Missing input: {INPUT}")
    for rel in REQUIRED_FONTS:
        p = PROJECT_ROOT / rel
        if not p.exists():
            raise SystemExit(f"Missing font: {p}")


def md_to_html(md_text):
    md = Markdown(
        extensions=[
            "extra",
            "sane_lists",
            "smarty",
        ],
        output_format="html5",
    )
    return md.convert(md_text)


def write_html_file(html_body, output_file):
    output_file.write_text(html_body, encoding="utf-8")


def write_pdf_file(html_body, pdf_style, output_file):
    html_doc = (
        f"""<!DOCTYPE html>"""
        f"""<html lang="en">"""
        f"""<head>"""
        f"""<meta charset="utf-8" />"""
        f"""<meta name="viewport" content="width=device-width, initial-scale=1" />"""
        f"""<style>"""
        f"""{pdf_style}"""
        f"""</style>"""
        f"""</head>"""
        f"""<body>"""
        f"""{html_body}"""
        f"""</body>"""
        f"""</html>"""
    )
    HTML(string=html_doc, base_url=str(PROJECT_ROOT)).write_pdf(output_file)


def clean_up(file):
    if file.exists():
        file.unlink()


def assert_intermediary(file):
    if not file.exists() or file.stat().st_size == 0:
        raise SystemExit(f"{file.name} not generated or empty")


def main():
    clean_up(HTML_OUTPUT_TEMP)
    clean_up(PDF_OUTPUT_TEMP)
    assert_dependency_files()
    md_text = INPUT.read_text(encoding="utf-8")
    html_body = md_to_html(md_text)
    write_html_file(html_body, HTML_OUTPUT_TEMP)
    pdf_style = PDF_STYLE.read_text(encoding="utf-8")
    write_pdf_file(html_body, pdf_style, PDF_OUTPUT_TEMP)
    assert_intermediary(HTML_OUTPUT_TEMP)
    HTML_OUTPUT_TEMP.replace(HTML_OUTPUT)
    assert_intermediary(PDF_OUTPUT_TEMP)
    PDF_OUTPUT_TEMP.replace(PDF_OUTPUT)
    clean_up(HTML_OUTPUT_TEMP)
    clean_up(PDF_OUTPUT_TEMP)

if __name__ == "__main__":
    main()
