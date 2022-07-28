'''This script generates recursive summary for directory tree of markdown files'''
from collections import defaultdict
from pathlib import Path


def get_markdown_tree(path: Path) -> dict[Path, list[Path]]:
    # gets all files recursively, sorted by nesting level and parent name
    all_paths = reversed(list(path.glob('**/*')))

    markdown_tree = defaultdict(set)
    has_markdown = set()
    root_depth = len(path.parents)
    for path_ in all_paths:
        if path_.suffix == '.md':
            # mark all parents, as having md files inside
            has_markdown.update({*list(path_.parents)[:-root_depth]})
            # put the file into its parents group
            markdown_tree[path_.parent].add(path_)
        elif path_ in has_markdown:
            # if dir contains(or recursively contains) md files, it should also be added
            # into its parents' SUMMARY.md. This way, we add link to its inner summary,
            # e.q. path_/SUMMARY.md
            markdown_tree[path_.parent].add(path_/'SUMMARY.md')

    return markdown_tree


def generate_summary(md_files: set[Path], root: Path, wikilinks=True):
    '''
    Generates SUMMARY.md for markdown files provide.

    Parameters
    -----------
    md_files
        set of paths to markdown files, from which the links would be constructed
    root
        root directory, all links would be relative to
    wikilinks
        if true, write [[wikilinks]] instead of [markdown]() ones
    '''
    if not wikilinks:
        link_format = '* [{text}]({link}.md)'
    else:
        link_format = '* [[{link}|{text}]]'

    links = []
    for md_file_path in md_files:
        # make path relative to root and get rid of suffix
        root_relative_path = Path(*md_file_path.parts[len(root.parents)+1:])
        root_relative_path = root_relative_path.with_suffix('')
        if root_relative_path.stem == 'SUMMARY':
            name = root_relative_path.parent.stem
        else:
            name = root_relative_path.stem.replace('_', ' ').capitalize()
        links.append(link_format.format(text=name, link=root_relative_path))

    return '\n'.join(links)


def write_summary(summary_dir: Path, summary: str):
    '''Writes summary to SUMMARY.md in directory root'''
    with open(summary_dir / 'SUMMARY.md', 'w') as f:
        f.write(summary)


if __name__ == "__main__":
    tree = get_markdown_tree(Path('/Users/technogleb/knowledge_base'))
    for dir_, md_files in tree.items():
        summary = generate_summary(md_files, Path('/Users/technogleb/knowledge_base'))
        write_summary(dir_, summary)

