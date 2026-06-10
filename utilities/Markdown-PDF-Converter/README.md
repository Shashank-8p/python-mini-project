# Markdown to PDF Converter

A lightweight Python command-line utility that parses a local Markdown file (`.md`) and exports it into a beautifully styled PDF document (`.pdf`).

## Features

- **Standard Markdown Parsing**: Supports headers, paragraphs, bold/italic formatting, inline/block code, blockquotes, lists, tables, and horizontal rules.
- **Custom Visual Themes**: Select from three beautiful, curated themes:
  - `Classic` (Default): Traditional serif/sans-serif combination with clean dark-blue accents.
  - `Modern`: Modern and clean sans-serif layout with teal/accent coloring and distinct tables/code styling.
  - `Sleek Dark`: Premium dark mode layout with deep dark backgrounds and neon cyan/purple accents.
- **Auto-pagination & Styling**: Automatically wraps text in tables and lists, implements running page headers, running footers, and page numbers.

## Requirements

The utility uses two lightweight Python libraries:
- `markdown2` (version 2.5.5) - for Markdown to HTML compilation.
- `reportlab` (version 4.5.1) - for PDF document rendering.

No system binary installations (like `wkhtmltopdf` or `cairo`) are required.

## Installation

Install the required python packages using `pip`:
```bash
pip install markdown2 reportlab
```
Or if using poetry:
```bash
poetry install
```

## Usage

Run the script from the command-line, specifying the path to your Markdown file:

```bash
python utilities/Markdown-PDF-Converter/markdown_to_pdf.py input.md
```

### CLI Arguments

- `input_file` (Required): Path to the input `.md` file.
- `-o`, `--output` (Optional): Path to the output `.pdf` file. Defaults to `<input_file_basename>.pdf`.
- `-t`, `--theme` (Optional): Visual style theme. Choices are `Classic` (default), `Modern`, and `Sleek Dark`.

### Examples

Generate a PDF using the **Modern** theme:
```bash
python utilities/Markdown-PDF-Converter/markdown_to_pdf.py document.md --theme Modern -o output.pdf
```

Generate a PDF using the **Sleek Dark** theme:
```bash
python utilities/Markdown-PDF-Converter/markdown_to_pdf.py document.md --theme "Sleek Dark"
```
