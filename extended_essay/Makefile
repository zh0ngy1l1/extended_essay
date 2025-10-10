# Define the source directory
SRC_DIR := src

# List of LaTeX auxiliary files to be deleted
LATEX_GARBAGE := *.aux *.fdb_latexmk *.fls *.bcf *.blg *.log *.out *.run.xml *.synctex.gz

# Default target: compile, clean, and move PDF
all: compile clean move_pdf

# Compile LaTeX document
compile:
	@echo "Compiling LaTeX document..."
	@cd $(SRC_DIR) && latexmk -pdf -interaction=nonstopmode main.tex

# Alternative compilation using pdflatex (for manual control)
pdflatex:
	@echo "Compiling with pdflatex..."
	@cd $(SRC_DIR) && pdflatex -interaction=nonstopmode main.tex
	@cd $(SRC_DIR) && bibtex main
	@cd $(SRC_DIR) && pdflatex -interaction=nonstopmode main.tex
	@cd $(SRC_DIR) && pdflatex -interaction=nonstopmode main.tex

# Clean up LaTeX auxiliary files
clean:
	@echo "Cleaning up LaTeX garbage..."
	@cd $(SRC_DIR) && rm -f $(LATEX_GARBAGE)

# Move main.pdf to the target directory
move_pdf:
	@echo "Moving main.pdf to the target directory..."
	@if [ -f $(SRC_DIR)/main.pdf ]; then mv $(SRC_DIR)/main.pdf .; else echo "main.pdf not found in $(SRC_DIR)"; fi

# Phony targets
.PHONY: all compile pdflatex clean move_pdf