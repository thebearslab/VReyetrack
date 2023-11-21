flow of project:

- save mp4 in folder
- download anaconda
- USE process.py to split video into frames
- USE labelme to determine AOIs
- USE compare_eye_anno.py to determine if hitting points fall within AOIs
- USE anaconda (?) to produce files for each participant

Scripts explicitly mentioned:
Process_video.py (2)
Geom3.py
Process.py (2)
Compare_eye_anno.py (5)

Input:
Mp4 360 video
User decision: do your video stills need to be cropped vertically and flipped horizontally?
User decision: What is the desired frequency of your video stills? (.5 second intervals is current)
User decision: what naming convention do you want to use for the video stills? (WSU_ED_001 is current)
Determine AOI on stills
User decision: do you want the video paused at the beginning and endings? If so, for how long?
User decision: Is your video paused? If so, where and for how long?

Output:

- a file in each participant folder ending in (e.g.,) ...001_EYE2 with the
  ending ...result.csv. This file contains columns for each AOI that was specified and whether or not the participant’s hitting points fell within the specified AOI at each half second interval.
- an image at each time stamp with depictions of the specified AOIs and the hitting point depicted as a green dot.

Software needed:
Labelme
