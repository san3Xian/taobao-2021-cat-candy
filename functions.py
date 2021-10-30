#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os,sys,random
from time import sleep
import cv2 as cv
import numpy as np

def adb_start_app(activity="com.taobao.taobao/com.taobao.browser.BrowserActivity"):
    os.system("adb shell am start -n {}".format(activity))

def adb_screenshot(output_path="screen-capture.png"):
    if(os.path.exists("screen-capture.png")):
        os.remove("screen-capture.png")
    os.system("adb shell screencap -p > screen-capture.png")

def adb_click(x, y):
    os.system("adb shell input tap {} {}".format(x, y))
    print("[adb] Screen clicked (x:{}, y:{})".format(x, y))

def adb_keyevent_back():
    os.system("adb shell input keyevent 4")

def cv_img_match(source_img, template_img, cv_method, cv_img_format=1, thresold=0):
    """
    有待增强:通过提高图片对比度以后再进行图片对比
    应该能增强精度
    """
    tpl = cv.imread(template_img, cv_img_format)
    tpl_h = tpl.shape[0]
    tpl_w = tpl.shape[1]
    print("template image [{}] height: {}, width: {}".format(template_img, tpl_h, tpl_w))

    s_img = cv.imread(source_img, cv_img_format)
    s_img_h = s_img.shape[0]
    s_img_w = s_img.shape[1]
    print("source image height: {}, width: {}".format(s_img_h, s_img_w))

    res = cv.matchTemplate(s_img, tpl, cv_method)
    # print(res)
    # get the most match location and the most mismatched location
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # 数组处理完以后xy位置乱了？w - h ,xy坐标在return时进行互换
    print("max_loc: (h{},w{}) -- {} ".format(max_loc[1], max_loc[0], max_val))
    print("min_loc: (h{},w{}) -- {} ".format(min_loc[1], min_loc[0], min_val))
    
    if (thresold != 0):
        # multi match mode
        loc=[]
        targets = np.where(res >= thresold)
        print("current multi target match thresold: {}".format(thresold))
        for target in zip(*targets[::1]):
            print("multi target match: (h{}, w{}) -- ".format(target[0], target[1]))
            loc.append(target)
            # draw a rectangle at the matching location
            cv.rectangle(s_img, (target[1], target[0]),
                         (target[1] + tpl_w, target[0] + tpl_h), (0, 0, 255), 4)
        print("multi target match {} items".format(len(loc)))
    else:
        # single match mode
        print("single target match: (h{}, w{}) -- ".format(max_loc[1], max_loc[0]))
        # draw a rectangle at the matching location
        ''' Red color '''
        debug_img1 = cv.rectangle(
            s_img, (max_loc[0], max_loc[1]), (max_loc[0] + tpl_w, max_loc[1] + tpl_h), (0, 0, 255), 4)
        
        # the most mismatched location
        # ''' Green color '''
        # debug_img2 = cv.rectangle(
        #     s_img, (min_loc[0], min_loc[1]), (min_loc[0] + tpl_w, min_loc[1] + tpl_h), (0, 255, 0), 1) 
        loc = [max_loc[1], max_loc[0]]
    # show the image match status
    cv.imshow(str(template_img) + '-Image', s_img)
    return loc

def taobao_get_task_state(task_location, done_task_locations, done_task_icon_height):
    """ Determine if this task has been completed
    
    Args:
        task_location: Location of detected task buttons(single location)
        done_task_locations: Multiple locations of detected task status buttons
        done_task_icon_height: Height of the image template used to position the task status icon
    
    Returns: 
        1 Task completed
        0 Task not completed
    """
    print("Checking task state {} with {} completed task locations".format(task_location, len(done_task_locations)))
    for done_task_loc in done_task_locations:
        if(task_location[0] >= done_task_loc[0] and task_location[0] < (done_task_loc[0] + done_task_icon_height) ):
            return 1
    # task is not complete
    return 0

def taobao_check_task_page(source_img, task_doing_icon, task_done_icon):
    """ 画饼
    """