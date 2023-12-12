# Bernard

Bernard is a Voice-Controlled Discord Music Bot designed for busy situations that require a banger soundtrack.
Bernard perpetually monitors the connected voice channel, processing incoming bytes on a per-user basis. 
When a user speaks, Bernard transcribes the audio using Google Speech Recognition and endeavors to identify and execute commands. 
Among its functionalities, Bernard can play audio, pause, resume, stop, and trigger predefined sounds associated with specific code words.

## Authors

- [@Delyanskiiii](https://www.github.com/Delyanskiiii)

## FAQ

#### How to use Bernard without commands?

To quickly get Bernard into the voice channel, mute and unmute. Then, simply say something as 'Bernard, play the Dr. Ford theme.'

#### How to make Bernard leave?

Bernard will automatically leave the voice channel when left alone. Alternatively, you can say 'That's enough, Bernard.'

## Roadmap

- Implement custom playlists per user.
- Integrate ChatGPT for enhanced interactions.

## Run Locally

1. Clone the project

    ```bash
    git clone https://github.com/Delyanskiiii/Bernard
    ```

2. Go to the project directory

    ```bash
    cd Bernard
    ```

3. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Go to the source directory

    ```bash
    cd bernard
    ```

5. Start the server

    ```bash
    python main.py
    ```

## Tech Stack

**Client:** Custom Pycord fork

**Speech Recognition:** Google Speech Recognition
