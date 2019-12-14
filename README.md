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
- Split videos into segments using a 10s sliding window with 5s offset
- Extract audio features using pyAudioAnalysis
- Extract video features ...
- Save audio & video features in database
- Train NN classifiers with database instances for predicting new video metadata

#### 3. Compute similarity graph for audio, visual and audio-visual feature representations
- Implement KNN on SQL evaluating distance weights along each feature

#### 4. Evaluate similarity in terms of metadata
- Classify the new video by the pre trained classifiers

## Running the app
The app is built with Flask framework. A Postgres container serves the database, therefore Docker is required to be installed.
You can easily setup your environment and run the app by modifying and sourcing run.sh
```
$ source ./run.sh
```
