#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
make template to static html
"""
import os
import re
from pathlib import Path
from typing import List, Dict, Pattern, Match, Set

from tornado.template import Loader

from trainier.util.logger import Log


class TemplateNode:
    def __init__(self, rel_path: Path, full_path: Path, parent_node = None, sub_nodes: List = None) -> None:
        self.rel_path: Path = rel_path
        self.full_path: Path = full_path
        self.parent_node: TemplateNode = parent_node
        self.sub_nodes: List[TemplateNode] = sub_nodes
        self.is_changed: bool = False

    def __repr__(self) -> str:
        return str(self.full_path)

    @property
    def is_leaf(self) -> bool:
        return self.sub_nodes is None or len(self.sub_nodes) == 0

    @property
    def is_root(self) -> bool:
        return self.parent_node is None

    @property
    def leaves(self) -> Set or None:
        if self.is_leaf:
            return None
        leaves: Set[TemplateNode] = set()
        queue: List[TemplateNode] = [self]
        while len(queue) > 0:
            n: TemplateNode = queue.pop(0)
            for sub_node in n.sub_nodes:
                if sub_node.is_leaf:
                    leaves.add(sub_node)
                else:
                    queue.append(sub_node)
        return leaves


class TemplateForest:
    EXTENDS_PATTERN: Pattern = re.compile(rb'{%\s*extends\s+\S+?\s*%}')

    def __init__(self, forest: Dict[Path, TemplateNode]) -> None:
        self.forest: Dict[Path, TemplateNode] = forest

    def make_relationship(self) -> None:
        """ check template content and find dependency of forest """
        for rel_path, node in self.forest.items():
            tpl_bytes: bytes = open(str(node.full_path), 'rb').read()
            m: Match = TemplateForest.EXTENDS_PATTERN.search(tpl_bytes)
            if m:
                base: str = m.group().decode().replace('{%', '').replace('%}', '').replace('extends', '').strip()
                base_path: Path = Path(base)
                if base_path not in self.forest:
                    raise ValueError('"{}" not exists in node tree.'.format(base))
                self.forest[base_path].sub_nodes.append(node)
                node.parent_node = self.forest[base_path]

    def check_changes(self, dst_dir: Path) -> None:
        queue: List[TemplateNode] = [root for root in self.forest.values() if root.parent_node is None]
        while len(queue) > 0:
            node: TemplateNode = queue.pop(0)
            if node.is_leaf:
                dst_path: Path = dst_dir / node.rel_path
                if not dst_path.is_file() or dst_path.stat().st_mtime < node.full_path.stat().st_mtime:
                    node.is_changed = True
            else:
                leaves: Set[TemplateNode] = node.leaves
                dst_leaves: Set[Path] = set([dst_dir / leaf.rel_path for leaf in leaves])
                leaves_mt_min = min([p.stat().st_mtime for p in dst_leaves])
                if node.full_path.stat().st_mtime > leaves_mt_min:
                    for leaf in leaves: leaf.is_changed = True
                else:
                    queue.extend(node.sub_nodes)

    @property
    def to_update_leaves(self) -> Set[TemplateNode]:
        return set([n for n in self.forest.values() if n.is_leaf and n.is_changed])

    @property
    def leaves(self) -> Set[TemplateNode]:
        return set([n for n in self.forest.values() if n.is_leaf])


def find_to_delete_output(forest: TemplateForest, dst_dir: Path) -> Set[Path]:
    all_leaves: Set[TemplateNode] = forest.leaves
    tpl_leaves: Set[TemplateNode] = set([p.rel_path for p in all_leaves])
    outputs: Set[Path] = set([p.relative_to(dst_dir) for p in dst_dir.rglob('*.html')])
    to_delete_outputs: Set[Path] = [dst_dir / p for p in outputs if p not in tpl_leaves]
    return to_delete_outputs


def static_template(leaf_node: TemplateNode, dst_dir: Path, loader: Loader):
    src_full: Path = leaf_node.full_path
    dst_full: Path = dst_dir / leaf_node.rel_path
    dst_parent: Path = dst_full.parent
    try:
        if not dst_parent.exists():
            dst_parent.mkdir(parents=True, exist_ok=True)
        b: bytes = loader.load(str(src_full)).generate()
        open(str(dst_full), 'wb').write(b)
    except Exception as e:
        Log.trainier.info(str(e))


def static_templates(src_dir: Path, dst_dir: Path):

    # first check if there are some changes
    forest: TemplateForest = TemplateForest(dict())
    for tpl_path in src_dir.rglob('*.html'):
        # create template node forest. prepare for output html.
        rel_path: Path = tpl_path.relative_to(src_dir)
        tpl_node: TemplateNode = TemplateNode(rel_path, tpl_path, None, list())
        forest.forest[rel_path] = tpl_node
    forest.make_relationship()
    forest.check_changes(dst_dir)

    # generate output html
    loader: Loader = Loader(str(src_dir))
    for node in forest.to_update_leaves:
        Log.trainier.info('to generate template [%s] to static [%s] ...', node.rel_path, node.rel_path)
        static_template(node, dst_dir, loader)
    # delete non-use html
    for p in find_to_delete_output(forest, dst_dir):
        Log.trainier.info('to delete static [%s] not in templates ...', p)
        os.remove(str(p))
