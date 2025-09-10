import heapq
import re


class BaseHeap:

    def __init__(self, items, key=None):
        self.key = key if key is not None else psuedo_key
        self.heap = [(self.key(i), i) for i in items]
        heapq.heapify(self.heap)

    def __len__(self):
        return len(self.heap)

    def push(self, item):
        return heapq.heappush(self.heap, (self.key(item), item))


class MinHeap(BaseHeap):

    def peek(self):
        return min(self.heap)[1]

    def pop(self):
        return heapq.heappop(self.heap)[1]


class MaxHeap(BaseHeap):

    def peek(self):
        return max(self.heap)[1]

    def pop(self):
        item = max(self.heap)
        self.heap.remove(item)
        return item[1]


def psuedo_key(item):
    return item


def walk(filepath):
    # NOTE: There is an issue where the output from fulllist doesn't
    #       properly cut off the last root. Due to this, there is no
    #       `if root: yield root, file_lines, files`
    #       at the end of the func.
    trunk_re = re.compile(r'trunk: \d+: (.*)')
    file_re = re.compile(r"current: u'(.*)': type:file")
    root = None
    file_lines, files = [], []
    with open(filepath, 'r', encoding='utf8') as f:
        for line in f:
            if match := trunk_re.match(line):
                if root is not None:
                    yield root, file_lines, files
                root = match.group(1)
                files = []
                file_lines = []
            elif match := file_re.match(line):
                files.append(match.group(1))
                file_lines.append(line.strip())


def by_history(filepath):
    trunk_re = re.compile(r'trunk: \d+: (.*)')
    file_re = re.compile(r"current: u'(.*)': type:file")
    root, filename = None, None
    count = 0
    heap = MaxHeap([], key=lambda x: x[1])
    with open(filepath, 'r', encoding='utf8') as f:
        lines = (i for i in f if i.strip())
        for line in lines:
            if filename is not None and line.startswith('historical'):
                count += 1
            elif match := trunk_re.match(line):
                if filename is not None:
                    heap.push((f'{root}/{filename}', count))
                root = match.group(1)
                filename = None
                count = 0
            else:
                if filename is not None and count > 0:
                    heap.push((f'{root}/{filename}', count))
                if match := file_re.match(line):
                    filename = match.group(1)
                else:
                    filename = None
                count = 0
    while True:
        try:
            filepath, count = heap.pop()
            print(f'{count:,} | {filepath}')
            if input('Continue? Y/n: ').lower().strip() == 'n':
                break
        except Exception:
            break


def by_len(filepath):
    heap = MaxHeap([], key=lambda x: x[1])
    for root, _, files in walk(filepath):
        heap.push((root, len(files)))
    while True:
        try:
            trunk, files = heap.pop()
            print(f'{files:,} | {trunk}')
            if input('Continue? Y/n: ').lower().strip() == 'n':
                break
        except Exception:
            break


def by_size(filepath):
    size_re = re.compile(r'size:(\d+)')
    heap = MaxHeap([], key=lambda x: x[0])
    for root, lines, files in walk(filepath):
        for line, f in zip(lines, files, strict=True):
            heap.push(
                (
                    int(size_re.search(line).group(1)),
                    f'{root}/{f}'
                )
            )
    while True:
        try:
            size, file = heap.pop()
            print(f'{size:,} | {file}')
            if input('Continue? Y/n: ').lower().strip() == 'n':
                break
        except Exception:
            break
