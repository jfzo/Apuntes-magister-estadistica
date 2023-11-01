# Slides for Topic-1 for the "Fundamentals on Data Science" 
## Magister en modelamiento matemático
## Instituto de Matemática - PUCV

- These slides use Pandoc
- Compile using the following command
```
pandoc -t beamer kmeans_variaciones.md -o kmeans_variaciones.pdf --katex --slide-level=2 --dpi=300 --toc --citeproc  --listings --shift-heading-level=0 --pdf-engine=xelatex --template default_mod.latex -f markdown+pipe_tables+backtick_code_blocks+auto_identifiers+strikeout+yaml_metadata_block+implicit_figures+all_symbols_escapable+link_attributes+smart+fenced_divs --verbose

```