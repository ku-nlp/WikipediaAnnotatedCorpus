from pathlib import Path
import sys

from rhoknp import Document


def main():
    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    for path in input_dir.glob("**/*.knp"):
        document = Document.from_knp(path.read_text())
        output_path: Path = output_dir.joinpath(path.relative_to(input_dir)).with_suffix(".org")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        org_text = ""
        for sentence in document.sentences:
            org_text += sentence.comment + "\n"
            org_text += sentence.text + "\n"
        output_path.write_text(org_text)


if __name__ == "__main__":
    main()
