## Creating flashcards procedure
1. Grab subtitles:
 - In network panel use the `subt` filter 
 - Identify the subtitles file

   - URL example: https://vod-akm.play.hotmart.com/video/rRAW5G1eL1/hls/subtitle/dynamic/rRAW5G1eL1-1650057758899_EN.vtt?hdntl=exp=1717852386~acl=/*~data=hdntl~hmac=8d0558ca704bea4ce538294d0a55ccaab391878563401928fb7b6a39c8c2ad0b&app=aa2d356b-e2f0-45e8-9725-e0efc7b5d29c
 - Copy the response 
3. Paste into Flashcard Generator 
 - into: `_input_subtitles.txt`
3. Run the generator, several times
4. Pick the best QA sets
 - from: `_flashcards_v#.txt`
 - into: `flashcards_compiled.txt`
5. Import into Anki
  - source: `flashcards_anki.txt`
