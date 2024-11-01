from block_markdown import markdown_to_html_node
import os

def extract_title(markdown):
    title_cands = filter(lambda x: x.startswith("# "), markdown.split("\n"))
    title_cands = map(lambda x: x[1:].strip(), title_cands)
    title_cands = list(title_cands)
    if len(title_cands) == 0:
        raise Exception("No title found in the markdown!")
    return title_cands[0]

def replace_placeholders_template(template, title, content):
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    return template

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        src = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html_body = markdown_to_html_node(src).to_html()
    html_title = extract_title(src)
    final_output = replace_placeholders_template(template, html_title, html_body)
    if not os.path.exists(os.path.split(dest_path)[0]):
        os.mkdir(os.path.split(dest_path)[0])
    with open(dest_path, "w") as f:
        f.write(final_output)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    ls = os.listdir(dir_path_content)
    for file in ls:
        if os.path.isdir(os.path.join(dir_path_content, file)):
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))
            continue
        exts = os.path.splitext(file)
        if len(exts) < 2:
            print(f"No extension: {file}")
            continue
        ext = exts[-1]
        if ext.lower() != ".md":
            continue
        basename, ext = os.path.splitext(file)
        generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, f"{basename}.html"))
