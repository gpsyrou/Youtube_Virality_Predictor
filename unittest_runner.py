import unittest

loader = unittest.TestLoader()
start_path = '/Users/georgiosspyrou/Desktop/GitHub/Projects/Youtube_Likes_Predictor'

suite = loader.discover(start_path)

runner = unittest.TextTestRunner()
runner.run(suite)
