class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if (value is None) and (children is None):
            raise Exception("Either value or children must be given!")  
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return " " + " ".join(map(lambda t: f"{t[0]}=\"{t[1]}\"", self.props.items()))