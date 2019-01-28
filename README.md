# README

### Set-up
In `models` directory download and unpack pretrained models with:
```console
wget https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz
gunzip GoogleNews-vectors-negative300.bin
curl -L -o content_module "https://drive.google.com/uc?export=download&id=1TP5FeupC0VeoCyNymzHITg9WHh4GfDDy"
curl -L -o best_model.h5 "https://drive.google.com/uc?export=download&id=1hCn43PzyXf9K1arcDPRBrYqN4RzNwbZK"
```
The word2vec model should be unziped in `models` dir as `GoogleNews-vectors-negative300.bin`

In `Egrader` directory download and unpack resources with:
```console
curl -L -o resources.zip "https://drive.google.com/uc?export=download&id=10ymcXU3Qzhkgynrm3USfy66EmJWTRbt1" && unzip resources.zip && rm resources.zip
```

### Running
Run the backend (might take some time to load w2v model and keras model), and keep it running with:
```console
python3 egrader.py
```

Download dependency modules with npm from the `frontend` folder with:
```
npm install
```

Run the frontend with:
```
npm run serve
```

Now open the IP in your browser given by the last command

### Re-training
Data available [here](https://drive.google.com/file/d/11icP5B2_1QanCrsZVIiaJPeq-bMGgKru/view?usp=sharing).
