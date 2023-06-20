import time
import requests
import re
import random
import os
import json


token = '' # add your token here or a bot token

sendto = '' # this is the channel id of the channel you want to send the message to


def send(message, auth, channel):
	r = requests.post(
			url=f"https://discord.com/api/v9/channels/{channel}/messages",
			data={'content': message},
			headers=({'authorization': auth})
		)
	print(r.status_code)
	return r


def edit(messageid, message, auth, channel):
	r = requests.patch(
			url=f"https://discord.com/api/v9/channels/{channel}/messages/{messageid}",
			data={'content': message},
			headers=({'authorization': auth})
		)
	print(r.status_code)
	return r

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'splittext.txt'), 'r') as file:
	text = file.read()

# print(text)


def split_text(text):
    # Split the text into chunks using the string "[split]"
    chunks = text.split("[split]")

    # Initialize the list of chunks
    result = []

    # Loop through the chunks and add them to the result list
    for chunk in chunks:
        # Split the chunk into sentences
        sentences = re.split(r'[\n]\s*', chunk)

        # Initialize the list of chunks for this chunk's sentences
        current_chunk = ''

        # Loop through the sentences and add them to the current chunk
        for sentence in sentences:
            # If adding the sentence to the current chunk would make it too long, add the current chunk to the result list and start a new one
            if len(current_chunk) + len(sentence) > 1940:
                result.append(current_chunk)
                current_chunk = ''

            # Add the sentence to the current chunk
            current_chunk += sentence + '\n'

        # Add the final chunk to the result list
        result.append(current_chunk)

    # Print the result list
    print(result)

    return result


# Get the list of chunks
chunks = split_text(text)

# Get the total number of chunks
total_chunks = len(chunks)

# Calculate the percentage of the file that has been sent
percent_sent = 1 / total_chunks * 100

# Send the chunk along with the percentage
message = f'{chunks[4]}\n## ({percent_sent:.2f}% sent)'
messageid = json.loads(send(message, token, sendto).text)["id"]

try:
	for i in range(5, total_chunks):
		# Calculate the percentage of the file that has been sent
		percent_sent = (i + 1) / total_chunks * 100
	
		# Send the chunk along with the percentage
		if int(percent_sent) != 100:
			message = f'{chunks[i]}\n## ({percent_sent:.2f}% sent)'
		else:
			message = chunks[i]
		tempmessageid = messageid
		edit_message = chunks[i-1]
		edit_response = edit(tempmessageid, edit_message, token, sendto)
		messageid = json.loads(send(message, token, sendto).text)["id"]
		print(i)
		# Wait for 2 seconds
		time.sleep(random.uniform(2.5, 3.5))
except KeyboardInterrupt:
    pass
