# import xmltojson
import json
import pdb

from bs4 import BeautifulSoup
import html_to_json


def dump_file(response, file_name):
    output_json = html_to_json.convert(response.text)
    with open(file_name, "w") as file:
        json.dump(output_json, file, ensure_ascii=False)


def get_table_data(response, table_type):
    all_tr = response.css("table tr")
    data = []
    if table_type == "horizontal":
        for tr in all_tr[1:]:
            item = {get_tag_text(all_tr[0], f"th:nth-child({index})"): get_tag_text(tr, f"td:nth-child({index})")
                    for index in range(1, len(all_tr.css("th"))+1)}
            data.append(item)
        return data
    if table_type == "horizontal-multi-header":
        header_rows = response.css('table tr:has(th)')
        headers = get_headers(header_rows)
        for row in all_tr[len(header_rows):]:
            data.append({headers[index]: get_tag_text(row, f"td:nth-child({index+1})"
                                                      ) for index in range(0, len(headers))})

    elif table_type == "vertical-no-header":
        data.append({
            get_tag_text(tr, "th"): get_tag_text(tr, "td") for tr in all_tr
        })
    return data


def get_tag_text(response, tag_type, append_by=" "):
    return f"{append_by}".join(response.css(f"{tag_type} ::text").getall()
                               ).replace("\u3000", "").replace("\r\n\t\t\t", ""
                                                               ).replace("\xa0", "").strip()


def get_headers(header_rows):
    rs, data = {}, []
    for i in range(len(header_rows)-1):
        row = header_rows[i]
        all_th = row.css("th")
        next_data, next_cell_added = [], 0
        for index in range(len(all_th)):
            col_span = int(all_th[index].attrib.get('colspan', '0'))
            row_span = int(all_th[index].attrib.get('rowspan', '1'))
            text = get_tag_text(row, f"th:nth-child({index+1})")

            cell_cs = 0
            for j in range(next_cell_added, next_cell_added+col_span):
                if col_span > cell_cs:
                    next_cell_added += 1
                    cell = header_rows[i+1].css(f"th:nth-child({j+1})")
                    cell_cs += int(cell.attrib.get("colspan", "1"))
                    next_data.append(get_tag_text(header_rows[i+1], f"th:nth-child({j+1})"))
            if row_span > 1:
                next_data.append(text)
                rs.update({text: row_span-1})
            elif col_span == 0:
                next_data.append(text)

            if not data:
                continue
            temp_rs = {}
            for key, value in rs.items():
                new_value = value
                position_in_data = len(data) - data.index(key)
                if position_in_data == (len(all_th) - index) and value > 0:
                    next_data.append(key)
                    new_value -= 1
                temp_rs.update({key: new_value})
            rs = temp_rs.copy()
        data = next_data
    return [obj for obj in data if obj]
