"""
Given an input directory
It will create an output directory
With a section for each language
And a Markdown page for each code snippet.
"""
import base64
import hashlib
import re
from argparse import ArgumentParser
from pathlib import Path

from data.entities import save_code_document, CodeDocumentItem


def _flatten_sources(source_dir, file_type):
    return [file for file in source_dir.glob(file_type)]


def match_line(line, regex):
    matches = regex.findall(line)
    if matches:
        return matches[0]
    else:
        return None


rgx_source_description = re.compile('snippet-sourcedescription:\[([\w+\.\s\'\-]+)\]*')
rgx_source_service = re.compile('snippet-service:\[(.*)\]')
rgx_source_syntax = re.compile('snippet-sourcesyntax:\[(.*)\]')


def extract_snippet(code_doc: CodeDocumentItem, f: Path):
    description = ''
    syntax = ''
    service = ''
    for line in f.read_text(encoding='utf-8').split('\n'):
        description = match_line(line, rgx_source_description) if not description else description
        service = match_line(line, rgx_source_service) if not service else service
        syntax = match_line(line, rgx_source_syntax) if not syntax else syntax
        if not (description or service or syntax):
            print("===> NO MATCH: {}".format(line))

    code_doc.cloud_service = service
    code_doc.source_syntax = syntax
    code_doc.description = description


def filter_code(code_doc: CodeDocumentItem, f: Path):
    return ""


def process_file(code_doc: CodeDocumentItem, f):
    extract_snippet(code_doc, f)
    filter_code(code_doc, f)


def generate_documentation(f, syntax) -> CodeDocumentItem:
    doc_sha = hashlib.blake2b(bytes(f.read_text(), encoding="utf-8")).hexdigest()
    topic = f.stem

    code_doc = CodeDocumentItem(doc_sha=doc_sha, topic=topic, source_syntax=syntax)
    process_file(code_doc, f)

    parsed_source = """
import boto3

ec2 = boto3.client('ec2')
response = ec2.describe_instances()
print(response)    
    """

    md = f"""
### {code_doc.topic}

{code_doc.description}

```{code_doc.source_syntax}
{parsed_source}
```
    """

    doc_in_bytes = bytes(md, encoding="utf-8")
    encoded_doc = base64.standard_b64encode(doc_in_bytes)
    code_doc.doc_md = encoded_doc
    return code_doc


guides = [
    dict(source_dir="python", file_glob="**/*.py", syntax="python"),
    dict(source_dir="php", file_glob="**/*.php", syntax="php"),
    dict(source_dir="ruby", file_glob="**/*.rb", syntax="ruby"),
]


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
