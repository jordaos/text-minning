
# File location
old_emotion_list = open('data/sentistrength/sentistrength_data/EmotionLookupTable-old.txt', 'r')

# File location
new_emotion_list = open('data/sentistrength/sentistrength_data/EmotionLookupTable.txt', 'w')

# File location
neutral_words = open('data/sentistrength/words-neutral.txt', 'r')
neutral_words_lines = neutral_words.readlines()

text = old_emotion_list.readlines()
for line in text:
    contains_in_neutral = False
    for neutral_line in neutral_words_lines:
        if "#" in neutral_line:
            continue
        line_contents = [splits for splits in line.split("\t") if splits is not ""]
        word = line_contents[0]
        if word.startswith(neutral_line):
            contains_in_neutral = True
            break
    if not contains_in_neutral:
        new_emotion_list.write(line)


old_emotion_list.close()
new_emotion_list.close()