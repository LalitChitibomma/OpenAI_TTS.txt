from openai import OpenAI
from gtts import gTTS
from pydub import AudioSegment
import os
import sys

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = "<Your-API-Key>"

print("Welcome to OpenAI_TTS.txt!")
    
# Check if the correct number of command-line arguments is provided
if len(sys.argv) < 3 or len(sys.argv) > 5:
    print("Usage: python main.py <text_file_path> <output_file_path> ~<model> ~<voice>")

else:
    # Extract command-line arguments
    text_file = sys.argv[1]
    output_file = sys.argv[2]
    if len(sys.argv) == 4:
        modl = sys.argv[3]
    else:
        modl = None
    if len(sys.argv) == 5:
        voic = sys.argv[4]
    else:
        voic = None

    if __name__ == "__main__":
        # Specify the path to your text file
        
        current_dir = os.getcwd()
        input_file_path = os.path.join(current_dir, text_file)
        print(input_file_path)

        # Read text from the file
        text = read_text_file(input_file_path)

        option = input(f"Total cost for {text_file} will be ~${round(len(text) * 0.015/1000, 2)}. Do you wish to continue? (y/n)\n")

        while option != "y":
            if option == 'n':
                print("Bye-bye :)")
                break
            else:
                option = input(f"Please use 'y' or 'n'\nTotal cost for {text_file} will be ~${round(len(text) * 0.015/1000, 2)}. Do you wish to continue? (y/n)\n")
        
        if option == 'y':
            directory = f"{text_file[:-4]}"
            path = os.path.join(current_dir, directory)
            try:
                os.mkdir(path)
            except:
                print("Path exists")

            max_length = 4096
            periods = text.split('.')
            size = 0
            phrase = ""
            chunks = []

            for chunk in periods:
                sentance = chunk + '.'

                if len(sentance) + size >= max_length:
                    chunks.append(phrase)
                    size = 0
                    phrase = ""

                phrase += sentance
                size += len(sentance)
            
            if not chunks:
                chunks.append(phrase)

            else:
                sentance = periods[-1]
                phrase += sentance
                chunks.append(phrase)

            # Generate audio using OpenAI text-to-speech
            try:
                client = OpenAI()
                audio_files = []
                
                for index, chunk in enumerate(chunks):
                    print(f"Now Creating Chunk {index+1}/{len(chunks)}")
                    file_name = f"speech_part_{index+1}.mp3"
                    speech_file_path = os.path.join(path, file_name)
                    response = client.audio.speech.create(
                        model=modl,
                        voice=voic,
                        input=chunk,
                    )

                    # Generate audio using gTTS
                    response.stream_to_file(speech_file_path)
                    audio_files.append(speech_file_path)

            except Exception as e:
                print(f"OpenAI API call failed: {e}")

            combined = AudioSegment.empty()
            for file in audio_files:
                audio = AudioSegment.from_mp3(file)
                combined += audio
            combined.export(output_file + ".mp3", format="mp3")