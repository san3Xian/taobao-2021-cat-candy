#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from functions import *

img_source = "screen-capture.png"
img_task_entry1 = "taobao-pics/task-entry-icon1.png"
img_debug_template = "taobao-pics/match-test-pic.png"
img_task_item_undo_godo = "taobao-pics/task_item_undo_godo.png"
img_task_item_undo_view = "taobao-pics/task_item_undo_view2.png"
img_task_item_undo_15s = "taobao-pics/task_item_15_sec.png"
img_task_done_icon = "taobao-pics/task_done_icon.png"

adb_screenshot(img_source)

methods = [cv.TM_SQDIFF_NORMED, cv.TM_CCORR_NORMED, cv.TM_CCOEFF_NORMED]
ocv_image_read_type = [cv.IMREAD_COLOR,
                       cv.IMREAD_GRAYSCALE, cv.IMREAD_UNCHANGED]

if(len(sys.argv) == 1):
    # locate the task list button
    click_location = cv_img_match(img_source, img_task_entry1, methods[2])
    print("Task list button location: ", click_location)
    adb_click(click_location[1], click_location[0])
else:
    print("Already at task list page")

while(1):
    sleep(random.randint(1, 3))
    # begin to find the runable task buttons
    adb_screenshot(img_source)
    # 针对 去浏览 按钮进行识别，精确率不高
    #click_location = cv_img_match(
    #    img_source, img_task_item_undo_view, methods[2], ocv_image_read_type[1], thresold=0.9)
    #print("task item button location(view): ", click_location)

    # 针对浏览15秒进行识别(更换手机可能需要调整阈值)
    click_location = cv_img_match(
        img_source, img_task_item_undo_15s, methods[2], ocv_image_read_type[1], thresold=0.784)
    print("Task start button location(15s text): ", click_location)
    # locale the completed task icons (更换手机可能需要调整阈值)
    task_done_locations = cv_img_match(
        img_source, img_task_done_icon, methods[2], ocv_image_read_type[1], thresold=0.89)
    
    done_task_icon_height = cv.imread(img_task_done_icon).shape[0]
    # Determining whether a task has been performed or not in the for section
    all_task_state = 0
    for task_loc in click_location:
        # Determine if this task is finished
        this_task_state = taobao_get_task_state(task_loc, task_done_locations, done_task_icon_height)
        if (not this_task_state):
            print("Got a undo task, begin to start the task: {}".format(task_loc))
            all_task_state = 1
            adb_click(task_loc[1], task_loc[0])
            # Waiting for the task to be completed
            rand_time = 20 + random.randint(4, 8)
            for i in range(rand_time):
                print("Sleep and wait for the task to be completed: {} / {}".format(i, rand_time), end="\r")
                sleep(1)
            print("")    
            print("Task completed, go back to task list page and wait")
            print("==============================================")
            adb_keyevent_back()
            sleep(2)
            # break to refind the runable task
            break
    if (not all_task_state):
      print("runable task not found") # 如果是匹配不到可做的任务，可以根据log中max_loc值调整阈值
      # debug and hold, enter any key in the pic windows to continue
      cv.waitKey(0)
      break
exit()