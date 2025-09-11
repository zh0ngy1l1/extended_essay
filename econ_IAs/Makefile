# Define the source directory
SRC_DIR := src

# List of LaTeX auxiliary files to be deleted
LATEX_GARBAGE := *.aux *.bbl *.bcf *.blg *.log *.out *.run.xml *.synctex.gz

# Target to clean up LaTeX garbage and move main.pdf
all: clean move_pdf

# Clean up LaTeX auxiliary files
clean:
	@echo "Cleaning up LaTeX garbage..."
	@cd $(SRC_DIR) && rm -f $(LATEX_GARBAGE)

# Move main.pdf to the target directory
move_pdf:
	@echo "Moving main.pdf to the target directory..."
	@mv $(SRC_DIR)/main.pdf .

# Phony targets
.PHONY: all clean move_pdf