import argparse

class BlankLinesHelpFormatter (argparse.HelpFormatter):
    """
    Formater function to add new lines in the help messages
    for argparse when '\n' is used.
    """
    # add empty line if help ends with \n
    def _split_lines(self, text, width):
        lines = super()._split_lines(text, width)
        if text.endswith('\n'):
            lines += ['']
        return lines