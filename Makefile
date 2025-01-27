ifeq ($(shell python3 --version 2>/dev/null),)
    ifeq ($(shell python --version 2>/dev/null),)
        $(error Python command not found. Please install Python or ensure it's in your PATH.)
    else
        PYTHON = python
    endif
else
    PYTHON = python3
endif

# Default target when no target is specified
help:
	@echo "Usage:"
	@echo "  make test - Run the test script"
	@echo "  make server - Start the server"

test:
	$(PYTHON) ./tester/tester.py > ./tester/output.txt

server:
	$(PYTHON) ./srcs/dopc.py

.PHONY: help
