# Melodicorn

Raspberry PI based keyboard sound player.

On the occasion of my son's first birthday.

Code and sound files Open MIT licensed. Please use!

## To run

This was made for a Raspberry PI Zero with the [Adafruit Stereo Bonnet](https://www.adafruit.com/product/3412). Two rows of 11 keys wired up, rows and cols per source code.

Install the audio driver. 

Then depending on your speaker, you may wish to adjust the volume for the right balance of loudness vs distortion. 200 is perfect for my setup.

    sudo amixer set PCM 200   
    python melodicorn.py

or to run at startup add to /etc/rc.local 

    cd /home/pi/melodicorn && ./run-loop.sh &

After a few hours of running the sounds gets garbled. Not sure why, but for now there's a reset key combination, which kills the Python process. The run-loop.sh restarts it.
