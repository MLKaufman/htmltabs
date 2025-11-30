import os

def create_repro_files():
    os.makedirs("repro_data", exist_ok=True)
    
    # File 1: Red background, ID="content" says "File 1"
    with open("repro_data/file1.html", "w") as f:
        f.write("""
        <html>
        <head>
            <style>
                body { background-color: #ffcccc; }
                #content { color: red; font-weight: bold; }
            </style>
            <script>
                var uniqueData = "File 1 Data";
                console.log("Loaded " + uniqueData);
            </script>
        </head>
        <body>
            <h1>Report 1</h1>
            <div id="content">This is content from File 1.</div>
            <script>
                document.getElementById("content").innerText += " (JS Modified)";
            </script>
        </body>
        </html>
        """)

    # File 2: Blue background, ID="content" says "File 2"
    with open("repro_data/file2.html", "w") as f:
        f.write("""
        <html>
        <head>
            <style>
                body { background-color: #ccccff; }
                #content { color: blue; font-style: italic; }
            </style>
            <script>
                var uniqueData = "File 2 Data";
                console.log("Loaded " + uniqueData);
            </script>
        </head>
        <body>
            <h1>Report 2</h1>
            <div id="content">This is content from File 2.</div>
            <script>
                document.getElementById("content").innerText += " (JS Modified)";
            </script>
        </body>
        </html>
        """)

if __name__ == "__main__":
    create_repro_files()
