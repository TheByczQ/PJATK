
#include "stdafx.h"
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <fstream>


using namespace cv;
using namespace std;



int main(int argc, char** argv)
{
	//Zmienne
	const unsigned int rozm = 150;
	Mat image;
	Mat image_r;
	int CorHor = 10;
	int CorVer = 7;
	Size size(CorHor, CorVer);
	vector <Point2f> outputarray;
	vector <Point2f> outputarray_r;
	vector <Point2f> corners;
	string frame;
	string frame_r;
	vector<Point3f> obj;
	Mat intrinsic = Mat(3, 3, CV_32FC1);
	Mat distCoeffs;
	Mat distCoeffs_r;
	Mat imageUndistorted;
	vector<Mat> rvecs;
	vector<Mat> tvecs;
	vector<vector<Point3f>> object_points;
	vector<vector<Point2f>> image_points;
	vector<vector<Point2f>> image_points_r;
	int lost = 0;
	int licz = 0;
	for (int j = 0; j < (CorHor*CorVer); j++)
		obj.push_back(Point3f(j / 10 * 100, j % 10 * 100, 0.0f));

	//Algorytm
	licz = 1;

	for (int i = 0; i < rozm; i++)
	{
		system("cls");
		frame = "img00" + to_string(i + 125) + "_l.bmp";
		frame_r = "img00" + to_string(i + 125) + "_r.bmp";
		image = imread(frame, IMREAD_GRAYSCALE);
		image_r = imread(frame_r, IMREAD_GRAYSCALE);
		cout << i + 1 << "/" << rozm << endl;
		cout << "pomineto " << lost << endl;
		if (findChessboardCorners(image, size, outputarray) && findChessboardCorners(image_r, size, outputarray_r))
		{
			cornerSubPix(image, outputarray, Size(5, 5), Size(-1, -1), TermCriteria(TermCriteria::COUNT + TermCriteria::EPS, 30, 1e-6));
			cornerSubPix(image_r, outputarray_r, Size(5, 5), Size(-1, -1), TermCriteria(TermCriteria::COUNT + TermCriteria::EPS, 30, 1e-6));
			if (i == 0)
			{
				corners = outputarray;
				image_points.push_back(outputarray);
				image_points_r.push_back(outputarray_r);
				object_points.push_back(obj);
			}
			if (i > 0)
			{
				if (abs(sqrt(pow(corners.at(0).x, 2) + pow(corners.at(0).y, 2)) - sqrt(pow(outputarray.at(0).x, 2) + pow(outputarray.at(0).y, 2))) > 15.0f ||
					abs(sqrt(pow((corners.at(0).x - corners.back().x), 2) + pow((corners.at(0).y - corners.back().y), 2)) - sqrt(pow((outputarray.at(0).x - outputarray.back().x), 2) + pow((outputarray.at(0).y - outputarray.back().y), 2))) > 10.0f ||
					abs(sqrt(pow((corners.at(9).x - corners.at(59).x), 2) + pow((corners.at(9).y - corners.at(59).y), 2)) - sqrt(pow((outputarray.at(9).x - outputarray.at(59).x), 2) + pow((outputarray.at(9).y - outputarray.at(59).y), 2))) > 10.0f)
				{
					image_points.push_back(outputarray);
					image_points_r.push_back(outputarray_r);
					object_points.push_back(obj);
					corners = outputarray;


				}
				else
				{
					lost++;

				}

				licz++;

			}
		}
		else
		{
			lost++;

		}
	}

	//Macierz
	intrinsic.ptr<float>(0)[0] = 1.11510032e+03f;
	intrinsic.ptr<float>(0)[1] = 0.0f;
	intrinsic.ptr<float>(0)[2] = 5.99616631e+02f;
	intrinsic.ptr<float>(1)[0] = 0.0f;
	intrinsic.ptr<float>(1)[1] = 1.14168758e+03f;
	intrinsic.ptr<float>(1)[2] = 5.05226607e+02f;
	intrinsic.ptr<float>(2)[0] = 0.0f;
	intrinsic.ptr<float>(2)[1] = 0.0f;
	intrinsic.ptr<float>(2)[2] = 1.0f;

	Mat in = Mat(3, 3, CV_32FC1);

	Mat image_l;
	image_l = imread("img00125_l.bmp", IMREAD_GRAYSCALE);
	//Mat image_r;
	image_r = imread("img00125_r.bmp", IMREAD_GRAYSCALE);

	//Kalibracja i undistorsja
	fstream plik;
	plik.open("logs.txt", ios::in | ios::out);
	if (plik.good() == true)
	{
		cout << "Uzyskano dostep do pliku!" << std::endl;
		//tu operacje na pliku
	}
	else cout << "Dostep do pliku zostal zabroniony!" << endl;

	plik << calibrateCamera(object_points, image_points, image_l.size(), intrinsic, distCoeffs, rvecs, tvecs, 0, TermCriteria(TermCriteria::COUNT + TermCriteria::EPS, 30, DBL_EPSILON)) << endl; //lewo
	plik << calibrateCamera(object_points, image_points_r, image_r.size(), intrinsic, distCoeffs_r, rvecs, tvecs, 0, TermCriteria(TermCriteria::COUNT + TermCriteria::EPS, 30, DBL_EPSILON)) << endl; //prawa
	
	Mat R, T, E, F, error;

	plik << stereoCalibrate(object_points, image_points, image_points_r, intrinsic, distCoeffs, intrinsic, distCoeffs_r, image_l.size(), R, T, E, F, error, CALIB_FIX_INTRINSIC + CALIB_USE_INTRINSIC_GUESS + CALIB_FIX_K1 + CALIB_FIX_K2 + CALIB_FIX_K3 + CALIB_FIX_K4 + CALIB_FIX_K5, TermCriteria(TermCriteria::COUNT + TermCriteria::EPS, 30, 1e-6)) << endl;

	plik << T;

	Mat imageUndistorted_l;
	Mat imageUndistorted_r;

	/*undistort(image_l, imageUndistorted_l, intrinsic, distCoeffs);
	undistort(image_r, imageUndistorted_r, intrinsic, distCoeffs_r);
	//Wyświetlanie
	imshow("Display windowL", imageUndistorted_l);
	imshow("Display windowR", imageUndistorted_r);*/

	cin.get();
	cin.get();
	waitKey(0); // Wait for a keystroke in the window
	return 0;
}
