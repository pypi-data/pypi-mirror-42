#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
import re
import requests

from datetime import date, timedelta
from pathlib import Path

from money2float import money


# In[4]:


def get_day(days_back):
    if days_back > 0:
        day = (date.today() - timedelta(days_back)).isoformat()
    else:
        day = date.today().isoformat()
    return day


# In[6]:


def get_content(download_url, auth_key):
    res = requests.get(download_url, auth=(auth_key, ""), timeout=5)
    try:
        content = res.json()
    except:
        content = {}
    return content


# In[213]:


def download_pdf(filename, url):
    response = requests.get(url)
    filename.write_bytes(response.content)


# In[9]:


def make_text_file_ready(text, strings_to_delete):
    try:
        text = re.sub("[^A-Za-z0-9\._ ]+", "", text).lower()
        text_list = text.split()
        good_text = []
        already_got_it = []
        for item in text_list:
            if item not in strings_to_delete and item not in already_got_it:
                good_text.append(item)
                already_got_it.append(item)
        text = "_".join(good_text)
    except:
        text = "missing_value"
    return text


# In[11]:


def make_filename(header, remittance, strings_to_delete):
    insured_shortname = make_text_file_ready(
        header["insurer_short_name"], strings_to_delete
    )
    broker = make_text_file_ready(remittance.get("broker", ""), strings_to_delete)
    remittance_date = make_text_file_ready(
        remittance.get("remittance_date", "missing"), strings_to_delete
    )
    filename = make_text_file_ready(remittance["remote_id"], strings_to_delete)
    return "_".join([insured_shortname, broker, remittance_date, filename])


# In[47]:


def make_header(remittance, strings_to_delete):
    header = {}
    try:
        header["insurer"] = " ".join(remittance.get("insurer").split())
    except:
        header["insurer"] = ""
    header["insurer_short_name"] = make_text_file_ready(
        header["insurer"], strings_to_delete
    )
    header["broker"] = remittance.get("broker", "")
    header["broker_abn"] = remittance.get("broker_abn", "")
    header["remittance_date"] = remittance.get("remittance_date", "")
    header["remittance_total"] = money(remittance.get("remittance_total", ""))
    header["doc_format"] = remittance.get("tagger", "")
    header["new_filename"] = make_filename(header, remittance, strings_to_delete)
    header["original_filename"] = remittance.get("file_name", "")
    header["full_text"] = remittance.get("full_text", "")
    return header


# In[256]:


def split_text_to_lines(text):
    text = text.replace("\n", "")
    lines = text.split("^^^")
    lines = [line.split() for line in lines if line]
    return lines


# In[263]:


def remove_rows(lines, position, string_to_find):
    lines_01 = []
    for line in lines:
        print(string_to_find.lower(), line[position].lower())
        if string_to_find.lower() not in line[position].lower():
            lines_01.append(line)
    return lines_01


# In[266]:


def set_header_field(lines, header, field_name, line_no, position):
    header[field_name] = lines[line_no, position]
    return header


# In[53]:


def change_sign(target):
    if "CR" in str(target) or "-" in str(target):
        try:
            target = target.strip("-")
            target = target.strip("CR")
        except:
            pass
        target = money(target) * -1
    return money(target)


# In[55]:


def validate_remittance(df, money_columns_add, money_columns_subtract, header):
    add_columns = [x for x in money_columns_add if x in df.columns]
    add = money(df[add_columns].sum().sum())
    subtract_columns = [x for x in money_columns_subtract if x in df.columns]
    subtract = money(df[subtract_columns].sum().sum())
    add = money(add)
    subtract = money(subtract)
    detail_total = add - subtract
    detail_total = money(line_total)
    remittance_total = money(header["remittance_total"])
    remittance_line_total = money(df["line_net"].sum())
    difference = remittance_total - remittance_line_total
    df["detail_difference"] = remittance_total - line_total
    df["total_difference"] = money(difference)
    return df


# In[117]:


def process_fee_group(row, fee_mapping):
    fee_group = row["fee_group"].replace(" 3 ", " B ")
    fee_group = fee_group.replace(" ", "")
    fee_group = fee_group.replace(",", "")
    fee_group = fee_group.replace("$", "")
    if fee_group[0].isdigit():
        fee_group = f"P{fee_group}"
    letters_regex = re.compile("[A-Z]")
    numbers_regex = re.compile("[0-9\.]+")
    letters = letters_regex.findall(fee_group)
    numbers = numbers_regex.findall(fee_group)
    if len(letters) != len(numbers):
        print("Problem extracting fees from fee_group")
    else:
        fees_dict = dict(zip(letters, numbers))
        for acronym, value in fees_dict.items():
            value = change_sign(value)
            row[fee_mapping.get(acronym, "missing")] = value
    row["line_net"] = change_sign(row["line_net"])
    return row


# In[120]:


def convert_aub_group_rows(rows, fee_mapping):
    return_rows = []
    for row in rows:
        process_fee_group(row, fee_mapping)
        return_rows.append(row)
    return return_rows


# In[209]:


def process_remittance(header, rows, return_columns, money_columns):
    transformed_rows = []
    add = 0
    subtract = 0
    for row in rows:
        for item, value in row.items():
            if item in money_columns["all"]:
                try:
                    row[item] = money(value)
                    if item in money_columns["add"]:
                        add += money(value)
                    elif item in money_columns["subtract"]:
                        subtract += money(value)
                except:
                    pass
        row["add_total"] = money(add)
        row["subtract_total"] = money(subtract)
        final = {**header, **row}
        transformed_rows.append(final)
    df = pd.DataFrame(transformed_rows)
    df["calculated_line_net"] = df["add_total"] - df["subtract_total"]
    df["calculated_remittance_total"] = df["line_net"].sum()
    columns = [x for x in return_columns if x in df.columns]
    df = df[columns]
    return df


# In[71]:


def save_remittance_output(folder, remittance, df, header, file_list):
    pdf_filename = Path.cwd() / folder / header["file_name"]
    json_remittance_filename = (Path.cwd() / folder / header["file_name"]).with_suffix(
        ".json"
    )
    csv_filename = (Path.cwd() / folder / header["file_name"]).with_suffix(".csv")
    if "pdf" in file_list:
        download_pdf(pdf_filename, remittance["media_link"])
    if "json" in file_list:
        json_remittance_filename.write_text(json.dumps(remittance, indent=4))
    if "csv" in file_list:
        df.to_csv(csv_filename, index=False)


# In[72]:


def create_files_grouped_by_column(df, column):
    gb = df.groupby(column)
    [gb.get_group(x) for x in gb.groups]
    return gb


# Used to group by insurer_short_name


# In[73]:


def save_daily_files(all_dfs):
    groups = create_files_grouped_by_insurer(all_dfs)
    for group in groups:
        display(group[0])
        excel_filename = (op / group[0]).with_suffix(".xlsx")
        group[1].to_excel(excel_filename, index=False)
        display(group[1])


# In[74]:


def make_hyperlink(folder, value):
    url = f'=HYPERLINK(".\\{folder}\\{value}", "PDF")'
    return url


# In[75]:


def create_mapping(target, cp):
    rows = pd.read_excel(cp / "company_mapping.xlsx", sheet_name=target)
    rows.to_dict(orient="records")
    mapping = {}
    for row in rows.values:
        mapping[row[0]] = row[1]
    return mapping


# In[77]:


def replace_blanks(row, mapping, target):
    if row[target] == None:
        for item in mapping.keys():
            if item in row["full_text"]:
                return item
    else:
        return row[target]


# In[ ]:


# In[ ]:
