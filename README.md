# htmltabs

A CLI tool to merge HTML files into a single HTML file with tabs. Perfect for combining data analysis reports generated with Jupyter Lab, R Markdown, or complex bioinformatics reports like Cell Ranger outputs.

## Features

- 📁 **Flexible File Selection**: Pattern matching, exclusions, and recursive directory scanning
- 🎨 **Multiple Themes**: Built-in dark, minimal, and default themes
- 📐 **Customizable Layout**: Position tabs on any side (top, bottom, left, right)
- 🔒 **Iframe Isolation**: Use `--iframe` mode for complex reports with conflicting CSS/JavaScript
- 🎯 **Smart Sorting**: Sort by name, size, date, or preserve original order
- 🚀 **Fast & Lightweight**: Single output file with no external dependencies

## Installation

### Quick Start with uvx (Recommended)

The easiest way to use `htmltabs` is with `uvx`, which runs the tool in an isolated environment without installation:

```bash
uvx --from git+https://github.com/MLKaufman/htmltabs htmltabs ./reports
```

### Install with uv

For regular use, install with `uv`:

```bash
# Install globally
uv tool install git+https://github.com/MLKaufman/htmltabs

# Or in a project
uv add git+https://github.com/MLKaufman/htmltabs
```

### Development Installation

```bash
git clone https://github.com/MLKaufman/htmltabs
cd htmltabs
uv venv
uv pip install -e .
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

### Complex Reports (Cell Ranger, etc.)

For complex HTML reports with JavaScript and CSS that conflict when merged, use the `--iframe` flag:

```bash
# Merge Cell Ranger reports with full isolation
htmltabs ./cellranger_outputs --iframe --force

# Combine multiple bioinformatics reports
htmltabs ./analysis --recursive --iframe --theme dark
```

The `--iframe` mode embeds each HTML file in an isolated iframe, preventing CSS and JavaScript conflicts while keeping everything in a single file.

## Options Reference

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `DIRECTORY_PATH` | Directory containing HTML files (required) | - |
| `OUTPUT_FILE` | Name of the merged HTML output file | `merged.html` |

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

### Advanced Options

| Option | Description | Default |
|--------|-------------|---------|
| `--iframe` | Embed files using iframes (better for complex reports with JS/CSS) | `False` |

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

## Advanced Examples

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

# Complex bioinformatics pipeline outputs with iframe isolation
htmltabs ./pipeline_results --recursive --iframe --sort-by date --theme dark
```

## When to Use `--iframe` Mode

Use the `--iframe` flag when:

- ✅ Merging complex reports like Cell Ranger, MultiQC, or other bioinformatics tools
- ✅ HTML files have conflicting CSS class names or IDs
- ✅ JavaScript code relies on specific DOM structures or global variables
- ✅ Reports use interactive visualizations (Plotly, D3.js, etc.)

Use the default mode (without `--iframe`) when:

- ✅ Merging simple HTML reports or static content
- ✅ You want a smaller output file size
- ✅ Reports don't have conflicting styles or scripts

## License

MIT
