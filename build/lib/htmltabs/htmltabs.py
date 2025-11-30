from bs4 import BeautifulSoup
import os
import typer
from rich.console import Console
from typing import Optional, List
import glob
from pathlib import Path

app = typer.Typer()
console = Console()

@app.command()
def merge_html(
    directory_path: str = typer.Argument(..., help="Directory containing HTML files"),
    output_file: str = typer.Argument("merged.html", help="Name of the merged HTML output file"),
    
    # File filtering options
    pattern: str = typer.Option("*.html", "--pattern", "-p", help="File pattern to match (e.g., '*.html', '*.htm')"),
    exclude: Optional[List[str]] = typer.Option(None, "--exclude", "-e", help="Patterns to exclude (can be used multiple times)"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Scan directories recursively"),
    
    # Sorting and organization
    sort_by: str = typer.Option("name", "--sort-by", "-s", help="Sort files by: name, size, date, or none"),
    reverse_sort: bool = typer.Option(False, "--reverse", help="Reverse the sort order"),
    
    # Styling and customization
    custom_css: Optional[str] = typer.Option(None, "--custom-css", "-c", help="Path to custom CSS file to include"),
    theme: str = typer.Option("default", "--theme", "-t", help="Built-in theme: default, dark, minimal"),
    tab_position: str = typer.Option("top", "--tab-position", help="Tab position: top, bottom, left, right"),
    
    # Output control
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress all output except errors"),
    preview: bool = typer.Option(False, "--preview", help="Show what files would be processed without creating output"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite output file if it exists"),
    
    # Tab naming
    use_full_path: bool = typer.Option(False, "--full-path", help="Use full file path as tab name instead of just filename"),
    strip_extensions: bool = typer.Option(True, "--strip-ext/--keep-ext", help="Strip file extensions from tab names"),
    
    # Advanced options
    use_iframe: bool = typer.Option(False, "--iframe", help="Embed files using iframes (better for complex reports with JS/CSS)")
):
    """
    Merge HTML files into a single HTML file with tabs.
    
    This tool scans a directory for HTML files and combines them into a single
    HTML file with a tabbed interface for easy navigation between the original files.
    """
    
    if quiet and verbose:
        console.print("[red]Error: Cannot use both --quiet and --verbose flags[/red]")
        raise typer.Exit(1)
    
    def log(message: str, style: str = ""):
        if not quiet:
            console.print(message, style=style)
    
    def verbose_log(message: str, style: str = ""):
        if verbose and not quiet:
            console.print(message, style=style)
    
    # Check if output file exists
    if os.path.exists(output_file) and not force and not preview:
        console.print(f"[red]Error: Output file '{output_file}' already exists. Use --force to overwrite.[/red]")
        raise typer.Exit(1)
    
    log(f"📂 Scanning directory: [yellow]{directory_path}[/yellow]")
    
    # Build file list
    if recursive:
        pattern_path = os.path.join(directory_path, "**", pattern)
        files = glob.glob(pattern_path, recursive=True)
    else:
        pattern_path = os.path.join(directory_path, pattern)
        files = glob.glob(pattern_path)
    
    # Apply exclusions
    if exclude:
        original_count = len(files)
        for exclude_pattern in exclude:
            if recursive:
                exclude_path = os.path.join(directory_path, "**", exclude_pattern)
                exclude_files = set(glob.glob(exclude_path, recursive=True))
            else:
                exclude_path = os.path.join(directory_path, exclude_pattern)
                exclude_files = set(glob.glob(exclude_path))
            files = [f for f in files if f not in exclude_files]
        
        excluded_count = original_count - len(files)
        if excluded_count > 0:
            verbose_log(f"Excluded {excluded_count} files based on exclusion patterns")
    
    if not files:
        console.print(f"[red]No files found matching pattern '{pattern}' in {directory_path}[/red]")
        raise typer.Exit(1)
    
    # Sort files
    if sort_by == "name":
        files.sort(key=os.path.basename, reverse=reverse_sort)
    elif sort_by == "size":
        files.sort(key=lambda f: os.path.getsize(f), reverse=reverse_sort)
    elif sort_by == "date":
        files.sort(key=lambda f: os.path.getmtime(f), reverse=reverse_sort)
    elif sort_by == "none":
        pass  # Keep original order
    else:
        console.print(f"[red]Invalid sort option: {sort_by}. Use: name, size, date, or none[/red]")
        raise typer.Exit(1)
    
    log(f"Found {len(files)} HTML files")
    
    if preview:
        log("\n[blue]Preview - Files that would be processed:[/blue]")
        for i, filepath in enumerate(files, 1):
            rel_path = os.path.relpath(filepath, directory_path)
            size = os.path.getsize(filepath)
            log(f"  {i:3d}. {rel_path} ({size:,} bytes)")
        log(f"\n[blue]Output would be saved to: {output_file}[/blue]")
        return
    
    # Initialize merged HTML structure
    merged_soup = BeautifulSoup("""
    <html>
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Merged HTML Tabs</title>
      </head>
      <body>
        <div id="tab-container">
          <div id="tab-buttons"></div>
          <div id="tab-contents"></div>
        </div>
      </body>
    </html>
    """, 'html.parser')

    # Deduplicate styles/scripts (only if not using iframes)
    if not use_iframe:
        seen_blocks = set()
        for filepath in files:
            verbose_log(f"Scanning for styles/scripts: [dim]{os.path.relpath(filepath, directory_path)}[/dim]")
            with open(filepath, "r", encoding='utf-8', errors='ignore') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                if soup.head:
                    for tag in soup.head.find_all(["style", "link", "script"]):
                        tag_str = str(tag)
                        if tag_str not in seen_blocks:
                            merged_soup.head.append(tag)
                            seen_blocks.add(tag_str)

    # Process each file
    for i, filepath in enumerate(files):
        rel_path = os.path.relpath(filepath, directory_path)
        log(f"✅ Processing: [green]{rel_path}[/green]")

        with open(filepath, "r", encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        tab_id = f"tab{i+1}"
        tab_class = "tab active" if i == 0 else "tab"
        content_div = merged_soup.new_tag("div", id=tab_id, **{"class": tab_class})

        if use_iframe:
             # Use iframe with srcdoc
            with open(filepath, "r", encoding='utf-8', errors='ignore') as f:
                file_content = f.read()
            
            # Create iframe
            iframe = merged_soup.new_tag("iframe", srcdoc=file_content, **{
                "class": "tab-iframe",
                "frameborder": "0",
                "sandbox": "allow-scripts allow-same-origin allow-popups allow-forms"
            })
            content_div.append(iframe)
        else:
            # Extract body content or entire content if no body tag
            content_html = ""
            if soup.body:
                content_html = "".join(str(element) for element in soup.body.contents if str(element).strip())
            else:
                content_html = "".join(str(element) for element in soup.contents if str(element).strip())
            
            # Parse and append the content
            if content_html.strip():
                parsed_content = BeautifulSoup(content_html, 'html.parser')
                for element in parsed_content:
                    if str(element).strip():
                        content_div.append(element)

        merged_soup.select_one("#tab-contents").append(content_div)

        # Generate tab name
        if use_full_path:
            tab_name = rel_path
        else:
            tab_name = os.path.basename(filepath)
        
        if strip_extensions:
            tab_name = os.path.splitext(tab_name)[0]

        button = merged_soup.new_tag("button", **{
            "class": "tab-button",
            "onclick": f"showTab('{tab_id}', this)",
            "title": rel_path  # Add tooltip with full path
        })
        button.string = tab_name
        merged_soup.select_one("#tab-buttons").append(button)

    # Add custom CSS if provided
    if custom_css and os.path.exists(custom_css):
        verbose_log(f"Including custom CSS from: {custom_css}")
        with open(custom_css, "r", encoding='utf-8') as f:
            custom_style = merged_soup.new_tag("style")
            custom_style.string = f.read()
            merged_soup.head.append(custom_style)
    elif custom_css:
        console.print(f"[yellow]Warning: Custom CSS file not found: {custom_css}[/yellow]")

    # Add theme-based styling
    style_tag = merged_soup.new_tag("style")
    
    # Get theme styles
    base_styles = get_theme_styles(theme, tab_position)
    style_tag.string = base_styles
    merged_soup.head.append(style_tag)

    # Tab switching script
    script_tag = merged_soup.new_tag("script")
    script_tag.string = """
    function showTab(tabId, button) {
        document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
        document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        button.classList.add('active');
    }
    document.addEventListener("DOMContentLoaded", () => {
        const firstButton = document.querySelector('.tab-button');
        if (firstButton) firstButton.classList.add('active');
    });
    """
    merged_soup.body.append(script_tag)

    # Write to file
    verbose_log(f"Writing merged HTML to: {output_file}")
    with open(output_file, "w", encoding='utf-8') as f:
        f.write(str(merged_soup))

    log(f"📄 Merged HTML saved as: [blue]{output_file}[/blue]")
    log(f"   Combined {len(files)} files into a single tabbed interface")


def get_theme_styles(theme: str, tab_position: str) -> str:
    """Get CSS styles based on theme and tab position."""
    
    # Base layout styles based on tab position
    if tab_position == "top":
        layout_css = """
        #tab-container { display: flex; flex-direction: column; height: 100vh; }
        #tab-buttons { display: flex; gap: 10px; flex-wrap: wrap; padding: 10px; border-bottom: 1px solid #ddd; }
        #tab-contents { flex: 1; overflow: auto; }
        """
    elif tab_position == "bottom":
        layout_css = """
        #tab-container { display: flex; flex-direction: column; height: 100vh; }
        #tab-buttons { display: flex; gap: 10px; flex-wrap: wrap; padding: 10px; border-top: 1px solid #ddd; order: 2; }
        #tab-contents { flex: 1; overflow: auto; order: 1; }
        """
    elif tab_position == "left":
        layout_css = """
        #tab-container { display: flex; height: 100vh; }
        #tab-buttons { display: flex; flex-direction: column; gap: 5px; padding: 10px; border-right: 1px solid #ddd; min-width: 200px; }
        #tab-contents { flex: 1; overflow: auto; }
        """
    elif tab_position == "right":
        layout_css = """
        #tab-container { display: flex; height: 100vh; }
        #tab-buttons { display: flex; flex-direction: column; gap: 5px; padding: 10px; border-left: 1px solid #ddd; min-width: 200px; order: 2; }
        #tab-contents { flex: 1; overflow: auto; order: 1; }
        """
    else:
        layout_css = """
        #tab-container { display: flex; flex-direction: column; height: 100vh; }
        #tab-buttons { display: flex; gap: 10px; flex-wrap: wrap; padding: 10px; border-bottom: 1px solid #ddd; }
        #tab-contents { flex: 1; overflow: hidden; display: flex; flex-direction: column; }
        .tab { flex: 1; display: none; flex-direction: column; }
        .tab.active { display: flex; }
        .tab-iframe { width: 100%; height: 100%; border: none; flex: 1; }
        """
    
    # Theme-specific styles
    if theme == "dark":
        theme_css = """
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; padding: 0; 
            background-color: #1a1a1a; 
            color: #e0e0e0; 
        }
        .tab-button {
            padding: 12px 20px; border: none; border-radius: 6px;
            background-color: #333; color: #e0e0e0; cursor: pointer;
            font-size: 14px; transition: all 0.3s ease;
        }
        .tab-button:hover { background-color: #555; }
        .tab-button.active { background-color: #007BFF; color: white; }
        .tab { display: none; padding: 20px; }
        .tab.active { display: block; }
        #tab-buttons { background-color: #252525; }
        """
    elif theme == "minimal":
        theme_css = """
        body { 
            font-family: system-ui, -apple-system, sans-serif; 
            margin: 0; padding: 0; 
            background-color: #fafafa; 
            color: #333;
            line-height: 1.6;
        }
        .tab-button {
            padding: 8px 16px; border: 1px solid #ddd; 
            background-color: white; color: #666; cursor: pointer;
            font-size: 13px; transition: all 0.2s ease;
            border-radius: 0;
        }
        .tab-button:hover { background-color: #f5f5f5; color: #333; }
        .tab-button.active { background-color: #333; color: white; border-color: #333; }
        .tab { display: none; padding: 30px; max-width: 1200px; margin: 0 auto; }
        .tab.active { display: block; }
        #tab-buttons { background-color: white; border-bottom: 1px solid #eee; }
        """
    else:  # default theme
        theme_css = """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 0; 
            background-color: #ffffff; 
            color: #333;
        }
        .tab-button {
            padding: 10px 20px; border: none; border-radius: 8px;
            background-color: #f8f9fa; color: #495057; cursor: pointer;
            font-size: 14px; font-weight: 500; 
            transition: all 0.3s ease;
        }
        .tab-button:hover { background-color: #007BFF; color: white; transform: translateY(-1px); }
        .tab-button.active { background-color: #0056b3; color: white; }
        .tab { display: none; padding: 20px; }
        .tab.active { display: block; }
        #tab-buttons { background-color: #f8f9fa; }
        """
    
    return layout_css + theme_css


if __name__ == "__main__":
    app()