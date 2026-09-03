.PHONY: all rps book pedoman clean distclean clean-rps clean-pedoman

LATEX ?= pdflatex
LATEXFLAGS ?= -interaction=nonstopmode -halt-on-error
LATEXMK ?= latexmk
LATEXMK_ENGINE ?= -xelatex
BOOK_DIR := book
MAIN := $(BOOK_DIR)/main.tex
CACHE_DIR := .cache
PEDOMAN_DIR := docs/pedoman-laboratorium
PEDOMAN_OUT := pedoman-lab

all: rps book pedoman

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

pedoman:
	@mkdir -p "$(CACHE_DIR)/fontconfig"
	@find $(PEDOMAN_DIR) -name '*.tex' -not -name 'preamble.tex' | sort | while IFS= read -r tex; do \
		name=$$(basename "$$tex" .tex); \
		out="$(CURDIR)/$(PEDOMAN_OUT)/$$name"; \
		mkdir -p "$$out"; \
		printf 'Building %s\n' "$$name"; \
		(cd "$(CURDIR)/$(PEDOMAN_DIR)" && \
		 XDG_CACHE_HOME="$(CURDIR)/$(CACHE_DIR)" xelatex -file-line-error -interaction=nonstopmode -halt-on-error \
			-output-directory "$$out" "$$name.tex" > "$$out/build.log" 2>&1 \
			|| { tail -120 "$$out/build.log"; exit 1; } && \
		 XDG_CACHE_HOME="$(CURDIR)/$(CACHE_DIR)" xelatex -file-line-error -interaction=nonstopmode -halt-on-error \
			-output-directory "$$out" "$$name.tex" >> "$$out/build.log" 2>&1 \
			|| { tail -120 "$$out/build.log"; exit 1; }); \
		rm -f "$$out"/*.aux "$$out"/*.log "$$out"/*.out "$$out"/*.toc "$$out"/*.xdv "$$out/build.log"; \
	done

clean:
	$(LATEXMK) -cd -c $(MAIN)
	@if [ -d RPS ]; then \
		find RPS \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.toc' \) -type f | xargs -r rm -f; \
	fi
	@if [ -d $(PEDOMAN_OUT) ]; then \
		find $(PEDOMAN_OUT) \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.toc' \) -type f | xargs -r rm -f; \
	fi

distclean:
	$(LATEXMK) -cd -C $(MAIN)

clean-rps:
	@rm -rf RPS

clean-pedoman:
	@rm -rf $(PEDOMAN_OUT)
