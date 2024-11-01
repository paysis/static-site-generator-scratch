from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            continue
        count_delimiter = sum(map(lambda _: 1, filter(lambda x: x == delimiter, old_node.text)))
        if count_delimiter % 2 != 0:
            raise Exception("Invalid Markdown syntax: delimiter non-match found")
        parts = []
        temp_text = ""
        type_scope = False
        for c in old_node.text:
            if c == delimiter and len(temp_text) > 0:
                part_item = TextNode(temp_text, text_type if type_scope else TextType.TEXT)
                parts.append(part_item)
                temp_text = ""
                type_scope = not type_scope
            elif c == delimiter:
                type_scope = not type_scope
            else:
                temp_text += c
        if len(temp_text) > 0:
            part_item = TextNode(temp_text, TextType.TEXT)
            parts.append(part_item)
        ret.extend(parts)
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
