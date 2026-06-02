from django.test import TestCase
from results_app.utils import calculate_grade

class HadiyaGradingSystemTests(TestCase):
    def test_hadiya_grading_scale(self):
        # 20 - 39 - D
        self.assertEqual(calculate_grade(39, 100, 'HADIYA'), ('D', 'D'))
        self.assertEqual(calculate_grade(20, 100, 'HADIYA'), ('D', 'D'))
        
        # below 20 - e
        self.assertEqual(calculate_grade(19, 100, 'HADIYA'), ('e', 'e'))
        self.assertEqual(calculate_grade(0, 100, 'HADIYA'), ('e', 'e'))
        
        # 40 - 49 - c
        self.assertEqual(calculate_grade(40, 100, 'HADIYA'), ('c', 'c'))
        self.assertEqual(calculate_grade(45, 100, 'HADIYA'), ('c', 'c'))
        self.assertEqual(calculate_grade(49, 100, 'HADIYA'), ('c', 'c'))
        
        # 50 - 59 - c+
        self.assertEqual(calculate_grade(50, 100, 'HADIYA'), ('c+', 'c+'))
        self.assertEqual(calculate_grade(55, 100, 'HADIYA'), ('c+', 'c+'))
        self.assertEqual(calculate_grade(59, 100, 'HADIYA'), ('c+', 'c+'))
        
        # 60 - 69 - b
        self.assertEqual(calculate_grade(60, 100, 'HADIYA'), ('b', 'b'))
        self.assertEqual(calculate_grade(65, 100, 'HADIYA'), ('b', 'b'))
        self.assertEqual(calculate_grade(69, 100, 'HADIYA'), ('b', 'b'))
        
        # 70 - 79 - b+
        self.assertEqual(calculate_grade(70, 100, 'HADIYA'), ('b+', 'b+'))
        self.assertEqual(calculate_grade(75, 100, 'HADIYA'), ('b+', 'b+'))
        self.assertEqual(calculate_grade(79, 100, 'HADIYA'), ('b+', 'b+'))
        
        # 80 - 89 - a
        self.assertEqual(calculate_grade(80, 100, 'HADIYA'), ('a', 'a'))
        self.assertEqual(calculate_grade(85, 100, 'HADIYA'), ('a', 'a'))
        self.assertEqual(calculate_grade(89, 100, 'HADIYA'), ('a', 'a'))
        
        # 90 - 100 - a+
        self.assertEqual(calculate_grade(90, 100, 'HADIYA'), ('a+', 'a+'))
        self.assertEqual(calculate_grade(95, 100, 'HADIYA'), ('a+', 'a+'))
        self.assertEqual(calculate_grade(100, 100, 'HADIYA'), ('a+', 'a+'))
        
    def test_different_max_marks(self):
        # test mapping percentage correctly with max_marks != 100
        # 30 out of 50 = 60% -> 'b'
        self.assertEqual(calculate_grade(30, 50, 'HADIYA'), ('b', 'b'))
        # 19 out of 50 = 38% -> 'D'
        self.assertEqual(calculate_grade(19, 50, 'HADIYA'), ('D', 'D'))
        # 9 out of 50 = 18% -> 'e'
        self.assertEqual(calculate_grade(9, 50, 'HADIYA'), ('e', 'e'))
        # 45 out of 50 = 90% -> 'a+'
        self.assertEqual(calculate_grade(45, 50, 'HADIYA'), ('a+', 'a+'))
