
__all__ = ('ManagerResult',
           'PkgInstalled',
           'PkgUpdated',
           'PkgRemoved',
           'ManagerError',
           'PkgAlreadyInstalled',
           'PkgConflictsWithInstalled',
           'PkgConflictsWithPreexisting',
           'PkgNonexistent',
           'PkgTemporarilyUnavailable',
           'PkgNotInstalled',
           'PkgOriginInvalid',
           'PkgUpToDate',
           'InternalError')


class ManagerResult:

    def __call__(self):
        return self


class PkgInstalled(ManagerResult):

    def __init__(self, pkg):
        super().__init__()
        self.new_pkg = pkg


class PkgUpdated(ManagerResult):

    def __init__(self, old_pkg, new_pkg):
        super().__init__()
        self.old_pkg = old_pkg
        self.new_pkg = new_pkg


class PkgRemoved(ManagerResult):

    def __init__(self, pkg):
        super().__init__()
        self.old_pkg = pkg


class ManagerError(ManagerResult,
                   Exception):
    pass


class PkgAlreadyInstalled(ManagerError):
    pass


class PkgConflictsWithInstalled(ManagerError):

    def __init__(self, pkg):
        super().__init__()
        self.conflicting_pkg = pkg


class PkgConflictsWithPreexisting(ManagerError):

    def __init__(self, folders):
        super().__init__()
        self.folders = folders


class PkgNonexistent(ManagerError):
    pass


class PkgTemporarilyUnavailable(ManagerError):
    pass


class PkgNotInstalled(ManagerError):
    pass


class PkgOriginInvalid(ManagerError):

    def __init__(self, origin):
        super().__init__()
        self.origin = origin


class PkgUpToDate(ManagerError):
    pass


class InternalError(ManagerResult,
                    Exception):

    def __init__(self, error):
        super().__init__()
        self.error = error
