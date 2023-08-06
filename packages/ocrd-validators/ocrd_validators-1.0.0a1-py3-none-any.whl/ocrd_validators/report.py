__all__ = ['ValidationReport']

#
# -------------------------------------------------
#

class ValidationReport(object):
    """
    Container of warnings and errors about a workspace.
    """

    def __init__(self):
        self.notices = []
        self.warnings = []
        self.errors = []

    def __str__(self):
        ret = 'OK' if self.is_valid else 'INVALID'
        if not self.is_valid or self.notices:
            ret += '['
            if self.warnings:
                ret += ' %s warnings' % len(self.warnings)
            if self.errors:
                ret += ' %s errors' % len(self.errors)
            if self.notices:
                ret += ' %s notices' % len(self.notices)
            ret += ' ]'
        return ret

    @property
    def is_valid(self):
        return not self.warnings and not self.errors

    def to_xml(self):
        body = ''
        for k in ['warning', 'error', 'notice']:
            for msg in self.__dict__[k + 's']:
                body += '\n  <%s>%s</%s>' % (k, msg, k)
        return '<report valid="%s">%s\n</report>' % ("true" if self.is_valid else "false", body)

    def add_warning(self, msg):
        self.warnings.append(msg)

    def add_error(self, msg):
        self.errors.append(msg)

    def add_notice(self, msg):
        self.notices.append(msg)

    def merge_report(self, otherself):
        self.notices += otherself.notices
        self.warnings += otherself.warnings
        self.errors += otherself.errors
