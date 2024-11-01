from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children=[], props=None):
        super().__init__(tag, None, children, props=props)
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def __eq__(self, other):
        if self.tag != other.tag:
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

        if isinstance(self.children, list) and isinstance(other.children, list):
            if len(self.children) != len(other.children):
                return False
            
            for sc, tc in zip(self.children, other.children):
                if sc != tc:
                    return False
        return True

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parameter tag is required")
        if (self.children is None) or not isinstance(self.children, list):
            raise ValueError("Parameter children is required and must be an instance of list")
 
        final = f"<{self.tag}{self.props_to_html()}>{''.join(map(lambda x: x.to_html(), self.children))}</{self.tag}>"
        return final