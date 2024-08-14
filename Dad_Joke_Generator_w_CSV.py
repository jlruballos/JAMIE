import requests
import boto3
import csv

# Function to fetch a dad joke from the API
def fetch_dad_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    joke = response.json().get("joke")
    return joke

# Function to convert text to speech using Amazon Polly and save as a WAV file
def text_to_speech(joke, file_name):
    polly_client = boto3.Session(
        aws_access_key_id='AKIAW3MEFJK7YM2STEAU',
        aws_secret_access_key='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',
        region_name='us-west-2'
    ).client("polly")

    response = polly_client.synthesize_speech(
        VoiceId="Joanna",
        OutputFormat="pcm",
        Text=joke
    )

    # Convert PCM to WAV format
    audio_stream = response["AudioStream"].read()
    with open(file_name, "wb") as file:
        # Writing WAV file header
        file.write(b'RIFF')
        file.write((len(audio_stream) + 36).to_bytes(4, byteorder='little'))
        file.write(b'WAVEfmt ')
        file.write((16).to_bytes(4, byteorder='little'))
        file.write((1).to_bytes(2, byteorder='little'))
        file.write((1).to_bytes(2, byteorder='little'))
        file.write((16000).to_bytes(4, byteorder='little'))
        file.write((32000).to_bytes(4, byteorder='little'))
        file.write((2).to_bytes(2, byteorder='little'))
        file.write((16).to_bytes(2, byteorder='little'))
        file.write(b'data')
        file.write(len(audio_stream).to_bytes(4, byteorder='little'))
        file.write(audio_stream)

# Main function to fetch the joke and save it as a WAV file
def main():
    start_index = 1
    num_jokes = 200
    jokes = {}
    unique_jokes = set()  # A set to store unique jokes

    for i in range(start_index, start_index + num_jokes):
        joke = fetch_dad_joke()
        while joke in unique_jokes:  # Check if the joke is already fetched
            print(f"Duplicate joke detected, refetching...")
            joke = fetch_dad_joke()

        unique_jokes.add(joke)  # Add the new unique joke to the set

        if joke:
            file_name = f"Joke_{i}.wav"
            text_to_speech(joke, file_name)
            jokes[file_name] = f'"{joke}"'
            print(f"Saved: {file_name}")
        else:
            print("Failed to fetch a dad joke.")

    # Write to CSV outside the loop to ensure it happens regardless of duplicates
    with open('jokes.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Text"])
        for joke_name, joke_text in jokes.items():
            writer.writerow([joke_name, joke_text])

if __name__ == "__main__":
    main()
