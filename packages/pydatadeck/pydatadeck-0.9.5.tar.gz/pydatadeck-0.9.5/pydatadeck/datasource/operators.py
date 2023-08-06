"""
Filter, segment and calculated fields operators related.
"""


class FilterOperators:
    """Filter operators"""
    IN_LIST = 'in_list'
    NOT_IN_LIST = 'not_in_list'
    STR_CONTAIN = 'str_contain'
    STR_NOT_CONTAIN = 'str_not_contain'
    REGEX_MATCH = 'regex_match'
    REGEX_NOT_MATCH = 'regex_not_match'
    EQUAL = 'equal'
    NOT_EQUAL = 'not_equal'
    IS_NULL = 'is_null'
    IS_NOT_NULL = 'is_not_null'
    GT = 'gt'
    GE = 'ge'
    LT = 'lt'
    LE = 'le'


class SegmentOperators(FilterOperators):
    """Segment operators"""


class CalculatedFieldOperators(FilterOperators):
    """Calculated fields operators"""
    