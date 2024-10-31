from textnode import TextNode, TextType

def main():
    t1 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(t1)

if __name__ == "__main__":
    main()