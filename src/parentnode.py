from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children=[], props=None):
        super().__init__(tag, None, children, props=props)
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"


    def to_html(self):
        if self.tag is None:
            raise ValueError("Parameter tag is required")
        if (self.children is None) or not isinstance(self.children, list):
            raise ValueError("Parameter children is required and must be an instance of list")
        final = f"<{self.tag}{self.props_to_html()}>{''.join(map(lambda x: x.to_html(), self.children))}</{self.tag}>"
        return final