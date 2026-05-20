PANDOC_OPTIONS=--standalone --highlight-style pygments -f markdown+pipe_tables+backtick_code_blocks+auto_identifiers+strikeout+yaml_metadata_block+implicit_figures+all_symbols_escapable+link_attributes+smart+fenced_divs 
PANDOC_XELATEX_PDF_OPTIONS=--dpi=300 --slide-level 2 --toc --citeproc --highlight-style=pygments --shift-heading-level=0 --data-dir=../pandoc --template templates/default_mod.latex -H ../pandoc/templates/preamble.tex --pdf-engine xelatex -V classoption:aspectratio=169 -t beamer
#pandoc $(PANDOC_OPTIONS) $(PANDOC_XELATEX_PDF_OPTIONS) -o $@ $<

SRC_DIR := .
OUT_DIR := output

# Find all markdown files recursively
MD_FILES := $(shell find $(SRC_DIR) -type f -name "*.md" ! -path "$(OUT_DIR)/*")

PDF_FILES := $(patsubst $(SRC_DIR)/%.md,$(OUT_DIR)/pdf/%.pdf,$(MD_FILES))


pdf: $(PDF_FILES)
	@echo "✓ PDF conversion done"

# PDF generation rule
$(OUT_DIR)/pdf/%.pdf: $(SRC_DIR)/%.md
	@mkdir -p $(dir $@)
	pandoc $(PANDOC_OPTIONS) $(PANDOC_XELATEX_PDF_OPTIONS) -o $@ $<


all: pdf 
