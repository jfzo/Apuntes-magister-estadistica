
PANDOC_OPTIONS=--standalone --syntax-highlighting=pygments -f markdown+pipe_tables+backtick_code_blocks+auto_identifiers+strikeout+yaml_metadata_block+implicit_figures+all_symbols_escapable+link_attributes+smart+fenced_divs 
PANDOC_XELATEX_PDF_OPTIONS=--dpi=300 --slide-level 2 --toc --citeproc --syntax-highlighting=pygments --shift-heading-level=0 --data-dir=../pandoc --template templates/default_mod.latex -H ../pandoc/templates/preamble.tex --pdf-engine xelatex -V classoption:aspectratio=169 -V classoption=t -t beamer

SRC_DIR := .
OUT_DIR := output

# 1. Función nativa de Make para buscar archivos recursivamente (reemplaza a 'find')
rwildcard=$(wildcard $1$2) $(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2))

# 2. Buscar todos los .md y filtrar (excluir) los que estén en la carpeta output
ALL_MD_FILES := $(call rwildcard,,*.md)
MD_FILES := $(filter-out $(OUT_DIR)/%, $(ALL_MD_FILES))

PDF_FILES := $(patsubst %.md,$(OUT_DIR)/pdf/%.pdf,$(MD_FILES))

# 3. Detectar el sistema operativo para usar el comando de carpetas correcto
ifeq ($(OS),Windows_NT)
	# En Windows, convertimos las barras "/" a "\" y verificamos si existe
	MKDIR = if not exist "$(subst /,\,$(dir $@))" mkdir "$(subst /,\,$(dir $@))"
else
	# En Linux/Mac usamos mkdir -p
	MKDIR = mkdir -p $(dir $@)
endif

pdf: $(PDF_FILES)
	@echo "✓ PDF conversion done"

# PDF generation rule
$(OUT_DIR)/pdf/%.pdf: %.md
	@$(MKDIR)
	pandoc $(PANDOC_OPTIONS) $(PANDOC_XELATEX_PDF_OPTIONS) -o $@ -V graphicspath="$(<D)/imgs" $<

all: pdf