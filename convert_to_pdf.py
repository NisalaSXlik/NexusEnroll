#!/usr/bin/env python3
"""
Convert markdown documentation files to HTML format (which can then be printed to PDF).
"""

import os
import markdown
from datetime import datetime

def convert_md_to_html():
    """Convert all markdown files in docs/ to HTML format."""
    
    # List of markdown files to convert
    md_files = [
        "docs/architecture_analysis.md",
        "docs/design_patterns_analysis.md", 
        "docs/uml_diagrams.md",
        "docs/README.md",
        "README.md",
        "REQUIREMENTS_VALIDATION.md",
        "TESTING_GUIDE.md",
        "SUBMISSION_GUIDE.md"
    ]
    
    print("Converting markdown files to HTML...")
    print("=" * 50)
    
    converted_count = 0
    failed_count = 0
    
    # HTML template with styling
    html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 0;
            padding-left: 20px;
            color: #666;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
        @media print {{
            body {{ margin: 0; }}
            .header {{ page-break-after: avoid; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>NexusEnroll - University Course Enrolment System</p>
        <p>Generated on: {date}</p>
    </div>
    {content}
</body>
</html>
"""
    
    for md_file in md_files:
        if os.path.exists(md_file):
            try:
                # Read markdown file
                with open(md_file, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                
                # Convert markdown to HTML
                html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])
                
                # Create HTML filename
                html_file = md_file.replace('.md', '.html')
                title = os.path.basename(md_file).replace('.md', '').replace('_', ' ').title()
                
                print(f"Converting: {md_file} -> {html_file}")
                
                # Create full HTML document
                full_html = html_template.format(
                    title=title,
                    content=html_content,
                    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                
                # Write HTML file
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(full_html)
                
                print(f"✅ Successfully converted: {html_file}")
                converted_count += 1
                    
            except Exception as e:
                print(f"❌ Error converting {md_file}: {str(e)}")
                failed_count += 1
        else:
            print(f"⚠️  File not found: {md_file}")
            failed_count += 1
    
    print("\n" + "=" * 50)
    print(f"Conversion Summary:")
    print(f"✅ Successfully converted: {converted_count} files")
    print(f"❌ Failed conversions: {failed_count} files")
    
    if converted_count > 0:
        print(f"\nHTML files created in the current directory.")
        print("To convert to PDF:")
        print("1. Open each HTML file in your web browser")
        print("2. Press Ctrl+P (or Cmd+P on Mac)")
        print("3. Select 'Save as PDF' as the destination")
        print("4. Click 'Save'")
        print("\nAlternatively, you can use online HTML to PDF converters.")

if __name__ == "__main__":
    convert_md_to_html()