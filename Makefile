.PHONY: all rps book clean distclean clean-rps

LATEX ?= pdflatex
LATEXFLAGS ?= -interaction=nonstopmode -halt-on-error
LATEXMK ?= latexmk
LATEXMK_ENGINE ?= -xelatex
BOOK_DIR := book
MAIN := $(BOOK_DIR)/main.tex
CACHE_DIR := .cache

all: rps book

rps:
	@find subjects -name 'RTI*.tex' -not -name '* - *' | sort | while IFS= read -r tex; do \
		name=$$(basename "$$tex" .tex); \
		out="RPS/$$name"; \
		mkdir -p "$$out"; \
		printf 'Building %s\n' "$$name"; \
		$(LATEX) -file-line-error $(LATEXFLAGS) -output-directory "$$out" "$$tex" > "$$out/build.log" || { tail -120 "$$out/build.log"; exit 1; }; \
		rm -f "$$out"/*.aux "$$out"/*.log "$$out"/*.out "$$out"/*.toc "$$out/build.log"; \
	done

book:
	@mkdir -p "$(CACHE_DIR)/fontconfig"
	XDG_CACHE_HOME="$(CURDIR)/$(CACHE_DIR)" $(LATEXMK) -cd $(LATEXMK_ENGINE) $(MAIN)

clean:
	$(LATEXMK) -cd -c $(MAIN)
	@if [ -d RPS ]; then \
		find RPS \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.toc' \) -type f | xargs -r rm -f; \
	fi

distclean:
	$(LATEXMK) -cd -C $(MAIN)

clean-rps:
	@rm -rf RPS
