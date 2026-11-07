
class ReversibleRange:
    def __init__(self, start, stop, step):
        if step == 0:
            raise ValueError("Step cannot be zero")

        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        current = self.start

        if self.step > 0:
            while current < self.stop:
                yield current
                current += self.step
        else:
            while current > self.stop:
                yield current
                current += self.step

    def __reversed__(self):
        length = len(self)

        if length == 0:
            return

        current = self.start + (length - 1) * self.step

        for _ in range(length):
            yield current
            current -= self.step

    def __len__(self):
        if self.step > 0:
            if self.start >= self.stop:
                return 0

            return (self.stop - self.start - 1) // self.step + 1

        else:
            if self.start <= self.stop:
                return 0

            return (self.start - self.stop - 1) // abs(self.step) + 1

    def __contains__(self, value):
        if not isinstance(value, int):
            return False

        if self.step > 0:
            if not self.start <= value < self.stop:
                return False
        else:
            if not self.stop < value <= self.start:
                return False

        return (value - self.start) % self.step == 0


# Sample data
numbers = ReversibleRange(2, 11, 3)

# Normal iteration
print("Normal:", list(numbers))

# Reverse iteration
print("Reversed:", list(reversed(numbers)))

# Length
print("Length:", len(numbers))

# Membership test
print("5 in range:", 5 in numbers)
print("6 in range:", 6 in numbers)

# Negative step example
negative_numbers = ReversibleRange(10, 0, -2)

print("Negative step:", list(negative_numbers))
print("Negative reversed:", list(reversed(negative_numbers)))
