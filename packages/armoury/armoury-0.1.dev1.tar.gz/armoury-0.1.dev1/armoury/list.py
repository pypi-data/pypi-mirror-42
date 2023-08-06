class PoweredList(list):
    def in_batches_of(self, batch_size=1):
        for i in range(0, len(self), batch_size):
            yield self[i:i+batch_size]

    def find(self, val):
        for item in self:
            if item == val:
                return item

    detect = find

    def findWhere(listOfDicts, props):
        pass

    def filter(self, func):
        pass
