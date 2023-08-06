class PowerList(list):
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
        return [x for x in self if func(x)]

    def any(self, func):
        for item in self:
            if func(item):
                return True

        return False

    def all(self, func):
        for item in self:
            if not func(item):
                return False

        return True

    def reject(self, func):
        return [x for x in self if not func(x)]

    def select(self, func):
        return [x for x in self if func(x)]

    def flatten(self, flat_list=[]):
        for x in self:
            if isinstance(x, list):
                px = PowerList(x)
                px.flatten(flat_list)
            else:
                flat_list.append(x)
        return flat_list

    def pluck(self):
        pass

    def invoke(self, func, args):
        pass

    def sort_by(self):
        pass

    def group_by(self):
        pass

    def count_by(self):
        pass

    def shuffle(self):
        pass

    def sample(self):
        pass

    def slice(self):
        pass

    def partition(self):
        pass

    def compact(self):
        pass

    def union(self):
        pass

    def intersection(self):
        pass

    def difference(self):
        pass

    def zip(self):
        pass

    def unzip(self):
        pass
