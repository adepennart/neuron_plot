## About
This program is useful for ploting 2D representations of catmaid neurons, and reproducing these plots.

This program can be directly installed from github (green Code button, top right).

This program is fully run on the terminal.
## Installation
### Conda environment
First make sure conda is installed. If you do not have conda, refer to online resources on how to install conda.
https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

Once installed, we can make a conda environment.

```bash=
conda create --name pymaid
#activate
conda activate pymaid
```

Create a directory for pymaid.
```bash=
mkdir pymaid
cd pymaid
```

### Python version
The python version for running this script is python=3.6
```bash=
conda install python=3.6
```

### Dependencies
The script runs with pip\==21.3.1 and python-catmaid==2.0.4

Update your dependencies, if you do not already have the versions for these dependencies.

```bash=
pip3 install --upgrade pip==21.3.1 wheel==0.37.1 setuptools==59.6.0

pip3 install python-catmaid==2.0.4 -U
```

### Make environmental variables

The environmental variables are the login credentials required to access catmaid online. Which include, the catmaid server, and your API token (the API token replaces your username and password to the server). Your API token can be found following the instructions on this website:
https://catmaid.readthedocs.io/en/stable/api.html#api-token

There are two ways to access catmaid online. The deemed safer version will be covered here, for the other option refer to this link:
https://pymaid.readthedocs.io/en/latest/source/intro.html

Add your new environmental variables via the bash_profile file.

```bash=
nano ~/.bash_profile
```
When in nano, add the following lines to your code, with  respect to your account. 
```bash=
export CATMAID_SERVER='https://www.your.catmaid-server.org'
export CATMAID_API_TOKEN='your_token'
```
Don't forget to source.
```bash=
source ~/.bash_profile
```

The script should be all ready to run.

## Usage
### Input
The code can be run as follows
```bash=
    python plot_pymaid.py [-h] [-v] -i PROJECT_ID
                      (-j JSON | -n NEURON [NEURON ...]) [-J] [-a]
                      [-c COLOUR [COLOUR ...]] [-V VOLUME [VOLUME ...]]
                      [-C VOLUME_COLOUR [VOLUME_COLOUR ...]]
                      [-p PERSPECTIVE PERSPECTIVE PERSPECTIVE] [-o OUTPUT]
                      [-s]
```
The help page can be accessed with the -h or --help flag
```bash=
python plot_pymaid.py -h
python plot_pymaid.py --help
```
The program version can be accessed with the -v or --version flag
```bash=
python plot_pymaid.py -v
python plot_pymaid.py --version
```
There are two required arguments for running this program, PROJECT_ID and JSON or PROJECT_ID and NEURON. PROJECT_ID specifies which species stack you are looking for neurons in. JSON is a json file with neurons of interest and NEURON are neurons of interest directly typed out to the terminal.
```bash=
python plot_pymaid.py -i PROJECT_ID -j JSON
python plot_pymaid.py -i PROJECT_ID -n NEURON
```

The following arguments are optional.

JSON_COLOUR, when user-specified neuron colours are not wanted (only useable with JSON).
```bash=
python plot_pymaid.py -i PROJECT_ID -j JSON -J
```
ANNOTATION, when annotations are how you are looking for neurons as opposed to by name (only useable with NEURON).
```bash=
python plot_pymaid.py -i PROJECT_ID -n NEURON -a
```

VOLUME, when you want to depict volumes in your plot.
```bash=
python plot_pymaid.py -i PROJECT_ID -j JSON -V VOLUME
python plot_pymaid.py -i PROJECT_ID -n NEURON -V VOLUME
```
COLOUR and VOLUME_COLOUR, when you want to have a specific colour for the neurons and the volumes respectively (COLOUR, only useable with NEURON).
```bash=
python plot_pymaid.py -i PROJECT_ID -n NEURON -c COLOUR

python plot_pymaid.py -i PROJECT_ID -j JSON -V VOLUME -C VOLUME_COLOUR
python plot_pymaid.py -i PROJECT_ID -n NEURON -V VOLUME -C VOLUME_COLOUR
```                      
PERSPECTIVE, when you want a specific view of the neurons in your plot.
```bash=
python plot_pymaid.py -i PROJECT_ID -j JSON -p PERSPECTIVE
python plot_pymaid.py -i PROJECT_ID -n NEURON -p PERSPECTIVE
```
OUTPUT, a output plot will be created with the specified file name.
```bash=
python plot_pymaid.py -i PROJECT_ID -j JSON -o OUTPUT
python plot_pymaid.py -i PROJECT_ID -n NEURON -o OUTPUT
```
Finally, NO_SHOW, when you don't want your plot displayed to screen.
```bash=
python plot_pymaid.py -i PROJECT_ID -j JSON -s
python plot_pymaid.py -i PROJECT_ID -n NEURON -s
```

### Example inputs

If interested in all E-PG neurons in your project and example input could be the following. 
```bash=
python3 plot_pymaid.py -i 8 -n EPG 
```

If a json file has been produced from Catmaid with all your neurons of interest it could be used as follows.
```bash=
python3 plot_pymaid.py -i 8 -j example.json 
```

If the json file neuron colours are not to your liking, you can not use them.
```bash=
python3 plot_pymaid.py -i 8 -j example.json -J
```

Perhaps we are interested in seraching neurons by annotations.
```bash=
python3 plot_pymaid.py -i 11 -n EPG -a
```

Perhaps there are two type of neurons you are interested in.
```bash=
python3 plot_pymaid.py -i 8 -n EPG PEN
```
Distinguishing them with colour, might be useful.
```bash=
python3 plot_pymaid.py -i 8 -n EPG PEN -c 1,0,0 0,0,1
```

Why not a new perspective on the neurons.
```bash=
python3 plot_pymaid.py -i 8 -n EPG -p 6 -90 360
```

Could be interesting to visualize with a volume.
```bash=
python3 plot_pymaid.py -i 8 -n EPG -V EB
```

Why not two.
```bash=
python3 plot_pymaid.py -i 8 -n EPG -V EB PB
```
The colouring of the volumes are off, let's change it.
```bash=
python3 plot_pymaid.py -i 8 -n EPG -V EB PB -C 0,0,1,0.1 0,0,1,0.1
```

Taking into account all the options a final view could be created with this.
```bash=
python3 plot_pymaid.py -i 11 -n EPG PEN -a -V EB PB -p 7 300 310 -C 0,1,0,.2 0,1,0,.2
```

If content with this final view, why not save it to output and save the hastle of showing it on the screen.
```bash=
python3 plot_pymaid.py -i 11 -n EPG PEN -a -V EB PB -p 7 300 310 -C 0,1,0,.2 0,1,0,.2 -o satisfied -s
```
