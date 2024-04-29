

class CircularList:
    def __init__(self, items, circular=False):
        self.circular = circular
        self.direction = 'forward'
        self.size = len(items)
        if self.size == 2:
            self.circular = True
        self.circular_list = [None] * self.size
        self.current_index = 0  # Pointer to the current position
        for item in items:
            self.append(tuple(item))
        print(self.circular, self.direction)

    def append(self, item):
        """Append an item to the circular list."""
        self.circular_list[self.current_index] = item
        self.current_index = (self.current_index + 1) % self.size

    def pop(self):
        print(self.circular, self.direction)
        if self.circular:
            """Pop an item from the circular list."""
            if self.current_index == 0:
                self.current_index = self.size - 1
            else:
                self.current_index = self.current_index - 1
        else:
            if self.current_index == 0:
                self.direction = 'forward'
                self.current_index = 1
            elif self.current_index == self.size - 1:
                self.direction = 'backward'
                self.current_index -= 1
            elif self.direction == 'forward':
                self.current_index += 1
            elif self.direction == 'backward':
                self.current_index -= 1

        item = self.circular_list[self.current_index]
        return list(item)
    
    def peek(self):
        return self.circular_list[self.current_index]

    def __eq__(self, other):
        if not isinstance(other, list):
            return False
        if len(other) != self.size:
            return False
        queue_set = set(self.circular_list)
        return queue_set == set([tuple(a) for a in other])