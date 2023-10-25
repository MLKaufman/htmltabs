from bs4 import BeautifulSoup
import os
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def merge_html(directory_path: str = typer.Argument(..., help="Directory containing HTML files"), 
               output_file: str = typer.Argument("merged.html", help="Name of the merged HTML output file")):
    """
    Merge all HTML files in the specified directory into a single HTML file with a tabbed interface.
    """
    console.print(f"Scanning directory: [yellow]{directory_path}[/yellow]")

    merged_soup = BeautifulSoup("<html><head></head><body><div id='tab-buttons'></div><div id='tab-contents'></div></body></html>", 'html.parser')
    
    filenames = sorted([filename for filename in os.listdir(directory_path) if filename.endswith('.html')])
    
    # Copy styles and scripts from the first HTML file to the merged HTML file
    first_filepath = os.path.join(directory_path, filenames[0])
    with open(first_filepath, "r") as f:
        first_page_content = f.read()
    
    first_soup = BeautifulSoup(first_page_content, 'html.parser')
    merged_soup.head.append(first_soup.head)
    
    for i, filename in enumerate(filenames):
        filepath = os.path.join(directory_path, filename)
        console.print(f"Processing file: [green]{filepath}[/green]")
        
        with open(filepath, "r") as f:
            page_content = f.read()
        
        soup = BeautifulSoup(page_content, 'html.parser')
        
        tab_id = f"tab{i+1}"
        tab_class = "tab" if i != 0 else "tab active"  # The first tab is active by default
        div = merged_soup.new_tag("div", id=tab_id, **{"class": tab_class})
        div.append(soup.body.extract())
        
        tab_name = filename.split('.')[0]  # Strip the ".html" extension
        button = merged_soup.new_tag("button", **{"class": "tab-button", "onclick": f"showTab('{tab_id}')"})
        button.string = tab_name

        merged_soup.select("#tab-buttons")[0].append(button)
        merged_soup.select("#tab-contents")[0].append(div)

    style_tag = merged_soup.new_tag("style")
    style_tag.string = """.tab { display: none; } .tab.active { display: block; } .tab-button { cursor: pointer; }"""
    merged_soup.head.append(style_tag)
    
    script_tag = merged_soup.new_tag("script")
    script_tag.string = """function showTab(tabId) { var tabs = document.querySelectorAll('.tab'); tabs.forEach(function(tab) { tab.style.display = 'none'; }); document.getElementById(tabId).style.display = 'block'; }"""
    merged_soup.body.append(script_tag)
    
    with open(output_file, "w") as f:
        f.write(str(merged_soup))

    console.print(f"Merged HTML file saved as: [blue]{output_file}[/blue]")

if __name__ == "__main__":
    app()
