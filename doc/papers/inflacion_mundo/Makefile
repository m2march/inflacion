all: inflacion_mundo.pdf

IMGS=imgs/cpi_vs_m.pdf correlacion_inflacion.tex.done

correlacion_inflacion.tex.done: \
	correlacion_inflacion.tex.tpl \
	imgs/cpi_vs_m.json 
	template_fill $^ > $@

inflacion_mundo.pdf: inflacion_mundo.tex $(IMGS)
	pdflatex inflacion_mundo.tex
	bibtex inflacion_mundo.aux
	pdflatex inflacion_mundo.tex
	pdflatex inflacion_mundo.tex
