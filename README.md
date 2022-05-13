
## conda environment
first make sure conda is installed. If you do not have conda, refer to online resources on how to install conda.

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

## installation of pymaid
 
All the following steps for installation can also be found at: https://pymaid.readthedocs.io/en/latest/source/install.html

Install python3, pip and pymaid. 

```bash=
conda install python=3.6

pip3 install --upgrade pip==21.3.1 wheel==0.37.1 setuptools==59.6.0

pip3 install python-catmaid==2.0.4 -U
```

## make environmental variables

The environmental variables are the login credentials required to access catmaid online. Which include, the catmaid server, and your API token which replaces your username and password to the server. Your API token can be gotten following the instructions at this website:
https://catmaid.readthedocs.io/en/stable/api.html#api-token

There are two ways to access catmaid online. The deemed safer version will be covered here, for the other option refere to this link:
https://pymaid.readthedocs.io/en/latest/source/intro.html

Add new environmental variables via the bash_profile file.

```bash=
nano ~/.bash_profile
```
When in nano, add the following lines to your code, with  respect to your account. 
```bash=
#instructions state CATMAID_SERVER_URL, but incorrect
export CATMAID_SERVER='https://www.your.catmaid-server.org'
export CATMAID_API_TOKEN='your_token'
```
Don't forget to source.
```bash=
source ~/.bash_profile
```

It's time to run the script.
```bash=
python3 test_pymaid.py
```


## visualization

for the perfect view
```bash=
python3 plot_pymaid.py -i 11 -n EPG PEN -a -V EB PB -p 7 300 310 -C 0,1,0,.2 0,1,0,.2
```
usage
```bash=
python plot_pymaid.py [-h] [-v] -i PROJECT_ID
                      (-j JSON | -n NEURON [NEURON ...]) [-a]
                      [-V VOLUME [VOLUME ...]] [-c COLOUR [COLOUR ...]]
                      [-C VOLUME_COLOUR [VOLUME_COLOUR ...]]
                      [-p PERSPECTIVE PERSPECTIVE PERSPECTIVE] [-o OUTPUT]
```

