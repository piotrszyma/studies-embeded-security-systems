MAIN_FILENAME = gate
TESTBENCH_FILENAME =$(MAIN_FILENAME)_tb

all: build build_test dump

build:
	ghdl -a $(MAIN_FILENAME).vhdl # (a)nalysis
	ghdl -e $(MAIN_FILENAME) # (e)laborate

build_test:
	ghdl -a $(TESTBENCH_FILENAME).vhdl
	ghdl -e $(TESTBENCH_FILENAME)

dump:
	ghdl -r $(TESTBENCH_FILENAME) --vcd=$(MAIN_FILENAME).vcd

gtkwave:
	gtkwave $(MAIN_FILENAME).vcd

clean:
	-rm *.o
	-rm $(MAIN_FILENAME)
	-rm *.cf
	-rm *.vcd