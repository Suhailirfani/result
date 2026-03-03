from django import template
from results_app.utils import calculate_grade

register = template.Library()

@register.simple_tag
def get_grade(marks, grading_system, max_marks=100, is_total=False):
    try:
        marks = float(marks)
        max_marks = float(max_marks)
    except (ValueError, TypeError):
        return ''
    return calculate_grade(marks, max_marks, grading_system, is_total=is_total)[0]

@register.simple_tag
def get_grade_name(marks, grading_system, max_marks=100, is_total=False):
    try:
        marks = float(marks)
        max_marks = float(max_marks)
    except (ValueError, TypeError):
        return ''
    return calculate_grade(marks, max_marks, grading_system, is_total=is_total)[1]

@register.filter
def clean_mark(value):
    try:
        val = float(value)
        return int(val) if val.is_integer() else val
    except (ValueError, TypeError):
        return value
