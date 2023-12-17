import argparse
import logging

from rhoknp import BasePhrase, Document, Phrase

from utils import list_files

logging.getLogger("rhoknp").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", type=str, nargs="+", help="paths to knp files or directories")
    args = parser.parse_args()

    for path in sorted(list_files(args.paths)):
        document = Document.from_knp(path.read_text())
        for sentence in document.sentences:
            verify_phrases_or_base_phrases(sentence.phrases)
            verify_phrases_or_base_phrases(sentence.base_phrases)


def verify_phrases_or_base_phrases(phrases_or_base_phrases: list[Phrase] | list[BasePhrase]) -> None:
    last_phrase = phrases_or_base_phrases[-1]
    if last_phrase.parent is not None:
        logger.warning(f"no root: {last_phrase.sentence.sid}")
        return
    for phrase in phrases_or_base_phrases:
        parent = phrase
        while parent.parent is not None:
            parent = parent.parent
            if parent == phrase:
                logger.warning(f"loop: {phrase.sentence.sid}")
                return
        if parent != last_phrase:
            logger.warning(f"multiple roots: {phrase.sentence.sid}")
            return


if __name__ == "__main__":
    main()
