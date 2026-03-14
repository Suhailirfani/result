def calculate_grade(marks, max_marks, grading_system, is_total=False):
    """
    Calculate the grade and grade name based on marks and grading system.
    Returns a tuple: (grade, grade_name)
    """
    if max_marks == 0:
        return ('', '')
        
    percentage = (marks / max_marks) * 100

    if grading_system == '10_POINT':
        if percentage >= 91: return ('A1', 'Outstanding')
        elif percentage >= 81: return ('A2', 'Excellent')
        elif percentage >= 71: return ('B1', 'Very Good')
        elif percentage >= 61: return ('B2', 'Good')
        elif percentage >= 51: return ('C1', 'Above Average')
        elif percentage >= 41: return ('C2', 'Average')
        elif percentage >= 33: return ('D', 'Marginal')
        else: return ('E', 'Needs Improvement')
        
    elif grading_system == '9_POINT':
        if percentage >= 90: return ('A+', 'Outstanding')
        elif percentage >= 80: return ('A', 'Excellent')
        elif percentage >= 70: return ('B+', 'Very Good')
        elif percentage >= 60: return ('B', 'Good')
        elif percentage >= 50: return ('C+', 'Above Average')
        elif percentage >= 40: return ('C', 'Average')
        elif percentage >= 30: return ('D+', 'Marginal')
        elif percentage >= 20: return ('D', 'Needs Improvement')
        else: return ('E', 'Needs Improvement')
        
    elif grading_system == 'SUNNI_BOARD':
        if is_total:
            if percentage >= 100: return ('Top', 'Top')
            elif percentage >= 96: return ('Topper', 'Topper')
            elif percentage >= 80: return ('Distinction', 'Distinction')
            elif percentage >= 40: return ('Pass', 'Pass')
            else: return ('Failed', 'Failed')
        else:
            if percentage >= 96: return ('A++', '')
            elif percentage >= 91: return ('A+', '')
            elif percentage >= 81: return ('A', '')
            elif percentage >= 71: return ('B+', '')
            elif percentage >= 61: return ('B', '')
            elif percentage >= 51: return ('C+', '')
            elif percentage >= 40: return ('C', '')
            else: return ('D', '')
            
    else: # PERCENTAGE or undefined
        if percentage >= 33:
            return ('Pass', '')
        else:
            return ('Fail', '')
