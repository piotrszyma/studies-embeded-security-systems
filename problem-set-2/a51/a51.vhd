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
  signal major : STD_LOGIC;
BEGIN
  PROCESS(clk, ld, data)
  BEGIN
    if(ld = '1')
    then
      q1 <= data(18 downto 0);
      q2 <= data(40 downto 19);
      q3 <= data(63 downto 41);
    elsif(clk'event and clk = '1')
    then
      if (q1(8) xor q2(10)) = '0' then
        major <= q1(8);
      elsif (q2(10) xor q3(10)) = '0' then
        major <= q2(10);
      else
        major <= q3(10);
      end if;

      if q1(8) = major then
          q1(18 downto 1) <= q1(17 downto 0);
          q1(0) <= q1(18) XOR q1(17) XOR q1(16) XOR q1(13);
      end if;

      if q2(10) = major then
        q2(21 downto 1) <= q2(20 downto 0);
        q2(0) <= q2(21) XOR q2(20);
      end if;

      if q3(10) = major then
        q3(22 downto 1) <= q3(21 downto 0);
        q3(0) <= q3(22) XOR q3(21) XOR q3(20) XOR q3(7);
      end if;
    end if;
  END PROCESS;
  result <= q1(18) XOR q2(21) XOR q3(22);
END first;