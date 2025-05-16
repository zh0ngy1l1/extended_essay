# Makefile

CXX = g++
CXXFLAGS = -Ofast -std=c++17
SRC_DIR = cpp_scripts
BINARIES = precompute_g precompute_phigma

all: run

# Compile both binaries
precompute_g: $(SRC_DIR)/precompute_g.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

precompute_phigma: $(SRC_DIR)/precompute_phigma.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

# Run the binaries
run: precompute_g precompute_phigma
	./precompute_g
	./precompute_phigma
	$(MAKE) clean

# Delete the compiled binaries
clean:
	rm -f $(BINARIES)
