from guidance import guidance



@guidance(stateless=True)
def generate_greeting(lm):
    return lm + "Hello!"


class Counter:
    def __init__(self):
        self.count = 0

    @guidance(stateless=False)
    def increment(self, lm):
        self.count += 1
        return lm + f"Count is {self.count}."


if __name__ == "__main__":
    # Create a simple placeholder for `lm` (in practice, this might be a model object)
    lm = ""

    # Call the stateless function `generate_greeting`
    greeting_result = generate_greeting()
    print(greeting_result("Hello!"))  # Output: "Hello!Hello!"
    

    # # Create an instance of `Counter`
    # counter = Counter()

    # # Call the stateful method `increment` multiple times
    # increment_result_1 = counter.increment(lm)
    # print(increment_result_1)  # Output: "Count is 1."

    # increment_result_2 = counter.increment(lm)
    # print(increment_result_2)  # Output: "Count is 2."

    # increment_result_3 = counter.increment(lm)
    # print(increment_result_3)  # Output: "Count is 3."
