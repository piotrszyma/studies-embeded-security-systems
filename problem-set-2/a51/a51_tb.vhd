library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use STD.textio.all;
use ieee.std_logic_textio.all; -- this lib allows to print std_logic_vector to file

-- this is a testbench, but can be any other entity
entity a51_tb is
  end a51_tb;

architecture complex of a51_tb is

  file file_RESULTS : text;

  -- this clock runs at HOW MANY MHz?
  constant clock_period : time := 10 ns;

  -- clock signal
  signal clock : std_logic :=  '0';
  -- IV to initialize internal LSFRs
  signal iv : std_logic_vector(63 downto 0) := (others => '0');
  -- signal to start loading LFSRs
  signal load  : std_logic := '0';
  -- outputs from A51
  signal a51_output : std_logic;

  ------------------------------------
  --  DECLARE COMPONENT UNDER TEST  --
  ------------------------------------
  component a51
    port( 
          clk  : in STD_LOGIC; 
          ld   : in STD_LOGIC;  
          data : in STD_LOGIC_VECTOR(63 downto 0);
          result    : out STD_LOGIC );
  end component;

  ------------------------------------
  --    DECLARE UNIT UNDER TEST     --
  ------------------------------------
  for UUT1 : a51 use entity work.a51(first); -- unit under test
  -- for UUT2 : lfsr use entity work.lfsr(second);

begin
  -- let's create instances of our LFSRs
  UUT1 : a51 port map ( clk => clock, data => iv, ld => load, result => a51_output);
  -- UUT2 : lfsr port map ( clk => clock, ld => load, data => q2, R => LFSR2 );

  -- this will run infinitely, stopping every few ns
  clocker : process
  begin
    clock <= not clock;
    wait for clock_period/2;
  end process;

  -- this will run once and then wait for ever
  init : process 
    variable stdio_line : line;
  begin
    -- readline(input, stdio_line)
    -- TODO: Read from stdin & save as HEX to iv
    file_open(file_RESULTS, "/tmp/a51_output.txt", write_mode);
    -- time to tell LFSRs to load up some data
    load <= '1';
    -- and give it to them (to one of them, at least)
    iv <= x"AAAAAAAAAAAAAAAA";
    -- even though LFSRs are async, let's wait for a bit...
    wait until clock'event and clock = '0';
    -- ... and let them run freely
    load <= '0';
    -- this process is finished, make it wait ad infinitum
    while true loop
      wait until clock'event and clock = '0';
      -- report string'image(a51_output);
      if a51_output = '1' then
        write(stdio_line, string'("1"));
        writeline(file_RESULTS, stdio_line);
      else
        write(stdio_line, string'("0"));
        writeline(file_RESULTS, stdio_line);
      end if;
    end loop;
  end process;

  -- okay, what's going on here? well, the 'clocker' process 
  -- keeps running, changing clk -> NOT clk -> clk -> NOT clk ...
  -- and clk is fed to LFSRs, so they are busy working
  -- the simulation will continue until you kill it, or specify 
  -- the stop time using '--stop-time=XXX' switch to ghdl 

end complex;
