.PHONY: all rps clean

LATEX := pdflatex
LATEXFLAGS := -interaction=nonstopmode -halt-on-error

all: rps

rps:
	@find subjects -name 'RTI*.tex' | while IFS= read -r tex; do \
		name=$$(basename "$$tex" .tex); \
		mkdir -p "RPS/$$name"; \
		$(LATEX) $(LATEXFLAGS) -output-directory "RPS/$$name" "$$tex" || exit 1; \
		rm -f "RPS/$$name"/*.aux "RPS/$$name"/*.log "RPS/$$name"/*.out "RPS/$$name"/*.toc; \
	done

clean:
	@rm -rf RPS
