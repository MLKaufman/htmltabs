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

### UV
Alternatively, you can install it using `uv` (Universal Virtual Environment) which is a cross-platform tool for managing Python environments.

```
uv venv 
uv pip install --editable . 
uv run htmltabs
```

## Usage


## Example Usage

```
 Usage: htmltabs [OPTIONS] DIRECTORY_PATH [OUTPUT_FILE]                                                  
                                                                                                         
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────╮
│ *    directory_path      TEXT           Directory containing HTML files [default: None] [required]    │
│      output_file         [OUTPUT_FILE]  Name of the merged HTML output file [default: merged.html]    │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
```