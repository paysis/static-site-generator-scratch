from enum import Enum
import re
from parentnode import ParentNode
from leafnode import LeafNode
from inline_markdown import create_text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    sections = map(lambda x: x.strip(), sections)
    sections = filter(lambda x: x != "", sections)
    sections = list(sections)
    return sections

def block_to_block_type(block):
    headings = ["".join(map(lambda _: "#", range(x))) for x in range(1, 7)]
    if block.split(" ")[0] in headings:
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("* ") or block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif re.search(r"^\d+\.\ ", block) is not None:
        lines = block.split("\n")
        line_counter = 1
        for line in lines:
            try:
                num = int(line.split(".", 1)[0])
                if num != line_counter:
                    raise Exception()
            except:
                raise Exception("Ordered list starts with 1 and increments in each line")
            line_counter += 1

        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def flatten_nodes(nodes):
    return [item for sub_item in nodes for item in sub_item]

def block_to_parent_node(block, block_type, metadata={}):
    text_nodes_nested = create_text_to_textnodes(block)
    roots = []
    nodes = map(lambda nested_nodes: list(map(text_node_to_html_node, nested_nodes)), text_nodes_nested)
    nodes = list(nodes)
    match block_type:
        case BlockType.PARAGRAPH:
            nodes = flatten_nodes(nodes)
            roots.append(ParentNode("p", nodes))
        case BlockType.QUOTE:
            nodes = flatten_nodes(nodes)
            roots.append(ParentNode("blockquote", nodes))
        case BlockType.UNORDERED_LIST:
            lis = map(lambda x: ParentNode("li", x), nodes)
            lis = list(lis)
            roots.append(ParentNode("ul", lis))
        case BlockType.ORDERED_LIST:
            lis = map(lambda x: ParentNode("li", x), nodes)
            lis = list(lis)
            roots.append(ParentNode("ol", lis))
        case BlockType.CODE:
            nodes = flatten_nodes(nodes)
            code_node = ParentNode("code", nodes)
            roots.append(ParentNode("pre", [code_node]))
        case BlockType.HEADING:
            if "heading" not in metadata:
                raise Exception("Heading tags are not given in metadata.")
            count_of_tags = int(metadata["heading"])
            if count_of_tags == 0 or count_of_tags > 6:
                raise Exception(f"Heading tags are from h1 to h6, given: {count_of_tags} tags")
            nodes = flatten_nodes(nodes)
            roots.append(ParentNode(f"h{count_of_tags}", nodes))
        case _:
            raise Exception(f"Block type was unexpected: {block_type}")
    return roots

def strip_block_annotations(block, block_type):
    metadata = {}
    match block_type:
        case BlockType.PARAGRAPH:
            return block, metadata
        case BlockType.QUOTE:
            return block[1:].strip(), metadata
        case BlockType.UNORDERED_LIST:
            return "\n".join(map(lambda x: x[1:].strip(), block.strip().split("\n"))), metadata
        case BlockType.ORDERED_LIST:
            return "\n".join(map(lambda x: x[2:].strip(), block.split("\n"))), metadata
        case BlockType.CODE:
            return block[3:-3], metadata
        case BlockType.HEADING:
            sections = block.split(" ", 1)
            metadata["heading"] = len(sections[0])
            return sections[1], metadata
        case _:
            raise Exception(f"Block type was unexpected: {block_type}")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_stripped, metadata = strip_block_annotations(block, block_type)
        parent_roots = block_to_parent_node(block_stripped, block_type, metadata=metadata)
        nodes.extend(parent_roots)
    root_node = ParentNode("div", nodes)
    return root_node