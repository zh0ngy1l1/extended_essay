# List of LaTeX auxiliary files to be deleted
LATEX_GARBAGE := *.aux *.bbl *.bcf *.blg *.log *.out *.run.xml *.synctex.gz

# Declare phony targets
.PHONY: all clean_micro clean_macro clean_global micro macro global

# Default target: build all
all: micro macro global

# Main phony targets
micro:
	@$(MAKE) clean_micro
	@$(MAKE) build_micro

macro:
	@$(MAKE) clean_macro
	@$(MAKE) build_macro

global:
	@$(MAKE) clean_global
	@$(MAKE) build_global

# Cleaning rules
clean_micro:
	@echo "Cleaning LaTeX garbage in micro..."
	@cd micro && rm -f $(LATEX_GARBAGE)

clean_macro:
	@echo "Cleaning LaTeX garbage in macro..."
	@cd macro && rm -f $(LATEX_GARBAGE)

clean_global:
	@echo "Cleaning LaTeX garbage in global..."
	@cd global && rm -f $(LATEX_GARBAGE)

# Build rules
build_micro:
	@echo "Moving micro/main.pdf to main_micro.pdf..."
	@mv -f micro/main.pdf main_micro.pdf

build_macro:
	@echo "Moving macro/main.pdf to main_macro.pdf..."
	@mv -f macro/main.pdf main_macro.pdf

build_global:
	@echo "Moving global/main.pdf to main_global.pdf..."
	@mv -f global/main.pdf main_global.pdf
