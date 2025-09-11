# Source directories
SRC_DIRS := micro macro global

# List of LaTeX auxiliary files to be deleted
LATEX_GARBAGE := *.aux *.fdb_latexmk *.fls *.bcf *.blg *.log *.out *.run.xml *.synctex.gz

# Default target: move all PDFs
all: $(SRC_DIRS:%=move_pdf_%)

# Clean all aux files everywhere
clean:
	@echo "Nuking LaTeX garbage everywhere..."
	@find $(SRC_DIRS) -type f \( \
		$(foreach ext,$(LATEX_GARBAGE),-name "$(ext)" -o) -false \
	\) -delete

# Move PDF rule for each dir
move_pdf_%:
	@echo "Moving $*/main.pdf -> main_$*.pdf"
	@mv $*/main.pdf ./main_$*.pdf

# Phony targets
.PHONY: all clean $(SRC_DIRS:%=move_pdf_%)
