#!/usr/bin/env python
# -*- coding: utf-8 -*-


class CannotFindError(LookupError):
    def __init__(self, exception_wrapper: Exception or None, *args: object) -> None:
        super().__init__(*args)
        self.exception_wrapper = exception_wrapper


class ErrorInQueryError(LookupError):
    def __init__(self, exception_wrapper: Exception or None, *args: object) -> None:
        super().__init__(*args)
        self.exception_wrapper = exception_wrapper


class TrunkIntegrityError(ValueError):
    def __init__(self, exception_wrapper: Exception or None, *args: object) -> None:
        super().__init__(*args)
        self.exception_wrapper = exception_wrapper
