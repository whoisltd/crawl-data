# Crawler example

This is a simple crawler example using [Scrapy](https://scrapy.org/).

## Slide

- [Slide](https://docs.google.com/presentation/d/153_9S5w43Ixn9_jn5p2zyVRLGUHEt6ItVWb_WpA9dms/edit?usp=sharing)

## Resource learn Scrapy

- [Scrapy Basic Tutorial](https://www.pluralsight.com/guides/implementing-web-scraping-with-scrapy)

## How to run

1. Install [Scrapy](https://scrapy.org/).
    
    ```
    pip install scrapy
    ```

2. Create a new Scrapy project using the command:

    ```
    scrapy startproject crawler_example
    ```

3. Create spider using the command:

    ```
    cd crawler_example
    scrapy genspider spider_name example.com
    ```

4. Run the spider using the command:

    ```
    scrapy crawl spider_name
    ```

