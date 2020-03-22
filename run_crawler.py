#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from indexer import IndexingNode
from settings import INDEXER_START_URL

if __name__ == "__main__":
    root_indexing_node = IndexingNode(target_url=INDEXER_START_URL)
    root_indexing_node.start()
