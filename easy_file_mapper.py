import os
import sys
from pathlib import Path
from collections import Counter

# ================= CONFIGURATION =================
# Replace this path with the folder you want to map.
# You can also pass the path as an argument via command line.
TARGET_DIRECTORY = r"C:\Your\Path\Here"
# =================================================

def format_line_stats(stats):
    """Generates the file count string for the tree line (e.g., `pdf = 2`, `txt = 1`)"""
    if not stats:
        return ""
    # Sort by count (descending) and then by name
    items = sorted(stats.items(), key=lambda x: (-x[1], x[0]))
    stats_str = ", ".join([f"`{ext} = {count}`" for ext, count in items])
    return f" # files here: {stats_str}"

def generate_tree_and_stats(base_dir):
    base_path = Path(base_dir)
    
    if not base_path.exists():
        print(f"❌ Error: Directory '{base_dir}' not found.")
        return

    # Global Counters (for the final Summary)
    global_file_stats = Counter()
    total_files_global = 0
    total_dirs_global = 0
    
    md_lines = []

    def process_directory(current_dir, prefix=""):
        nonlocal total_files_global, total_dirs_global
        
        # Try to list content. Handle permission errors gracefully.
        try:
            # Sort: Directories first, then files (alphabetical)
            content = sorted(list(current_dir.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            md_lines.append(f"{prefix}└── 🔒 <Access Denied>")
            return

        # Calculate LOCAL stats (files strictly inside this folder)
        local_stats = Counter()
        for item in content:
            if item.is_file():
                ext = item.suffix.lower().replace('.', '') or 'no_extension'
                local_stats[ext] += 1

        # Calculate tree structure
        item_count = len(content)
        
        for i, item in enumerate(content):
            is_last = (i == item_count - 1)
            connector = "└── " if is_last else "├── "
            
            if item.is_dir():
                total_dirs_global += 1
                
                # Calculate sub-folder stats for the inline display
                sub_stats = Counter()
                try:
                    for subitem in item.iterdir():
                        if subitem.is_file():
                            e = subitem.suffix.lower().replace('.', '') or 'no_extension'
                            sub_stats[e] += 1
                except PermissionError:
                    pass

                stats_text = format_line_stats(sub_stats)
                md_lines.append(f"{prefix}{connector}{item.name}/{stats_text}")
                
                # Recursion
                new_prefix = prefix + ("    " if is_last else "│   ")
                process_directory(item, new_prefix)
                
            else: # It is a file
                total_files_global += 1
                ext = item.suffix.lower().replace('.', '') or 'no_extension'
                global_file_stats[ext] += 1
                # Uncomment the line below if you want to list every single file
                # md_lines.append(f"{prefix}{connector}{item.name}") 
                # Keeping it commented to reduce noise, as per typical large directory requests, 
                # but you can enable it if you want file-level detail in the tree.
                md_lines.append(f"{prefix}{connector}{item.name}")

    # --- GENERATION START ---
    
    # Markdown Header
    md_lines.append(f"# Folder Tree\n")
    md_lines.append(f"## Main Dir: {base_path.name}\n")
    
    # Process Root separately to show its stats on the first line
    root_stats = Counter()
    try:
        for item in base_path.iterdir():
            if item.is_file():
                e = item.suffix.lower().replace('.', '') or 'no_extension'
                root_stats[e] += 1
    except Exception:
        pass
        
    md_lines.append(f"{base_path.name}/ {format_line_stats(root_stats)}")
    
    # Start recursion
    process_directory(base_path)

    # --- SUMMARY GENERATION ---
    md_lines.append(f"\n\n## Summary\n")
    md_lines.append(f"- Total files: {total_files_global}")
    md_lines.append(f"- Directories: {total_dirs_global}")
    
    for ext, count in sorted(global_file_stats.items()):
        md_lines.append(f"- {ext}: {count}")

    # Save File
    filename = f"{base_path.name}_file_mapping.md"
    output_path = base_path / filename
    
    final_content = "\n".join(md_lines)
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"✅ Success! Report generated at:\n-> {output_path}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

if __name__ == "__main__":
    # Allow passing path via command line argument, otherwise use default
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = TARGET_DIRECTORY
    
    generate_tree_and_stats(target)