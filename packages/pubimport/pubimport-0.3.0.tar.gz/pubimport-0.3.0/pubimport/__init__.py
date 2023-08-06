import pathlib

import bibtexparser
import click
from click import command, argument, File
from dominate.tags import div, section, p, h2, li, h3, ul


@command()
@argument('source_dir', type=click.Path(exists=True))
@argument('destination', type=File('w'))
def cli(source_dir, destination):
    root = pathlib.Path(source_dir)
    container = div(id='publications')
    for source in root.iterdir():
        topic_title = source.name.split('-')[1]
        topic_title.replace('_', ' ')
        topic_section = section()
        topic_section.add(h2(topic_title))
        paper_list = ul()
        topic_section.add(paper_list)
        with source.open() as f:
            data = bibtexparser.load(f)
        for entry in data.entries:
            list_item = li()
            paper_list.add(list_item)
            paper_title = h3(entry['title'])
            list_item.add(paper_title)
            authors = p(entry['author'])
            list_item.add(authors)
            if 'journal' in entry:
                journal = p(entry['journal'])
                list_item.add(journal)
        container.add(topic_section)
    destination.write(str(container))
