# Directory Mapper & Statistics Generator

A simple, dependency-free Python script that recursively maps a directory structure and generates a Markdown report. It visualizes the folder tree and calculates file statistics (counts by extension) for each subdirectory and a grand total summary.

## 🚀 Features

- **Recursive Mapping:** Traverses all subfolders to the deepest level.
- **Visual Tree:** Generates a clean Markdown directory tree representation.
- **File Statistics:** - Displays file counts per extension next to each folder (e.g., `pdf = 5`, `py = 2`).
  - Provides a global summary of all file types found.
- **Portable:** Uses only Python's standard library (`pathlib`, `collections`, `os`). No `pip install` required.

## 📋 Prerequisites

- Python 3.6 or higher.

## 🛠️ Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/directory-mapper.git](https://github.com/YOUR-USERNAME/directory-mapper.git)
   cd directory-mapper

```

2. **Configure the path:**
Open `file_mapper.py` and set the `TARGET_DIRECTORY` variable to the folder you want to analyze:
```python
TARGET_DIRECTORY = r"C:\Users\Name\Documents\MyProject"

```


*(Alternatively, you can modify the script to accept command-line arguments).*
3. **Run the script:**
```bash
python file_mapper.py

```


4. **Check the output:**
A new file named `{FolderName}_file_mapping.md` will be created inside the target directory.

## 📄 Output Example

The generated Markdown file will look like this:

```md
# Folder Tree

## Main Dir: References

References/                   # files here: `pdf = 2`
├── Data/                     # files here: `csv = 5`, `json = 1`
│   ├── data_clean.csv
│   └── config.json
└── Docs/                     # files here: `docx = 1`
    └── report.docx

## Summary

- Total files: 9
- Directories: 2
- csv: 5
- docx: 1
- json: 1
- pdf: 2

```
