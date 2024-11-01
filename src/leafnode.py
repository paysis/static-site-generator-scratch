from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, other):
        if self.tag != other.tag:
            return False

        if self.value != other.value:
            return False

        if ((self.props is not None) and (other.props is None)) or ((self.props is None) and other.props is not None):
            return False

        if (self.props is not None) and (other.props is not None):
            if len(self.props.keys()) != len(other.props.keys()):
                return False

            sorted_keys_s = sorted(self.props.items(), key=lambda x: x[0])
            sorted_keys_t = sorted(other.props.items(), key=lambda x: x[0])

            for item_s, item_t in zip(sorted_keys_s, sorted_keys_t):
                if item_s[0] != item_t[0] or item_s[1] != item_t[1]:
                    return False 

        return True

    def to_html(self):
        if self.value is None:
            raise ValueError("Parameter \"value\" is required!")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"