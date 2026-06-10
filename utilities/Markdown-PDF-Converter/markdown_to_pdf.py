#!/usr/bin/env python3
"""
Markdown to PDF Converter
A utility that parses a local Markdown file (.md) and exports it into a beautifully styled PDF document (.pdf).
Supports custom styling themes (Classic, Modern, Sleek Dark).
"""

import os
import sys
import argparse
import html
import re
from functools import partial
import markdown2

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from html.parser import HTMLParser

# Theme Configurations
THEMES = {
    "Classic": {
        "background": "#FFFFFF",
        "text": "#2C3E50",
        "h1": "#1A365D",
        "h2": "#2C3E50",
        "h3": "#34495E",
        "accent": "#2980B9",
        "code_bg": "#F8F9F9",
        "code_text": "#C0392B",
        "quote_bg": "#F4F6F6",
        "quote_text": "#7F8C8D",
        "quote_border": "#BDC3C7",
        "table_header_bg": "#34495E",
        "table_header_text": "#FFFFFF",
        "table_row_bg1": "#FFFFFF",
        "table_row_bg2": "#F2F4F4",
        "font_family_headings": "Times-Roman",
        "font_family_body": "Helvetica",
    },
    "Modern": {
        "background": "#FDFDFD",
        "text": "#1F2937",
        "h1": "#0F766E",
        "h2": "#115E59",
        "h3": "#134E4A",
        "accent": "#0D9488",
        "code_bg": "#F3F4F6",
        "code_text": "#D97706",
        "quote_bg": "#F9FAFB",
        "quote_text": "#4B5563",
        "quote_border": "#0D9488",
        "table_header_bg": "#0D9488",
        "table_header_text": "#FFFFFF",
        "table_row_bg1": "#FFFFFF",
        "table_row_bg2": "#F3F4F6",
        "font_family_headings": "Helvetica-Bold",
        "font_family_body": "Helvetica",
    },
    "Sleek Dark": {
        "background": "#121212",
        "text": "#E0E0E0",
        "h1": "#00E5FF",
        "h2": "#8A2BE2",
        "h3": "#FF007F",
        "accent": "#00E5FF",
        "code_bg": "#1E1E1E",
        "code_text": "#FFD700",
        "quote_bg": "#1A1A1A",
        "quote_text": "#A0A0A0",
        "quote_border": "#8A2BE2",
        "table_header_bg": "#2A2A2A",
        "table_header_text": "#00E5FF",
        "table_row_bg1": "#1E1E1E",
        "table_row_bg2": "#252525",
        "font_family_headings": "Helvetica-Bold",
        "font_family_body": "Helvetica",
    }
}


def setup_styles(theme):
    """Sets up and returns custom ParagraphStyles based on the active theme."""
    styles = getSampleStyleSheet()

    # Modify/Add Heading styles
    styles['Heading1'].fontName = theme["font_family_headings"]
    styles['Heading1'].fontSize = 24
    styles['Heading1'].leading = 28
    styles['Heading1'].textColor = colors.HexColor(theme["h1"])
    styles['Heading1'].spaceAfter = 12
    styles['Heading1'].spaceBefore = 10
    styles['Heading1'].keepWithNext = True

    styles['Heading2'].fontName = theme["font_family_headings"]
    styles['Heading2'].fontSize = 18
    styles['Heading2'].leading = 22
    styles['Heading2'].textColor = colors.HexColor(theme["h2"])
    styles['Heading2'].spaceBefore = 14
    styles['Heading2'].spaceAfter = 8
    styles['Heading2'].keepWithNext = True

    styles['Heading3'].fontName = theme["font_family_headings"]
    styles['Heading3'].fontSize = 14
    styles['Heading3'].leading = 18
    styles['Heading3'].textColor = colors.HexColor(theme["h3"])
    styles['Heading3'].spaceBefore = 12
    styles['Heading3'].spaceAfter = 6
    styles['Heading3'].keepWithNext = True

    # Subordinate Headings
    for level in ('Heading4', 'Heading5', 'Heading6'):
        styles[level].fontName = theme["font_family_headings"]
        styles[level].fontSize = 11.5
        styles[level].leading = 15
        styles[level].textColor = colors.HexColor(theme["text"])
        styles[level].spaceBefore = 10
        styles[level].spaceAfter = 4
        styles[level].keepWithNext = True

    # Modify Normal/BodyText
    styles['Normal'].fontName = theme["font_family_body"]
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 15
    styles['Normal'].textColor = colors.HexColor(theme["text"])
    styles['Normal'].spaceAfter = 10

    if 'BodyText' in styles:
        styles['BodyText'].fontName = theme["font_family_body"]
        styles['BodyText'].fontSize = 10
        styles['BodyText'].leading = 15
        styles['BodyText'].textColor = colors.HexColor(theme["text"])
        styles['BodyText'].spaceAfter = 10

    # Custom styling for list item paragraph wrapping
    list_style = ParagraphStyle(
        'CustomListItem',
        parent=styles['Normal'],
        leftIndent=24,
        firstLineIndent=-12,
        spaceAfter=5
    )
    styles.add(list_style)

    # Monospace block code style
    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor(theme["text"]),
        spaceAfter=0
    )
    styles.add(code_style)

    # Quote style
    quote_para_style = ParagraphStyle(
        'QuoteParaStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique' if theme["font_family_body"] == 'Helvetica' else 'Times-Italic',
        textColor=colors.HexColor(theme["quote_text"]),
        spaceAfter=6
    )
    styles.add(quote_para_style)

    # Table Header cell style
    th_style = ParagraphStyle(
        'TableHeaderStyle',
        fontName=theme["font_family_headings"],
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor(theme["table_header_text"])
    )
    styles.add(th_style)

    # Table Body cell style
    td_style = ParagraphStyle(
        'TableCellStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        spaceAfter=0
    )
    styles.add(td_style)

    return styles


class HTMLToFlowablesParser(HTMLParser):
    """Parses well-formed HTML generated by markdown2 and converts it into ReportLab Flowables."""
    
    def __init__(self, styles, theme, printable_width):
        super().__init__()
        self.styles = styles
        self.theme = theme
        self.printable_width = printable_width
        
        self.story = []
        
        # State tracking
        self.current_block = None
        self.text_accumulator = []
        
        # Blockquote state
        self.in_blockquote = False
        self.blockquote_flowables = []
        
        # Preformatted/Code block state
        self.in_pre = False
        
        # List tracking (nesting supported)
        self.list_type_stack = []
        self.list_counter_stack = []
        
        # Table tracking
        self.in_table = False
        self.table_data = []
        self.table_row = []

    def _add_flowable(self, flowable):
        """Helper to append to either the main story or the current blockquote group."""
        if self.in_blockquote:
            self.blockquote_flowables.append(flowable)
        else:
            self.story.append(flowable)

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Handle Block Level Elements
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'):
            self.current_block = tag
            self.text_accumulator = []
            
        elif tag == 'blockquote':
            self.in_blockquote = True
            self.blockquote_flowables = []
            
        elif tag == 'pre':
            self.in_pre = True
            self.text_accumulator = []
            
        elif tag == 'ul':
            self.list_type_stack.append('ul')
            self.list_counter_stack.append(0)
            
        elif tag == 'ol':
            self.list_type_stack.append('ol')
            self.list_counter_stack.append(0)
            
        elif tag == 'li':
            self.current_block = 'li'
            self.text_accumulator = []
            if self.list_type_stack and self.list_type_stack[-1] == 'ol':
                self.list_counter_stack[-1] += 1
                
        elif tag == 'table':
            self.in_table = True
            self.table_data = []
            
        elif tag == 'tr':
            self.table_row = []
            
        elif tag in ('th', 'td'):
            self.current_block = tag
            self.text_accumulator = []
            
        # Inline tags formatting mapping to ReportLab tags
        elif tag in ('strong', 'b'):
            self.text_accumulator.append('<b>')
        elif tag in ('em', 'i'):
            self.text_accumulator.append('<i>')
        elif tag == 'code':
            if not self.in_pre:
                self.text_accumulator.append(f'<font face="Courier" color="{self.theme["code_text"]}">')
        elif tag == 'a':
            href = attrs_dict.get('href', '')
            self.text_accumulator.append(f'<a href="{href}" color="{self.theme["accent"]}">')
            
        elif tag == 'br':
            self.text_accumulator.append('<br/>')
            
        elif tag == 'hr':
            hr = HRFlowable(
                width="100%",
                thickness=1,
                color=colors.HexColor(self.theme["quote_border"]),
                spaceBefore=10,
                spaceAfter=10
            )
            self._add_flowable(hr)

    def handle_endtag(self, tag):
        # Inline tags mapping
        if tag in ('strong', 'b'):
            self.text_accumulator.append('</b>')
        elif tag in ('em', 'i'):
            self.text_accumulator.append('</i>')
        elif tag == 'code':
            if not self.in_pre:
                self.text_accumulator.append('</font>')
        elif tag == 'a':
            self.text_accumulator.append('</a>')
            
        # Block-level tags mapping
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            content = "".join(self.text_accumulator).strip()
            style_map = {
                'h1': 'Heading1', 'h2': 'Heading2', 'h3': 'Heading3',
                'h4': 'Heading4', 'h5': 'Heading5', 'h6': 'Heading6'
            }
            para = Paragraph(content, self.styles[style_map[tag]])
            self._add_flowable(para)
            self.current_block = None
            
        elif tag == 'p':
            content = "".join(self.text_accumulator).strip()
            if content:
                # Use blockquote specific style if we are inside a quote
                style = self.styles['QuoteParaStyle'] if self.in_blockquote else self.styles['Normal']
                para = Paragraph(content, style)
                self._add_flowable(para)
            self.current_block = None
            
        elif tag == 'blockquote':
            if self.blockquote_flowables:
                # Group blockquote items inside a padded/bordered single-cell table
                quote_table = Table([[self.blockquote_flowables]], colWidths=[self.printable_width])
                quote_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(self.theme["quote_bg"])),
                    ('LINELEFT', (0, 0), (-1, -1), 3, colors.HexColor(self.theme["quote_border"])),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 12),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ]))
                self.in_blockquote = False
                self.story.append(quote_table)
                self.story.append(Spacer(1, 8))
                self.blockquote_flowables = []
                
        elif tag == 'pre':
            content = "".join(self.text_accumulator).rstrip('\n')
            pre = Preformatted(content, self.styles['CodeStyle'])
            
            # Wrap in code-block block layout table
            code_table = Table([[pre]], colWidths=[self.printable_width])
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(self.theme["code_bg"])),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor(self.theme["quote_border"])),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ]))
            self.in_pre = False
            self._add_flowable(code_table)
            self._add_flowable(Spacer(1, 8))
            
        elif tag in ('ul', 'ol'):
            if self.list_type_stack:
                self.list_type_stack.pop()
                self.list_counter_stack.pop()
                self._add_flowable(Spacer(1, 4))
                
        elif tag == 'li':
            content = "".join(self.text_accumulator).strip()
            # Get proper list bullet/number prefix
            if self.list_type_stack:
                list_type = self.list_type_stack[-1]
                if list_type == 'ol':
                    prefix = f"{self.list_counter_stack[-1]}.&nbsp;&nbsp;"
                else:
                    prefix = "<font name='Helvetica'>&bull;</font>&nbsp;&nbsp;"
            else:
                prefix = "<font name='Helvetica'>&bull;</font>&nbsp;&nbsp;"
                
            para = Paragraph(f"{prefix}{content}", self.styles['CustomListItem'])
            self._add_flowable(para)
            self.current_block = None
            
        elif tag in ('th', 'td'):
            content = "".join(self.text_accumulator).strip()
            style = self.styles['TableHeaderStyle'] if tag == 'th' else self.styles['TableCellStyle']
            para = Paragraph(content, style)
            self.table_row.append(para)
            self.current_block = None
            
        elif tag == 'tr':
            if self.table_row:
                self.table_data.append(self.table_row)
                
        elif tag == 'table':
            if self.table_data:
                num_cols = max(len(row) for row in self.table_data)
                col_width = self.printable_width / num_cols
                col_widths = [col_width] * num_cols
                
                t = Table(self.table_data, colWidths=col_widths)
                t_style = [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(self.theme["table_header_bg"])),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor(self.theme["quote_border"])),
                ]
                
                # Apply row background alternating pattern
                for idx in range(1, len(self.table_data)):
                    bg = self.theme["table_row_bg2"] if idx % 2 == 1 else self.theme["table_row_bg1"]
                    t_style.append(('BACKGROUND', (0, idx), (-1, idx), colors.HexColor(bg)))
                    
                t.setStyle(TableStyle(t_style))
                self.in_table = False
                self._add_flowable(t)
                self._add_flowable(Spacer(1, 8))

    def handle_data(self, data):
        # Accumulate text inside active text blocks
        if self.current_block or self.in_pre:
            if self.in_pre:
                self.text_accumulator.append(data)
            else:
                escaped_data = html.escape(data)
                clean_data = re.sub(r'\s+', ' ', escaped_data)
                self.text_accumulator.append(clean_data)


def draw_page_decorations(canvas, doc, theme):
    """Draws background color, header, footer, and page numbers."""
    canvas.saveState()
    
    # Paint Page Background
    canvas.setFillColor(colors.HexColor(theme["background"]))
    canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=True, stroke=False)
    
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor(theme["quote_text"]))
    
    # Footer and Page Number
    page_num = canvas.getPageNumber()
    canvas.drawRightString(doc.pagesize[0] - 54, 30, f"Page {page_num}")
    canvas.drawString(54, 30, "Generated by Markdown-to-PDF Utility")
    
    # Horizontal rule above footer
    canvas.setStrokeColor(colors.HexColor(theme["quote_border"]))
    canvas.setLineWidth(0.5)
    canvas.line(54, 42, doc.pagesize[0] - 54, 42)
    
    # Running header on subsequent pages
    if page_num > 1:
        canvas.drawString(54, doc.pagesize[1] - 36, "Markdown to PDF Document")
        canvas.line(54, doc.pagesize[1] - 42, doc.pagesize[0] - 54, doc.pagesize[1] - 42)
        
    canvas.restoreState()


def convert_markdown_to_pdf(input_path, output_path, theme_name):
    """Reads Markdown, parses it into HTML, converts to flowables, and builds the PDF."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input Markdown file not found: {input_path}")
        
    # Standard letter page measurements
    PAGE_WIDTH, PAGE_HEIGHT = letter
    MARGIN = 54
    printable_width = PAGE_WIDTH - 2 * MARGIN
    
    # Set theme
    theme = THEMES.get(theme_name, THEMES["Classic"])
    
    # Read Markdown
    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()
        
    # Convert MD -> HTML (incorporating tables and code block extensions)
    html_content = markdown2.markdown(
        md_content,
        extras=["tables", "fenced-code-blocks", "code-friendly", "break-on-newline"]
    )
    
    # Build document templates
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )
    
    # Setup custom styles and parse
    styles = setup_styles(theme)
    parser = HTMLToFlowablesParser(styles, theme, printable_width)
    parser.feed(html_content)
    
    # Setup running footer/header callback
    page_decorations_callback = partial(draw_page_decorations, theme=theme)
    
    # Render PDF
    doc.build(
        parser.story,
        onFirstPage=page_decorations_callback,
        onLaterPages=page_decorations_callback
    )


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file (.md) into a beautifully styled PDF (.pdf)."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input Markdown file."
    )
    parser.add_argument(
        "--output", "-o",
        help="Path to the output PDF file. Defaults to <input_file_basename>.pdf."
    )
    parser.add_argument(
        "--theme", "-t",
        choices=["Classic", "Modern", "Sleek Dark"],
        default="Classic",
        help="Visual styling theme for the generated PDF. Defaults to Classic."
    )
    
    args = parser.parse_args()
    
    # Resolve output path
    output_path = args.output
    if not output_path:
        base, _ = os.path.splitext(args.input_file)
        output_path = f"{base}.pdf"
        
    try:
        convert_markdown_to_pdf(args.input_file, output_path, args.theme)
        print(f"Successfully converted '{args.input_file}' to '{output_path}' using the '{args.theme}' theme.")
    except Exception as e:
        print(f"Error during PDF conversion: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
