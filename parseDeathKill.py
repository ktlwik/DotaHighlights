from moviepy.editor import VideoFileClip, concatenate_videoclips, concatenate_audioclips
cnt = 0
#print(1)

death_time = []
window = 30
step = 10
highlight_time = 500
clip_time = 4080 

def check (x, mp):
	cur_time = 0
	ans = 0
	#print (x)
	while (cur_time < clip_time) :
		if mp[cur_time] >= x:
			ans += window
			cur_time += window
			while (mp[cur_time] > 0):
				cur_time += step
				ans += step
		else :
			cur_time += step 

	if (ans >= highlight_time):
		return True
	return False

f = open('output.txt', 'r')

for line in f:
	r = line.split(" ")
	#print (r[2])
	
	#f (r[2] == "type:DOTA_COMBATLOG_DEATH" and r[8] == "is_attacker_hero:true" and r[10] == "is_target_hero:true"):
	if (r[2] == "type:DOTA_COMBATLOG_DEATH" and line.find("assist_players") != -1):
		cnt = cnt + 1
		#print (r[15], r[16])
		timestamp = r[15]
		if (timestamp.startswith("timestamp") == False):
			timestamp = r[16]
		timestamp = timestamp.split(":")[1]
		#print (timestamp)
		x = float(timestamp)
		x -= 160
		death_time.append(x)
		#m = 0
		#while (x > 60):
		#	m += 1
		#	x -= 60
		#print(m, x)
		#print(timestamp)
		#print(r)
		#if (cnt > 10):
		#	break
#print(death_time)

mp = {}
for cur_time in range(0, clip_time, step):
	death_count = 0
	for dead_time in death_time:
		if (dead_time >= cur_time and dead_time <= cur_time + window) :
			death_count += 1
	#print (death_count)
	mp[cur_time] = death_count

l = 0
r = 20
ans = 0
for i in range(10) :
	m = (l + r) / 2
	#print (l, r, m)
	if (check (m, mp) == True) :
		l = m + 1
		ans = m
	else :
		r = m - 1

cur_time = 0
cut_frames = []
while (cur_time < clip_time) :
	if mp[cur_time] >= ans:
		beg_time = cur_time
		cur_time += window
		while (mp[cur_time] > 0):
			cur_time += step
		cut_frames.append([beg_time, cur_time])
	else :
		cur_time += step 
#print(ans)
#print(cut_frames)

video = VideoFileClip("VP vs Liquid.mp4")
video_1 = video.subclip(cut_frames[0][0], cut_frames[0][1]) 
video_2 = video.subclip(cut_frames[1][0], cut_frames[1][1]) 

final_video = concatenate_videoclips([video_1, video_2])
for i in range(2, len(cut_frames)):
	video_i = video.subclip(cut_frames[i][0], cut_frames[i][1])  
	final_video = concatenate_videoclips([final_video, video_i])

final_video.write_videofile("highlight_final.mp4")