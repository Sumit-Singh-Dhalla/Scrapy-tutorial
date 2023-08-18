from tutorial.utils.dump_data import get_tag_text


def crawl_caa(response):
    _item = {}
    for section in response.css("section:has(p)"):
        heading = get_tag_text(section, "h2")
        detail = get_tag_text(section, "p")
        if heading:
            _item.update({heading: detail})
        else:
            _item.update({"open_text": detail})
    return _item
