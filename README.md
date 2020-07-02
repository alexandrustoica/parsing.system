# Flux Syntactic Analyzer

![](https://img.shields.io/github/workflow/status/alexandrustoica/fluxsa/Build)
![](https://img.shields.io/github/repo-size/alexandrustoica/fluxsa)


**fluxsa** is a syntactic analyzer for flux, a simple procedural programming language.

#### Build 

##### With Docker
```
$ docker build -t flux:new .
```

##### With Docker-Compose
```
$ docker-compose build flux
```

#### Run
```
$ docker run -v <absolute path to example.json>:/parsing/example.json -t flux:new python /parsing/main.py /parsing/example.json
```

#### Run Tests
```
$ docker-compose build flux-test; docker-compose run flux-test
```

