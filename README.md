# clarefy-app
Flask application to help clarify key concepts in scientific papers

### Motivation

We want to help researchers and students understand academic papers and articles more easily when they are reading outside their comfort zone/area of expertise. The prospect of slogging through a publication full of jargon and references to a body of literature the reader hasn't heard of can be extremely daunting, which can discourage people from pushing the limits of their understanding. 

The reality: the user supplies an arXiv address to a paper, the app reads in the title and abstract, uses the Microsoft cognitive services API to extract the key concepts, then provides a ranked list of short definitions and Wikipedia links for the reader.

The dream: with more time, we would finish off our reference-parsing code, which would access the content of the paper's citations in addition to the paper itself. We would then use this to compare with the important concepts of the primary paper and give ranked suggestions for background reading. Ideally, instead of a long list of citations in no useful order in the paper, the app could provide the top few papers which are seminal works on the area and most relevant to understanding the paper at hand.

The [futureWork](futureWork) directory shows what we were working on at submission: code to read and sort references.

### Requirements

Python 2.7 with the following libraries installed:
```
flask
re
urllib
urllib2
feedparser
wikipedia
httplib
base64
json
```

### Running

After cloning this repository, `cd` to the directory containing [`app.y`](app.py) and do

```bash
python app.py
```
to start the Flask app.

Navigate to http://127.0.0.1:5000/ in a web browser to use claREFy. The search bar can accept any string containing an arXiv code, so  it should be happy with input in any of these formats:

https://arxiv.org/abs/1303.7367

https://arxiv.org/pdf/1609.01668v1.pdf

random1207.7214string

**Note:** typing enter won't submit the request - users must click the button on screen.
