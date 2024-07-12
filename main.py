import string

def split_data(data):
  reviews = data.split('\n')
  structured_data = []
  for i in range(0, len(reviews), 2):
      sentiment = reviews[i].split()[-1]
      text = reviews[i+1]

      structured_data.append({'sentiment' : sentiment, 'text' : text})
  return structured_data
 

structured_data = split_data(open("read.txt", encoding="utf-8").read())

for review in structured_data:
    print(f"Sentiment: {review['sentiment']}. Text: {review['text']}")

