SCRIPT = main.py
BUILD_DIR = build
DIST_DIR = dist

.PHONY: all clean
all: build

build:
	python3 -m PyInstaller --onefile  $(SCRIPT)

clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR) 

