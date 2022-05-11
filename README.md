
first make sure conda is installed
#follow steps for installation

then create conda environment
```bash=
conda create --name pymaid
#activate
conda activate pymaid
```

create directory

```bash=
mkdir pymaid
cd pymaid
```


# installation of pymaid
 
installation of python3
#done online

installation of pip3

```bash=
python -m pip install --upgrade pip==22.0.4
```

install pymaid

```bash=
pip3 install python-catmaid
```

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
spyder 3.3.6 requires pyqtwebengine<5.13; python_version >= "3", which is not installed.
spyder 3.3.6 requires pyqt5<5.13; python_version >= "3", but you have pyqt5 5.15.6 which is incompatible.
Successfully installed PyQt5-5.15.6 PyQt5-Qt5-5.15.2 PyQt5-sip-12.10.1 cached-property-1.5.2 fonttools-4.32.0 freetype-py-2.2.0 fuzzywuzzy-0.18.0 h5py-3.6.0 hsluv-5.0.2 igraph-0.9.10 matplotlib-3.5.1 molesq-0.4.0 morphops-0.1.13 navis-1.2.1 ncollpyde-0.19.0 networkx-2.6.3 numpy-1.21.6 packaging-21.3 pandas-1.3.5 pint-0.18 plotly-5.7.0 pynrrd-0.4.2 pypng-0.0.21 python-catmaid-2.1.0 python-igraph-0.9.10 rdata-0.7 requests-futures-1.0.0 scikit-learn-1.0.2 scipy-1.7.3 seaborn-0.11.2 setuptools-62.1.0 skeletor-1.2.0 tenacity-8.0.1 texttable-1.6.4 threadpoolctl-3.1.0 tqdm-4.64.0 trimesh-3.10.8 typing-extensions-4.1.1 vispy-0.9.6 xarray-0.20.2


uses spyder
when back to base environment

```bash=
conda deactivate
conda update spyder
```
#did not work


```bash=
conda update --all
```

#having issues with spyder3
```bash=
/Users/lamarcki//opt/anaconda3/bin/spyder3 

/Users/lamarcki/opt/anaconda3/bin/pythonw: line 3: /Users/lamarcki/opt/anaconda3/python.app/Contents/MacOS/python: No such file or directory

```

```bash=
spyder3
```
in environment
PackagesNotFoundError: The following packages are missing from the target environment:
  - spyder3
out of environment
No such file or directory


```bash=

conda uninstall spyder
```

perhaps reinstall spyder if necessary



```bash=
conda activate pymaid
```

# retry
was getting an error so made a new environment

```bash=
conda create --name pymaid2
#activate
conda activate pymaid2
```

when step by step in the instrcutions 

```bash=
conda install python=3.6

pip3 install --upgrade pip==21.3.1 wheel==0.37.1 setuptools==59.6.0

pip3 install python-catmaid==2.0.4 -U
```

make environmental variables

there are two ways to access the catmaid online, I will explain the version that is deemed safer, but you can refer to the tutorial for the other version

environmental variables need to be made

add new environmental variables via the bash_profile file

```bash=
nano ~/.bash_profile
```

when in nano, add the following lines to your code, with your respect to your account. You can get the API token here(refere to website) or I will explain here (check). alternatively you may not need your username and password with AP_token.
```bash=
#instructions state CATMAID_SERVER_URL, but incorrect
export CATMAID_SERVER='https://www.your.catmaid-server.org'
export CATMAID_API_TOKEN='you_token'
#export CATMAID_HTTP_USER='your_username'
#export CATMAID_HTTP_PASSWORD='your_password'
```
(CHeck) different way to display this

don't forget to source
```bash=
source ~/.bash_profile
```

then, it's time to run script
```bash=
python3 test_pymaid.py
```
