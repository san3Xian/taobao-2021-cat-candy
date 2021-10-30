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
img_taobao_ttlq_icon = "taobao-pics/ttlq-icon.png"

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

    # 针对 浏览15秒(s) 进行识别(更换手机可能需要调整阈值)
    click_location_15s = cv_img_match(
        img_source, img_task_item_undo_15s, methods[2], ocv_image_read_type[1], thresold=0.784)
    print("Task start button location(15s text): ", click_location_15s)
    # locale the completed task icons (更换手机可能需要调整阈值)
    task_done_locations = cv_img_match(
        img_source, img_task_done_icon, methods[2], ocv_image_read_type[1], thresold=0.89)
    
    # 针对 去浏览 按钮进行识别(更换手机可能需要调整阈值)
    click_location_go_view = cv_img_match(
        img_source, img_task_item_undo_view, methods[2], ocv_image_read_type[1], thresold=0.9)
    print("Task start button location(view): ", click_location_go_view)

    click_location = click_location_15s + click_location_go_view
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
            sleep(random.randint(1, 2))

            # 检测是否进入到了天天领钱引导页
            adb_screenshot(img_source)
            click_location_ttlq = cv_img_match(
                img_source, img_taobao_ttlq_icon, methods[2], ocv_image_read_type[1], thresold=0.9)
            if (click_location_ttlq):
                adb_click(click_location_ttlq[0][1], click_location_ttlq[0][0])
            
            # Waiting for the task to be completed, Long start-up times for some tasks
            rand_time = 20 + random.randint(3, 6)
            for i in range(rand_time):
                print("Sleep and wait for the task to be completed: {} / {}".format(i, rand_time), end="\r")
                sleep(1)
            print("")    
            print("Task completed, go back to task list page and wait")
            print("==============================================")
            adb_keyevent_back()
            sleep(random.randint(0, 2))
            # break to refind the runable task
            break
    if (not all_task_state):
      print("runable task not found") # 如果是匹配不到可做的任务，可以根据log中max_loc值调整阈值
      # debug and hold, enter any key in the pic windows to continue
      cv.waitKey(0)
      break
exit()