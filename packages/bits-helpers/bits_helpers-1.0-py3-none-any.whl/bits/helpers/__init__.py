"""Helpers class file."""


class Helpers(object):
    """Helpers class."""

    def chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in xrange(0, len(l), n):
            yield l[i:i + n]