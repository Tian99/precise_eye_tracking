#!/usr/bin/env python3
import matplotlib.pyplot as plt
import timeit
from eye_circle import circle_vectorized, circle

frame=threshold(cv2.imread('./analysis_set/kang00013.png'),100,8)

tcv = timeit.timeit(lambda: circle_vectorized(frame), number=10)
tc = timeit.timeit(lambda: circle("",frame), number=10)

# >>> tcv
# 27.77392174769193
# >>> tc
# 47.4045549579896

# also see the nice plots!
# plt.ion()
circle_vectorized(frame, show=True)
