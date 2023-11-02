# Slides for Topic-1 for the "Fundamentals on Data Science" 
## Magister en modelamiento matemático
## Instituto de Matemática - PUCV

### Planificación de las sesiones

| **Sesión** 	|                            **Tema**                           	|
|:----------:	|:-------------------------------------------------------------:	|
|      1     	| K-Means y variaciones                                         	|
|      2     	| Método Espectral                                              	|
|      3     	| Métodos basados en densidad                                   	|
|      4     	| Factorización No Negativa                                     	|
|      5     	| Modelo probabilístico para la extracción de tópicos en textos 	|


- These slides use Pandoc 3.1.1+
- Compile using the following command
  
```
pandoc -t beamer kmeans_variaciones.md -o kmeans_variaciones.pdf --katex --slide-level=2 --dpi=300 --toc --citeproc  --listings --shift-heading-level=0 --pdf-engine=xelatex --template default_mod.latex -f markdown+pipe_tables+backtick_code_blocks+auto_identifiers+strikeout+yaml_metadata_block+implicit_figures+all_symbols_escapable+link_attributes+smart+fenced_divs --verbose
```
