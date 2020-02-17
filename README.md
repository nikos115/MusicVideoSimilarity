# Music Video Similarity
P2 Multimodal Information Processing and Analysis project - MSc in Data Science @ NCSR Demokritos <br>
Find the most similar song in database

## Steps:
#### 1. Compile a list of 1000 videos along with metadata attributes
~ Create a genre list <br>
~ Implement a script for:
- Downloading top 50 youtube videos per music genre
- Gathering metadata for each video on spotify
- Saving video metadata and file attributes in a Postgres database
 
#### 2. Extract audio and video features
- Split videos into 10sec segments
- Extract audio features using [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis)
- Extract video features using [Tyiannak](https://github.com/tyiannak/multimodalAnalysis) modules
- Save audio & video features in database
- Train NN autoencoder for encoding videos into a fixed length vector
- Train NN classifier on database instances for predicting new video genre
![composite nn model](model/composite.png?raw=true "composite autoencoder-classifier")

#### 3. Compute similarity graph for audio, visual and audio-visual feature representations
- Implement KNN on SQL evaluating distance weights along each feature
- Use Euclidian and Cosine similarity metrics

#### 4. Evaluate similarity in terms of metadata
- Classify the new video by the pre trained classifier, boost same genre videos on similarity

## Running the app
The app is built with Flask framework. A Postgres container serves the database, therefore [Docker](https://docs.docker.com/install/) and the [psycopg2](https://www.psycopg.org/docs/install.html) driver are required to be installed.
- Download and extract [database data]() into the project root directory.
- Install the project requirements:
```
$ pip3 install -r requirements.txt
```
- Run the app by sourcing run.sh
```
$ source ./run.sh
```
