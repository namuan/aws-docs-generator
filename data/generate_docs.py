"""
Given an input directory
It will create an output directory
With a section for each language
And a Markdown page for each code snippet.
"""
from argparse import ArgumentParser
from pathlib import Path

from slugify import slugify

from data.entities import CodeDocumentItem


def write_documentation(destination_dir: Path, code_document: CodeDocumentItem):
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination_path: Path = destination_dir.joinpath(
        "{}.md".format(slugify(code_document.topic))
    )
    destination_path.write_text(code_document.doc)


def process():
    pass


def parse_args():
    parser = ArgumentParser()
    return parser.parse_args()


def main(args):
    process()


if __name__ == "__main__":
    args = parse_args()
    main(args)
