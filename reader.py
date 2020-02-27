'''
#TODO
[X] show percentage complete
[X] scaling options
[ ] a way to pause
[ ] show times in HH:MM:SS



Commands to read:

M3 S# - set the pen height. 0 is up, 100 is max down (60 is probably better)
	(for this, I think anything above 0 can just be down)
G1 X# Y# - go to the given point
G0 X# Y# - go to the given point a fast as possible (not sure you need this either)

'''



import sys
import time


from pyaxidraw import axidraw

#values
file_name = "NONE"
scale_factor = 1

def seconds2time(raw):

	hours = 0
	minutes = 0
	seconds = 0

	while raw > 3600:
		hours += 1
		raw -= 3600

	while raw > 60:
		minutes += 1
		raw -= 60

	seconds = raw


	min_s = str(minutes)
	if minutes < 10:
		min_s = "0"+str(minutes)

	sec_s = str(int(seconds))
	if seconds < 10:
		sec_s = "0"+str(int(seconds))

	return str(hours)+":"+min_s+":"+sec_s

	
#get arguments
if (len(sys.argv) >= 2):

	#first argument should always be file name
	file_name = sys.argv[1]
	print("opening ",file_name)

	#after that it could be a mix of commands
	i=2
	while i < len(sys.argv):
		arg = sys.argv[i]
		val = sys.argv[i+1]
		i += 2
		#print("arg:",arg,"  val:",val)
		if (arg == "-s"):
			scale_factor = float(val)
		

print("scale: ",scale_factor)

#do our thing
file = open(file_name)
file_lines = file.readlines()
print("lines: ",len(file_lines))

ad = axidraw.AxiDraw()
ad.interactive()
connected = ad.connect()

if not connected:
	print("not connected")
	sys.exit()

ad.options.model=2	#AxiDraw V3/A3

ad.penup()

print("hello dad")

start_time = time.time()

pen_down = False

line_count = 0
for this_line in file_lines:
	line_count += 1
	prc = float(line_count)/float(len(file_lines))
	elapsed_time = time.time() - start_time
	time_left = (elapsed_time / prc) - elapsed_time

	progress_str = str( int(prc*100))
	print ("progress: "+progress_str+"  time: "+seconds2time(elapsed_time)+"  estimated time left: "+seconds2time(time_left))

	#print(this_line[0:-1])	#chopping off the last character because it is a newlien char

	cmd = this_line[0:2]

	if cmd == "M3":
		val = int(this_line[4:])		#get the string to the end of the string and converts to int
		#print(" val:",val)
		pen_down = val > 0
		if pen_down:
			ad.pendown()
		else:
			ad.penup()
		#print(" pen down: ",pen_down)

	if cmd == "G0" or cmd == "G1":
		#we need X and Y
		x_index = this_line.find("X")
		y_index = this_line.find("Y")
		end_index = y_index

		while this_line[end_index] != " " and end_index < len(this_line)-1:
			end_index += 1

		#print(" x index: ",x_index)
		#print(" y index: ",y_index)
		#print(" end index: ",end_index)

		x_val_s = this_line[x_index+1:y_index-1]
		y_val_s = this_line[y_index+1:end_index]
		#print(" x val_s: ",x_val_s)
		#print(" y val_s: ",y_val_s)
		x_val = float(x_val_s) * scale_factor
		y_val = float(y_val_s) * scale_factor
		#print(" x val: ",x_val)
		#print(" y val: ",y_val)

		ad.goto(x_val, y_val)

	#print(cmd)

#cleanup

ad.penup()
ad.moveto(0,0)
ad.disconnect()










