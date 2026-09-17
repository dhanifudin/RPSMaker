.PHONY: all clean

LATEX := xelatex
LATEXFLAGS := -interaction=nonstopmode -halt-on-error

SRC := $(filter-out preamble.tex,$(wildcard *.tex))
PDF := $(SRC:.tex=.pdf)

all: $(PDF)

%.pdf: %.tex preamble.tex
	$(LATEX) $(LATEXFLAGS) $<
	rm -f $(@:.pdf=.aux) $(@:.pdf=.log) $(@:.pdf=.out) $(@:.pdf=.toc)

clean:
	rm -f *.aux *.log *.out *.toc *.pdf
