#!/usr/bin/env python3
import re
import urllib.parse
import os
import argparse

def adjust_image_paths(file_path, base_img_url):
    """
    Converts Obsidian-style image links ![[filename.png]] to standard Markdown
    links ![filename](base_img_url/filename.png) with URL encoding.
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    # Ensure base_img_url ends with a slash
    if not base_img_url.endswith('/'):
        base_img_url += '/'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_obsidian_link(match):
        full_name = match.group(1) # e.g. "Pasted image 20251113202717.png"
        name_no_ext = os.path.splitext(full_name)[0]
        encoded_name = urllib.parse.quote(full_name)
        return f'![{name_no_ext}]({base_img_url}{encoded_name})'

    # Pattern to match ![[filename.png]] or ![[filename.jpg]] etc.
    pattern = r'!\[\[(.*?\.(?:png|jpg|jpeg|gif|svg))\]\]'

    new_content = re.sub(pattern, replace_obsidian_link, content)

    # Optional: Alert user if no matches were found
    if new_content == content:
        print("No Obsidian-style links found or file already processed.")
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully adjusted image paths in {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Adjust Obsidian-style image paths in Markdown files.")
    parser.add_argument("file", help="Path to the Markdown file.")
    parser.add_argument("img_url", help="Base URL path for the images (e.g., /assets/img/posts/server-side-attacks/)")

    args = parser.parse_args()

    adjust_image_paths(args.file, args.img_url)

if __name__ == "__main__":
    main()
