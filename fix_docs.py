import os
import re

def fix_frontmatter(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if content.strip().startswith('# ') and not content.startswith('---'):
                    # Extract title
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    title = title_match.group(1) if title_match else file
                    
                    new_content = f"---\ntitle: {title}\ndescription: Auto-generated description for {title}\n---\n\n{content}"
                    
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✅ Fixed frontmatter for {path}")

if __name__ == "__main__":
    fix_frontmatter("domains/sidebar/src/content/docs")
