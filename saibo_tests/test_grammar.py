from guidance._grammar import GenRegexTerminalRule, JoinRule, GrammarRule, string, capture


class TestGrammarRules:
    def __init__(self):
        # Initialize any necessary state for testing
        self.used_names_count = 0  # Mimicking the static counter for `num_used_names`

    def test_GenRegexTerminalRule(self):
        # Test the initialization of Gen with regex
        grammar_rule = GenRegexTerminalRule(body_regex="a", stop_regex="b")
        assert isinstance(grammar_rule, GenRegexTerminalRule), f"Expected type Gen, got {type(grammar_rule)}"

    def test_grammar_rule_auto_naming(self):
        # Test the name generation for GrammarFunction
        # Reset the counter
        GrammarRule.num_used_names = 0

        new_rule_name = GrammarRule._new_name()
        assert new_rule_name == "a", f"Expected new name 'a', got {new_rule_name}"
        assert GrammarRule.num_used_names == 1, f"Expected 1 used name, got {GrammarRule.num_used_names}"
        
        new_rule_name = GrammarRule._new_name()
        assert new_rule_name == "b", f"Expected new name 'b', got {new_rule_name}"
        
        # Generate more names to test wrapping
        for i in range(24):
            new_rule_name = GrammarRule._new_name()
        
        assert new_rule_name == "z", f"Expected new name 'z', got {new_rule_name}"
        
        new_rule_name = GrammarRule._new_name()
        assert new_rule_name == "ba", f"Expected new name 'ba', got {new_rule_name} (why not 'aa'?)"

    def test_grammar_rule_add(self):

        # Case 1 - Test adding a GrammarRule instance with a string
        terminal_rule = GenRegexTerminalRule(body_regex="a", stop_regex="b")
        added_rule = terminal_rule + "c"
        assert isinstance(added_rule, JoinRule), f"Expected type Join, got {type(added_rule)}"

        # Test adding two GrammarRule instances
        terminal_rule1 = GenRegexTerminalRule(body_regex="Kobe", stop_regex="Bryant")
        terminal_rule2 = GenRegexTerminalRule(body_regex="Lebron", stop_regex="James")
        added_rule = terminal_rule1 + terminal_rule2
        assert isinstance(added_rule, JoinRule), f"Expected type Join, got {type(added_rule)}"

    def test_add_method(self):

        class MyNumber:
            def __init__(self, value):
                self.value = value

            def __radd__(self, other):
                # Handle right-side addition with integers
                if isinstance(other, int):
                    return self.value + other
                return NotImplemented

        # Create an instance of MyNumber
        num = MyNumber(10)

        # Try adding the integer 5 on the left
        result = 5 + num  # This will call num.__radd__(5)
        assert result == 15, f"Expected 15, got {result}"

        # Try adding the number on the right
        try:
            result = num + 5  # This would call num.__add__(5) if it were defined.
        except TypeError as e:
            assert str(e) == "unsupported operand type(s) for +: 'MyNumber' and 'int'"
        else:
            assert False, "Expected a TypeError but did not get one"
        

    def test_gen_join(self):
        # Test joining two Gen instances
        g_rule1 = GenRegexTerminalRule(body_regex="a", stop_regex="b")
        g_rule2 = GenRegexTerminalRule(body_regex="c", stop_regex="d")
        joined_rule = g_rule1 + g_rule2  # Should result in a Join object
        print(joined_rule)
        assert isinstance(joined_rule, JoinRule), f"Expected type Join, got {type(joined_rule)}"
        assert joined_rule.values == [g_rule1, g_rule2], "Expected elements to match the Gen instances"

    def test_string_rule(self):
        # Test the string function
        string_g_rule = string("hello")
        assert repr(string_g_rule).startswith("b'hello'             <- b'h' b'e' b'l' b'l' b'o'"), f"Expected repr to start with 'b'hello'             <- b'h' b'e' b'l' b'l' b'o'', got {repr(string_g_rule)}"
        assert str(string_g_rule).startswith("{{G|") and str(string_g_rule).endswith("}}"), f"Expected str to start with '{{G|' and end with '}}', got {str(string_g_rule)}"

    def test_join_rule(self):
        # Test the representation of the Join object
        rule1 = GenRegexTerminalRule(body_regex="a", stop_regex="b")
        rule2 = GenRegexTerminalRule(body_regex="c", stop_regex="d")
        joined_rule = JoinRule([rule1, rule2], name="my_join", max_tokens=199)
        expected_repr = 'my_join'
        assert repr(joined_rule).startswith(expected_repr), f"Expected repr to start with '{expected_repr}', got {repr(joined_rule)}"


    def test_capture(self):
        # Test capturing a joined result
        rule1 = GenRegexTerminalRule(body_regex="a", stop_regex="b")
        rule2 = GenRegexTerminalRule(body_regex="c", stop_regex="d")
        joined_rule = JoinRule([rule1, rule2], name="my_join", max_tokens=199)
        captured = capture(joined_rule, "my_captured")

        assert "capture_name=my_captured" in repr(captured), f"Expected 'capture_name='my_captured'' in repr, got {repr(captured)}"


    def run_all_tests(self):
       # ANSI color codes for green, red, and yellow
        green = "\033[92m"
        red = "\033[91m"
        yellow = "\033[93m"
        reset = "\033[0m"
        
        # Dynamically find all methods that start with "test_"
        methods = [method for method in dir(self) if method.startswith("test_") and callable(getattr(self, method))]
        # Sort the methods
        methods.sort()
        for method in methods:
            test_method = getattr(self, method)
            try:
                test_method()
                print(f"{yellow}{method}{reset} - {green}passed{reset}")
            except AssertionError as e:
                print(f"{yellow}{method}{reset} - {red}failed: {e}{reset}")



# Run the tests manually
if __name__ == "__main__":
    tester = TestGrammarRules()

    # Run all tests
    tester.run_all_tests()