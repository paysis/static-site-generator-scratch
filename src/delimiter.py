from textnode import TextType, TextNode

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
            