SCRIPT = main.py
BUILD_DIR = build
DIST_DIR = dist
BRIEFCASE_PYTHON = /home/matias/bees/bin/python

.PHONY: all clean dist
all: build

build:
	python3 -m PyInstaller --onefile  $(SCRIPT)

dist:
	$(BRIEFCASE_PYTHON) -m briefcase build
	$(BRIEFCASE_PYTHON) -m briefcase package
	DEB_FILE="$$(ls -t dist/breakingdown_*_amd64.deb 2>/dev/null | head -n1)"; \
		if [ -z "$$DEB_FILE" ]; then \
			echo "No Debian package found in dist/"; \
			exit 1; \
		fi; \
		sudo apt install --reinstall "$$DEB_FILE"
	sudo pkill -x breakingdown || true
	/usr/bin/breakingdown

clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR) 
