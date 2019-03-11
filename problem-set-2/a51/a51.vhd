library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity a51 is
  Port ( 
    clk : in std_logic;
    ld : in std_logic;
    data : in std_logic_vector(63 downto 0) := (others => '0');
    result : out std_logic
  );
end a51;

-- there can be many architectures (aka "ways things work") 
-- defined for a given entity. here we define two, that differ
-- in places where taps are located
ARCHITECTURE first OF a51 IS
  -- this will store internal state of LFSR
  -- initialise it to all-zeroes
  signal q1 : STD_LOGIC_VECTOR(18 downto 0) := (OTHERS => '0');
  signal q2 : STD_LOGIC_VECTOR(21 downto 0) := (OTHERS => '0');
  signal q3 : STD_LOGIC_VECTOR(22 downto 0) := (OTHERS => '0');
BEGIN

  -- this process will be executed each time
  -- a change in either of the signals: clk, ld, data
  -- is detected. this is the "sensitivity list"
  PROCESS(clk, ld, data)
  BEGIN
    -- note that if 'ld = 1' then, regardless of clk the LFSR
    -- will read external data; that's why it's __asynchronous__
    if(ld = '1') 
    then
      q1 <= data(18 downto 0);
      q2 <= data(40 downto 19);
      q3 <= data(63 downto 41);
    -- however, if 'ld' is not operational, then 'clk' will 
    -- cause the state change
    elsif(clk'event and clk = '1')
    then
      -- cyclic shift - as simple as that
      q1(18 downto 1) <= q1(17 downto 0);
      q2(21 downto 1) <= q2(20 downto 0);
      q3(22 downto 1) <= q3(21 downto 0);

      q1(0) <= q1(18) XOR q1(17) XOR q1(16) XOR q1(13);
      q2(0) <= q2(21) XOR q2(20);
      q3(0) <= q3(22) XOR q3(21) XOR q3(20) XOR q3(7);
    end if;
  END PROCESS;

  -- this is not a part of the process - this assignment is
  -- permanent, i.e. "it's always there" - just like a wire 
  -- connecting MSB to the output
  result <= q1(18) XOR q2(21) XOR q3(22);
END first;