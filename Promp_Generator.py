import boto3

# Function to convert text to speech using Amazon Polly and save as a WAV file
def text_to_speech(phrase, file_name):
    polly_client = boto3.Session(
        aws_access_key_id='AKIAW3MEFJK7YM2STEAU',
        aws_secret_access_key='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',
        region_name='us-west-2'
    ).client("polly")

    response = polly_client.synthesize_speech(
        VoiceId="Joanna",
        OutputFormat="pcm",
        Text=phrase
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

# Main function to save phrases as WAV files
def main():
    phrases = [
"Knock Knock....Who's there?....Vladislav. Vladislav who...Vladislav. Baby don't hurt me, don't hurt me no more."
]

    for i, phrase in enumerate(phrases, start=1):
        file_name = f"Phrase_{i}.wav"
        text_to_speech(phrase, file_name)
        print(f"Saved: {file_name}")

if __name__ == "__main__":
    main()
