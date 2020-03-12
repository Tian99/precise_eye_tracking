Precise-Eye-Tracker

Knowledge:
    Hough Transform

Main idea:
    1. Break it down into frames
    2. The video contains a lot of nosie, in order to get precise result, blur the frame, and find the threshold of each frame
    3. In order to find the correct thrershold, implement the voting mechanism of Hough Transform(The images are shrinked 8 times to boost up the speed)
    4. Once get the correct threshold, Read in the file, record five states of eye experiment --> cur center --> cue picture --> cue center --> cur disappeared picture --> return to the center and waiting for the next trail
    5. Get the indexed frame based on the time range provided in the file, get x, y, and radius of the circle output by the hough transform.
    6. Plot the data

Improvements:
    1. Vectorize the hough transform
    2. Improve the pre_testing for threshold, also adding the pre_testing for radius
    3. so fking slow!!!!!!

