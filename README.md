# DTW TextGrid alignment

This code uses the [Dynamic Time Warping (DTW)](https://github.com/pierre-rouanet/dtw) and the [librosa](https://github.com/librosa/librosa) music and audio analysis to time align two [Praat](https://github.com/praat/praat) `TextGrid` files using the [TextGrid tools (tgt)](https://github.com/hbuschme/TextGridTools) module. The code was written following the example code on [Using DTW to compare sounds](https://github.com/pierre-rouanet/dtw/blob/master/examples/MFCC%20%2B%20DTW.ipynb).

The code can be useful to time align annotations of multiple recordings of the same utterances, preferably from the same speaker, but possibly from different speakers.

# Use

The code is split up in [Spyder](https://github.com/spyder-ide) cells which can be executed one at a time. All the parameters are set in the second cell and their names are self-explanatory.

# Acknowledgement

The code was written within the [ProsoDeep](https://gerazov.github.io/prosodeep/) project, which has received funding from the European Union’s Horizon 2020 research and innovation programme under the [Marie Skłodowska-Curie Actions (MSCA)](http://ec.europa.eu/research/mariecurieactions/) grant agreement No 745802: “ProsoDeep: Deep understanding and modelling of the hierarchical structure of Prosody”.
