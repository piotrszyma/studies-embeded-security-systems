MAIN_FILENAME = a51
TESTBENCH_FILENAME =$(MAIN_FILENAME)_tb
MAIN_EXTENSION = vhd
STOP_TIME = 1ms

all: build build_test dump

build:
	ghdl -a --ieee=synopsys $(MAIN_FILENAME).$(MAIN_EXTENSION)
	ghdl -e --ieee=synopsys $(MAIN_FILENAME) # (e)laborate

build_test:
	ghdl -a --ieee=synopsys $(TESTBENCH_FILENAME).$(MAIN_EXTENSION)
	ghdl -e --ieee=synopsys $(TESTBENCH_FILENAME)

dump:
	ghdl \
		-r $(TESTBENCH_FILENAME) \
		--vcd=$(MAIN_FILENAME).vcd \
		--stop-time=$(STOP_TIME)

gtkwave:
	gtkwave $(MAIN_FILENAME).vcd

clean:
	-rm *.o
	-rm $(MAIN_FILENAME)
	-rm $(TESTBENCH_FILENAME)
	-rm *.cf
	-rm *.vcd