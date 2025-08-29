# Create Anki flashcards from video subtitles

## The procedure
1. Grab subtitles:
 - Cantril option:
   - In network panel use the `subt` filter 
   - Identify the subtitles file
     - URL example: https://vod-akm.play.hotmart.com/video/rRAW5G1eL1/hls/subtitle/dynamic/rRAW5G1eL1-1650057758899_EN.vtt?hdntl=exp=1717852386~acl=/*~data=hdntl~hmac=8d0558ca704bea4ce538294d0a55ccaab391878563401928fb7b6a39c8c2ad0b&app=aa2d356b-e2f0-45e8-9725-e0efc7b5d29c
   - Copy the response 
   - Paste into the `_input_subtitles.txt` file
 - Udemy option:
   - In network panel use the enter .vtt
   - Identify the subtitles file
   - Copy the request URL
   - Run the `fetch_subtitles.py` script, paste the URL when asked
   - Paste the name of the episode / subfolder, when asked
3. ~~Run the generator, several times using the command: `docker-compose up --build`~~
4. Copy the resulting mindmap summary, either from the UI, or from the relevant folder
  - use: `qa_2_anki_converter.py _results/<video_folder>/summary_v#.txt`
5. Pick the best QA sets
 - from: `_qa_set_v#.txt`
 - into: `qa_set_compiled.txt`
6. Import into Anki
  - use: `qa_2_anki_converter.py _results/<video_folder>/qa_sets/_qa__set_v#.txt`
