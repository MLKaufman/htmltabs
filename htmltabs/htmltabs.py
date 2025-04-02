from bs4 import BeautifulSoup
import os
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def merge_html(
    directory_path: str = typer.Argument(..., help="Directory containing HTML files"), 
    output_file: str = typer.Argument("merged.html", help="Name of the merged HTML output file")
):
    console.print(f"📂 Scanning directory: [yellow]{directory_path}[/yellow]")

    merged_soup = BeautifulSoup("""
    <html>
      <head></head>
      <body>
        <div id="tab-buttons-container">
          <div id="tab-buttons"></div>
        </div>
        <div id="tab-contents"></div>
      </body>
    </html>
    """, 'html.parser')

    filenames = sorted([f for f in os.listdir(directory_path) if f.endswith('.html')])

    # Deduplicate styles/scripts
    seen_blocks = set()
    for filename in filenames:
        filepath = os.path.join(directory_path, filename)
        with open(filepath, "r") as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            if soup.head:
                for tag in soup.head.find_all(["style", "link", "script"]):
                    tag_str = str(tag)
                    if tag_str not in seen_blocks:
                        merged_soup.head.append(tag)
                        seen_blocks.add(tag_str)

    for i, filename in enumerate(filenames):
        filepath = os.path.join(directory_path, filename)
        console.print(f"✅ Processing: [green]{filepath}[/green]")

        with open(filepath, "r") as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        tab_id = f"tab{i+1}"
        tab_class = "tab active" if i == 0 else "tab"
        content_div = merged_soup.new_tag("div", id=tab_id, **{"class": tab_class})

        if soup.body:
            for element in soup.body.contents:
                content_div.append(BeautifulSoup(str(element), 'html.parser'))
        else:
            for element in soup.contents:
                content_div.append(BeautifulSoup(str(element), 'html.parser'))

        merged_soup.select_one("#tab-contents").append(content_div)

        tab_name = os.path.splitext(filename)[0]
        button = merged_soup.new_tag("button", **{
            "class": "tab-button",
            "onclick": f"showTab('{tab_id}', this)"
        })
        button.string = tab_name
        merged_soup.select_one("#tab-buttons").append(button)

    # Add styling
    style_tag = merged_soup.new_tag("style")
    style_tag.string = """
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }
    #tab-buttons-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    #tab-buttons {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    .tab-button {
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        background-color: #f0f0f0;
        cursor: pointer;
        font-size: 16px;
        transition: background-color 0.3s, color 0.3s;
    }
    .tab-button:hover {
        background-color: #007BFF;
        color: white;
    }
    .tab-button.active {
        background-color: #0056b3;
        color: white;
    }
    .tab {
        display: none;
        padding: 20px;
    }
    .tab.active {
        display: block;
    }
    """
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
    with open(output_file, "w") as f:
        f.write(str(merged_soup))

    console.print(f"📄 Merged HTML saved as: [blue]{output_file}[/blue]")

if __name__ == "__main__":
    app()