entity logic_gate is
  port (a, b, c : in bit; x, y : out bit);
end logic_gate;

architecture rtl of logic_gate is
begin
    x <= not(not(a or b) or (b or c));
    y <= (b or c) and not(a xor c);
end rtl;