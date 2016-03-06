# facebook_pykov
Markov generator written in python, using Pykov and data from your own Facebook messages!

### Instructions:
1. Go to https://www.facebook.com/settings and request a copy of your facebook data (at the bottom).
2. Unpack the archive to a directory called 'facebook' in the project root.
3. Run facebookparser.py to save raw data by sender.
4. Run chaingenerator.py to build a chain file from one of the parsed data files.
5. Various pykov.Chain() methods can then be used to generate random strings text.

### Dependencies:
1. Pykov https://github.com/riccardoscalco/Pykov, and all of its dependencies.
2. BeautifulSoup
3. re
4. pickle
