# htmltabs

A CLI tool to merge HTML files into a single HTML file with tabs. Mainly useful for concatenanting data analysis reports generated with Jupyter Lab or Rmarkdown.

## Installation

### PIPX

Prefered method of installtion using pipx: <https://pypa.github.io/pipx/>

```
pipx install git+https://github.com/MLKaufman/htmltabs
```

can aslo be installed with vanilla pip:

```
pipx install git+https://github.com/MLKaufman/htmltabs
```

Once installed can be run using the command:
`htmltabs`

### UVX

The easiest possible way to run with `uvx`. Similar to `pipx`, `uvx` allows you to install and run Python packages in isolated environments without polluting your global Python environment.

```
uvx git+https://github.com/MLKaufman/htmltabs
```

### UV
Alternatively, you can install it using `uv` (Universal Virtual Environment) which is a cross-platform tool for managing Python environments.

```
uv venv 
uv pip install --editable . 
uv run htmltabs
```

## Usage

```bash
htmltabs [OPTIONS] DIRECTORY_PATH [OUTPUT_FILE]
```

### Basic Examples

```bash
# Basic usage - merge all HTML files in a directory
htmltabs ./reports

# Specify output filename
htmltabs ./reports combined.html

# Preview what files would be processed
htmltabs ./reports --preview

# Use dark theme with recursive scanning
htmltabs ./reports --recursive --theme dark

# Custom file pattern and exclusions
htmltabs ./data --pattern "*.htm" --exclude "*temp*" --exclude "*draft*"
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `DIRECTORY_PATH` | Directory containing HTML files (required) | - |
| `OUTPUT_FILE` | Name of the merged HTML output file (optional) | `merged.html` |

### File Filtering Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--pattern` | `-p` | File pattern to match (e.g., '*.html', '*.htm') | `*.html` |
| `--exclude` | `-e` | Patterns to exclude (can be used multiple times) | None |
| `--recursive` | `-r` | Scan directories recursively | `False` |

### Sorting and Organization

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--sort-by` | `-s` | Sort files by: name, size, date, or none | `name` |
| `--reverse` | | Reverse the sort order | `False` |

### Styling and Customization

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--theme` | `-t` | Built-in theme: default, dark, minimal | `default` |
| `--tab-position` | | Tab position: top, bottom, left, right | `top` |
| `--custom-css` | `-c` | Path to custom CSS file to include | None |

### Output Control

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--verbose` | `-v` | Enable verbose output | `False` |
| `--quiet` | `-q` | Suppress all output except errors | `False` |
| `--preview` | | Show what files would be processed without creating output | `False` |
| `--force` | `-f` | Overwrite output file if it exists | `False` |

### Tab Naming

| Option | Description | Default |
|--------|-------------|---------|
| `--full-path` | Use full file path as tab name instead of just filename | `False` |
| `--strip-ext/--keep-ext` | Strip/keep file extensions from tab names | `True` (strip) |

### Document Metadata

| Option | Description | Default |
|--------|-------------|---------|
| `--title` | Set the HTML title of the merged document | `Merged HTML Tabs` |

### Advanced Examples

```bash
# Recursive scan with custom sorting and dark theme
htmltabs ./projects --recursive --sort-by date --reverse --theme dark

# Use custom CSS and exclude certain files
htmltabs ./reports --custom-css ./my-styles.css --exclude "*draft*" --exclude "*backup*"

# Minimal theme with tabs on the left side
htmltabs ./docs --theme minimal --tab-position left

# Preview with verbose output to see what would be processed
htmltabs ./analysis --recursive --preview --verbose

# Keep file extensions and use full paths for tab names
htmltabs ./nested --recursive --full-path --keep-ext

# Force overwrite existing output with quiet mode
htmltabs ./data combined.html --force --quiet

# Set custom title and use specific output file
htmltabs ./reports dashboard.html --title "Analytics Dashboard - Q4 2024"
```