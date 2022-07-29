import numpy as np
import time
import os
import sys
from os.path import join as opj
import pygame
from responsive_objects.button import Button
import shutil
import cv2

SCRIPT_DIR = os.path.dirname(__file__)


def save_video_as_frames(video_path, frames_folder_path):
    cap = cv2.VideoCapture(video_path)
    img_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        filename = opj(frames_folder_path, f"{img_num:06d}.png")
        print(cv2.imwrite(filename, frame))
        img_num += 1
    cap.release()


res_folder = "E:\\frames"
video1 = opj(
    "C:\\Users\\ААА\\Desktop\\OldtownDaysIdeas\\img_backgrounds", "citadel.mp4"
)
save_video_as_frames(video1, res_folder)
