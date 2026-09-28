class DomainError(Exception):
    pass


class ImageTooLargeError(DomainError):
    pass


class InvalidImageError(DomainError):
    pass


class EmptyUploadError(DomainError):
    pass
