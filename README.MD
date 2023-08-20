# Scrappy POC

### run using docker
    > sudo docker build -t my-scrapy-spider .
    > sudo docker run my-scrapy-spider

### deploy on zyte
    > pip install shub
    > shub login <your API Key>
    > shub deploy >your project ID>

#### Startswith query regex
    > {"link": {$regex: "<your_str>.*"}}
        eg: {"link": {$regex: "https://www.shouhiseikatu.metro.tokyo.lg.jp/.*"}}