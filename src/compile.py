import shutil
import os
from markdown_util import generate_pages_recursive

def copytree(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    if not os.path.exists(src):
        raise Exception(f"Src path does not exist: {src}")
    ls = os.listdir(src)
    for _x in ls:
        x = os.path.join(src, _x)
        if os.path.exists(x) and os.path.isdir(x):
            copytree(x, os.path.join(dst, _x))
        elif os.path.exists(x) and os.path.isfile(x):
            shutil.copy(x, os.path.join(dst, _x))
        else:
            print(f"Something went wrong: {x}")

def compile(src="./static", dst="./public"):
    shutil.rmtree(dst)
    copytree(src, dst)
    generate_pages_recursive("content/", "template.html", "public/")
    print("Complete!")
    

if __name__ == "__main__":
    compile()