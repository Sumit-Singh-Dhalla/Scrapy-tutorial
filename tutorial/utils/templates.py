from tutorial.spiders.templates_utils import crawl_caa, crawl_shouhiseikatu


TEMPLATES = {
  "https://www.caa.go.jp/": crawl_caa,
  "https://www.shouhiseikatu.metro.tokyo.lg.jp/": crawl_shouhiseikatu
}
