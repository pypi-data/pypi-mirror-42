#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SqlOperationEnum(object):
    u"""Типы операций в sql"""
    SELECT = 's'
    INSERT = 'i'
    UPDATE = 'u'
    DELETE = 'd'
    COMMIT = 'c'
    SAVEPOINT = 'sp'
    JOIN = 'j'
    DISTINCT = 'di'
    GROUP_BY = 'gb'

    values = {
        SELECT: 'SELECT',
        INSERT: 'INSERT',
        UPDATE: 'UPDATE',
        DELETE: 'DELETE',
        COMMIT: 'COMMIT',
        SAVEPOINT: 'SAVEPOINT',
        JOIN: 'JOIN',
        DISTINCT: 'DISTINCT',
        GROUP_BY: 'GROUP BY',
    }

    @classmethod
    def operations(cls):
        return cls.values.items()