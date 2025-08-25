import os
import re


def find(filepath, pattern=None, ipattern=None, directory=True, file=True):
    is_match = pattern_match(pattern=pattern, ipattern=ipattern)
    trunk_re = re.compile(r'trunk: \d+: (.*)')
    file_re = re.compile(r"current: u'(.*)': type:file")
    with open(filepath, 'r', encoding='utf8') as f:
        deleted_branch = False
        root = None
        try:
            for line in f:
                if deleted_branch and not line.startswith('trunk'):
                    continue
                if line.startswith('deleted_branch'):
                    deleted_branch = True
                elif not line.startswith('deleted'):
                    deleted_branch = False
                    if match := trunk_re.match(line):
                        root = match.group(1)
                        if directory and is_match(root):
                            yield root
                    if file and (match := file_re.match(line)):
                        group = match.group(1)
                        if is_match(group):
                            yield os.path.join(root, group)
        except KeyboardInterrupt:
            return


def pattern_match(*, pattern, ipattern):
    patterns = []
    if pattern is not None:
        patterns.append(re.compile(clean(pattern)))
    if ipattern is not None:
        patterns.append(re.compile(clean(ipattern), re.IGNORECASE))

    def compute(line):
        return all(r.match(line) for r in patterns)

    return compute


def clean(pattern):
    output = []
    puncs = {'.', '\\'}
    for index, char in enumerate(str(pattern)):
        if char == '*' and (index == 0 or pattern[index - 1] not in puncs):
            output.append('.')
        output.append(char)
    return ''.join(output)
