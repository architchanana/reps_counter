import poses
import All_motion_capture
import squats
import jumping_jacks

my_work=str(input("Wht function to you want to use. you wan to check your bicep curls or would like to see in the grid \n"
				+"Choose Between 1 or 2 or 3 or 4\n")).lower()
if my_work=="1" or my_work=="one":
	poses.bicepcurls()
elif my_work=="2" or my_work=="two":
	squats.squats()
elif my_work=="4" or my_work=="four":
	jumping_jacks.jumpingjacks()
else:
	All_motion_capture.facialhanddetection()