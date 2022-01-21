import argparse

class BlankLinesHelpFormatter (argparse.HelpFormatter):
    # add empty line if help ends with \n
    def _split_lines(self, text, width):
        lines = super()._split_lines(text, width)
        if text.endswith('\n'):
            lines += ['']
        return lines