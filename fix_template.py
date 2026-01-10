import re

file_path = r'c:\Users\webdi\exclusive_pro\templates\home.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find the specific split tag and replace it with single line
# It looks like: <span ...>{{ \n ... }}</span>
pattern = r'(<span[^>]*class="[^"]*text-gold[^"]*"[^>]*>)\s*\{\{\s*p\.tarifa\.nombre\s*\}\}\s*(</span>)'

new_content = re.sub(pattern, r'\1{{ p.tarifa.nombre }}\2', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed tags in home.html")
