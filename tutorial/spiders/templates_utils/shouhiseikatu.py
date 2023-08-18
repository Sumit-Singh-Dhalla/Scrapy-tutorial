from tutorial.utils.dump_data import (get_tag_text, get_table_data)


def crawl_shouhiseikatu(response):
    children = response.css('div#LayerContentsInner > *')
    item = {
        # "detail_1": get_tag_text(children[0], "h1"),
        # "detail_1_date": get_tag_text(children[1], "p"),
        # "detail_2": get_tag_text(children[2], "div"),
        get_tag_text(children[3], "h2"): get_table_data(children[4], "vertical-no-header"),
        # get_tag_text(children[6], "h2"): get_tag_text(children[7], "table tr td"),
        # get_tag_text(children[8], "h2"): get_tag_text(children[9], "p") + get_tag_text(children[10],
        #                                                                                "ol li",
        #                                                                                append_by="\n"),
        # get_tag_text(children[11], "h2"): get_table_data(children[12], "horizontal"),
        # get_tag_text(children[13], "h2"): get_tag_text(children[14], "ol li", append_by="\n"),
        # get_tag_text(children[15], "h2"): get_table_data(children[16], "horizontal"),
        # get_tag_text(children[17], "h3"): get_tag_text(children[18], "p") + "\n" + get_tag_text(children[19], "p"),
        # get_tag_text(children[20], "h2"): get_table_data(children[21], "horizontal-multi-header"),
        # get_tag_text(children[22], "h2"): get_tag_text(children[23], "ul li", append_by="\n"),
        # get_tag_text(children[24], "h2"): get_tag_text(children[25], "p") + get_tag_text(children[26],
        #                                                                                  "ul li",
        #                                                                                  append_by="\n"),
    }
    return item


