import pathlib

from pypdf import PdfReader

MAX_CHARS = 12000


def main():
    out = pathlib.Path("text")
    out.mkdir(exist_ok=True)
    for pdf in sorted(pathlib.Path("reports").glob("*.pdf")):
        try:
            reader = PdfReader(pdf)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            print(f"skip {pdf.name}: {e}")
            continue
        tmp = out / (pdf.stem + ".txt.tmp")
        tmp.write_text(text[:MAX_CHARS])
        tmp.replace(out / (pdf.stem + ".txt"))
        print(f"extracted {len(text)} chars from {pdf.name}")


if __name__ == "__main__":
    main()
