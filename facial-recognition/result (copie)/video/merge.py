from moviepy.editor import VideoFileClip, concatenate_videoclips


clip = []

for i in range(10):
	clip.append(VideoFileClip(f"chunk.{i}.mp4"))
	

# Concatenate the clips
final_clip = concatenate_videoclips(clip)

# Write the result to a file
final_clip.write_videofile("final.mp4")
