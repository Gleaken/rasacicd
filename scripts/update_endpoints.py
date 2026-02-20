#!/usr/bin/env python3
import re
import os

def extract_endpoints(file_path):
    endpoints = []
    # Regex for app.MapGet, app.MapPost, etc.
    pattern = re.compile(r'app\.Map(Get|Post|Put|Delete)\("([^"]+)"', re.IGNORECASE)
    
    if not os.path.exists(file_path):
        return endpoints

    with open(file_path, 'r') as f:
        content = f.read()
        matches = pattern.findall(content)
        for method, route in matches:
            endpoints.append(f"- **{method.upper()}** `{route}`")
    
    return endpoints

def update_readme(endpoints, readme_path='README.md'):
    start_marker = "<!-- ENDPOINTS_START -->"
    end_marker = "<!-- ENDPOINTS_END -->"
    
    if not os.path.exists(readme_path):
        with open(readme_path, 'w') as f:
            f.write("# rasacicd\n\n## Endpoints\n" + start_marker + "\n" + end_marker + "\n")
            
    with open(readme_path, 'r') as f:
        content = f.read()

    endpoint_str = "\n".join(endpoints)
    
    if start_marker in content and end_marker in content:
        new_content = re.sub(
            f"{start_marker}.*?{end_marker}",
            f"{start_marker}\n{endpoint_str}\n{end_marker}",
            content,
            flags=re.DOTALL
        )
    else:
        new_content = content + f"\n\n## Endpoints\n{start_marker}\n{endpoint_str}\n{end_marker}\n"

    with open(readme_path, 'w') as f:
        f.write(new_content)

if __name__ == "__main__":
    program_cs = "src/RasaCicd.API/Program.cs"
    endpoints = extract_endpoints(program_cs)
    update_readme(endpoints)
    print(f"Updated README with {len(endpoints)} endpoints.")
