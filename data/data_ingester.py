"""
Given an input directory
It will create an output directory
With a section for each language
And a Markdown page for each code snippet.
"""
import base64
import hashlib
from argparse import ArgumentParser
from pathlib import Path

from data.entities import save_code_document, CodeDocumentItem


def _flatten_sources(source_dir, file_type):
    return [file for file in source_dir.glob(file_type)]


def extract_snippet(f):
    pass


def filter_code(f):
    pass


def process_file(f):
    snippets_map = extract_snippet(f)
    code = filter_code(f)
    return snippets_map, code


def generate_documentation(f, syntax) -> CodeDocumentItem:
    doc_sha = hashlib.blake2b(bytes(f.read_text(), encoding="utf-8")).hexdigest()
    source_syntax = syntax
    topic = f.stem
    description = "How to retrieve details about your Amazon EC2 instances"
    parsed_source = """
import boto3

ec2 = boto3.client('ec2')
response = ec2.describe_instances()
print(response)    
    """

    md = f"""
### {topic}

{description}

```{source_syntax}
{parsed_source}
```
    """

    doc_in_bytes = bytes(md, encoding="utf-8")
    encoded_doc = base64.standard_b64encode(doc_in_bytes)
    return CodeDocumentItem(source_syntax="python", topic=topic, doc_md=encoded_doc, doc_sha=doc_sha)


guides = [dict(source_dir="python", file_glob="**/*.py", syntax="python")]


def process():
    for guide in guides:
        source_dir = Path.cwd().joinpath(
            "raw", "aws-doc-sdk-examples", guide.get("source_dir")
        )
        flatten_sources = _flatten_sources(source_dir, guide.get("file_glob"))
        for f in flatten_sources:
            doc = generate_documentation(f, guide.get("source_syntax"))
            save_code_document(doc)


def parse_args():
    parser = ArgumentParser()
    return parser.parse_args()


def main(args):
    process()


if __name__ == "__main__":
    args = parse_args()
    main(args)
