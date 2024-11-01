from textnode import TextType, TextNode
import re
            
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            if len(old_node.text) > 0:
                ret.append(old_node)
            continue
        text = old_node.text
        sections = text.split(delimiter, 2)
        if len(sections) > 1 and len(sections) != 3:
            raise Exception("Delimiter mismatch")
        if len(sections) == 1:
            if len(old_node.text) > 0:
                ret.append(old_node)
            continue
        section1 = split_nodes_delimiter([TextNode(sections[0], TextType.TEXT)], delimiter, text_type)
        section2 = TextNode(sections[1], text_type)
        section3 = split_nodes_delimiter([TextNode(sections[2], TextType.TEXT)], delimiter, text_type)
        ret.extend(section1)
        ret.append(section2)
        ret.extend(section3)
    return ret


def split_nodes_image_or_link(old_nodes):
    ret = []
    for old_node in old_nodes:
        parts = []
        imgs = extract_markdown_images(old_node.text)
        links = extract_markdown_links(old_node.text)
        if len(imgs) == 0 and len(links) == 0:
            if len(old_node.text) > 0:
                ret.append(old_node)
            continue
        if len(imgs) > 0:
            image_alt, image_link = imgs[0]
            splits = old_node.text.split(f"![{image_alt}]({image_link})", 1)
            parts.append(TextNode(splits[0], TextType.TEXT))
            parts.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if len(splits) > 1:
                parts.append(TextNode(splits[1], TextType.TEXT))
        elif len(links) > 0:
            link_text, link_link = links[0]
            splits = old_node.text.split(f"[{link_text}]({link_link})", 1)
            parts.append(TextNode(splits[0], TextType.TEXT))
            parts.append(TextNode(link_text, TextType.LINK, link_link))
            if len(splits) > 1:
                parts.append(TextNode(splits[1], TextType.TEXT))
        ret.extend(split_nodes_image_or_link(parts))
    return ret

def extract_markdown_images(text):
    extracted_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_images

def extract_markdown_links(text):
    extracted_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_links

def split_genesis_nodes_by_newline(text):
    sections = text.split("\n")
    sections = map(lambda x: x.strip(" "), sections)
    sections = filter(lambda x: x != "", sections)
    sections = map(lambda x: TextNode(f"{x}", TextType.TEXT), sections)
    sections = list(sections)
    return sections

def create_text_to_textnodes(text):
    new_nodes = split_genesis_nodes_by_newline(text)
    nested_nodes = []
    for new_node in new_nodes:
        new_node = [new_node]
        new_node = split_nodes_delimiter(new_node, "**", TextType.BOLD)
        new_node = split_nodes_delimiter(new_node, "*", TextType.ITALIC)
        new_node = split_nodes_delimiter(new_node, "`", TextType.CODE)
        new_node = split_nodes_image_or_link(new_node)
        nested_nodes.append(new_node)
    return nested_nodes
