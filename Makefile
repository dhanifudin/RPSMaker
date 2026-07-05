.PHONY: all rps clean

LATEX := pdflatex
LATEXFLAGS := -interaction=nonstopmode -halt-on-error

all: rps

rps:
	@find subjects -name 'RTI*.tex' | while IFS= read -r tex; do \
		name=$$(basename "$$tex" .tex); \
		mkdir -p "build/$$name"; \
		$(LATEX) $(LATEXFLAGS) -output-directory "build/$$name" "$$tex" || exit 1; \
		rm -f "build/$$name"/*.aux "build/$$name"/*.log "build/$$name"/*.out "build/$$name"/*.toc; \
	done

clean:
	@rm -rf build
