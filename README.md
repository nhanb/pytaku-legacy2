# Pytaku [![Build Status](https://travis-ci.org/nhanb/pytaku.png)](https://travis-ci.org/nhanb/pytaku)

Manga fetcher for otaku on the go

[to be updated]

## Development environment setup

Make sure you have the follow environment variables set up:

- `$GAE_PATH`: path to GAE python SDK on your machine, necessary for the test
  suite. If this envar is not available then the test suite will go for
  `~/google_appengine` by default.
- `$PYTHONPATH`: this should include the GAE path and root project path to
  help your code completer (might be unnessary for smart IDEs, but it seems
  like vim's YouCompleteMe python support isn't there yet - or maybe I'm just
  too dumb to find the right config variable, whatever) 
