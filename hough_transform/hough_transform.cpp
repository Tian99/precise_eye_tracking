#include<opencv2/opencv.hpp>
#include<opencv2/core/core.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<iostream>
#include "opencv2/imgproc/imgproc.hpp"

using namespace cv;
using namespace std;

// class Hough_transform{
// public:
// 	Mat image;
// 	Hough_transform(Mat frame = NULL){
// 		image = frame;

// 	}

// };

int main()
{
	string image_path = "../chosen_pic.png";
	Mat img = imread(image_path, CV_LOAD_IMAGE_COLOR);
	// imwrite("test.png", img);
	return 0;
}
