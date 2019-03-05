--  A testbench has no ports.
entity logic_gate_tb is
end logic_gate_tb;

architecture behav of logic_gate_tb is
   --  Declaration of the component that will be instantiated.
   component logic_gate
      port (a : in bit; b : in bit; c : in bit; x : out bit; y : out bit);
   end component;

   --  Specifies which entity is bound with the component.
   for logic_gate_0: logic_gate use entity work.logic_gate;
   signal a, b, c, x, y: bit;
begin
   --  Component instantiation.
   logic_gate_0: logic_gate port map (a => a, b => b, c => c, x => x, y => y);

   --  This process does the real job.
   process
      type pattern_type is record
         --  The inputs of the adder.
         a, b, c : bit;
         --  The expected outputs of the adder.
         x, y : bit;
      end record;
      --  The patterns to apply.
      type pattern_array is array (natural range <>) of pattern_type;
      constant patterns : pattern_array :=
        (('0', '0', '0', '0', '0'),
         ('0', '0', '1', '0', '0'),
         ('0', '1', '0', '0', '1'),
         ('0', '1', '1', '0', '0'),
         ('1', '0', '0', '1', '0'),
         ('1', '0', '1', '0', '1'),
         ('1', '1', '0', '0', '0'),
         ('1', '1', '1', '0', '1'));
   begin
      --  Check each pattern.
      for i in patterns'range loop
         --  Set the inputs.
         a <= patterns(i).a;
         b <= patterns(i).b;
         c <= patterns(i).c;
         --  Wait for the results.
         wait for 1 ns;
         --  Check the outputs.
         assert x = patterns(i).x
            report "bad x out value" severity error;
         assert y = patterns(i).y
            report "bad y out value" severity error;
      end loop;
      assert false report "end of test" severity note;
      --  Wait forever; this will finish the simulation.
      wait;
   end process;
end behav;