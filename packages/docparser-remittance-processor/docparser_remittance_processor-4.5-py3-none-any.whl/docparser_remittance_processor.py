#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
import re
import requests

from datetime import date, timedelta
from dataclasses import dataclass, field
from typing import List
from pathlib import Path

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from money2float import money

pd.options.display.float_format = "{:,.2f}".format


# In[3]:


def get_day(days_back):
    if days_back > 0:
        day = (date.today() - timedelta(days_back)).isoformat()
    else:
        day = date.today().isoformat()
    return day


# In[5]:


def get_content(download_url, auth_key):
    res = requests.get(download_url, auth=(auth_key, ""), timeout=5)
    try:
        content = res.json()
    except:
        content = {}
    return content


# In[7]:


def download_pdf(filename, url):
    response = requests.get(url)
    filename.write_bytes(response.content)


# In[8]:


def make_text_file_ready(text, strings_to_delete):
    try:
        text = re.sub("[^A-Za-z0-9_ ]+", "", text).lower()
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


# In[10]:


def make_filename(header, remittance, strings_to_delete):
    extension = Path(remittance["file_name"]).suffix
    insured_shortname = make_text_file_ready(
        header["insurer_short_name"], strings_to_delete
    )
    broker = make_text_file_ready(header.get("broker", ""), strings_to_delete)
    remittance_date = make_text_file_ready(
        remittance.get("remittance_date", "missing"), strings_to_delete
    )
    filename = make_text_file_ready(remittance["remote_id"], strings_to_delete).strip()
    new_filename = "_".join(
        [insured_shortname, broker, remittance_date, filename, extension]
    )
    return new_filename.replace("_.", ".")


# In[11]:


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
    header["original_filename"] = remittance.get("file_name", "")
    header["full_text"] = remittance.get("full_text", "")
    return header


# ## Parse data out of text
#
# The following code takes a block of structured text from the PDF and extracts data elements.
#
# Helper applications are find_numbers and find_dates

# In[16]:


def split_text(text):
    lines = text.split("^^^")
    lines = [line.split() for line in lines if line]
    return lines


# In[17]:


def find_objects(lines, object_type):
    return_lines = []
    for line in lines:
        return_line = []
        for word in line:
            if object_type == "dates":
                try:
                    if len(word) > 5:
                        raw_date = parse(word, dayfirst=True)
                        formatted_date = raw_date.strftime(format="%Y-%m-%d")
                        elapsed_years = relativedelta(raw_date, date.today()).years
                        if elapsed_years > -10:
                            return_line.append(formatted_date)
                except:
                    pass
            elif object_type == "numbers":
                r1 = re.match(r"[\$0-9\.,]+", word)
                try:
                    return_line.append(r1.group(0))
                except:
                    pass
        return_lines.append(return_line)
    return return_lines


# In[20]:


def build_row(text, doc_format):
    lines = split_text(text)
    dates = find_objects(lines, "dates")
    numbers = find_objects(lines, "numbers")
    try:
        if doc_format == "wuf":
            response = {"insured_name": " ".join(lines[0][:])}

        if doc_format == "ins_set_statement":
            response = {
                "policy_number": lines[0][-1],
                "type": "",
                "effective_date": dates[1][0],
                "invoice_number": lines[1][3],
                "insured_name": " ".join(lines[0][2:-2]),
            }

        if doc_format == "brokerplus":
            insured_name = f"{' '.join(lines[0][1:-3])} {' '.join(lines[1][:])})"
            response = {
                "policy_number": lines[0][-2],
                "type": lines[0][-3],
                "effective_date": dates[0][-1],
                "invoice_number": lines[0][0],
                "insured_name": insured_name,
            }

        if doc_format == "aub_group":
            insured_name = f"{' '.join(lines[1][2:-2])} ({lines[0][3]})"
            response = {
                "policy_number": lines[0][-1],
                "type": lines[1][-1],
                "effective_date": dates[0][0],
                "invoice_number": lines[1][-2],
                "insured_name": insured_name,
            }

        if doc_format == "macquarie":
            response = {
                "policy_number": lines[0][0],
                "type": lines[0][1],
                "effective_date": dates[0][0],
                "invoice_number": lines[0][-1],
                "insured_name": " ".join(lines[1][:-1]),
            }

        if doc_format == "portrait":
            response = {
                "policy_number": lines[0][-3],
                "type": lines[0][-1],
                "effective_date": dates[0][0],
                "invoice_number": numbers[1][0],
                "insured_name": " ".join(lines[0][:-3]),
                "premium_inc_commission_inc_gst": numbers[2][0],
                "broker_commission": numbers[2][1],
                "gst_broker_commission": numbers[2][2],
            }
    except:
        print("Failed to build row")
        response = {}
    return response


# In[68]:


def determine_sign(target):
    if "CR" in str(target) or "-" in str(target) or "(" in str(target):
        try:
            target = target.strip("-")
            target = target.strip("CR")
            target = target.strip("()")
        except:
            pass
        target = money(target) * -1
    return money(target)


# In[26]:


def build_fee_group_list(row):
    fee_group = row["fee_group"].replace(" 3 ", " B ")
    fee_group = fee_group.replace(" ", "")
    fee_group = fee_group.replace(",", "")
    fee_group = fee_group.replace("$", "")
    fee_group = fee_group.replace("CR", "-")
    letters_regex = re.compile("[A-Z]")
    numbers_regex = re.compile("[0-9\.\-]+")
    letters = letters_regex.findall(fee_group)
    numbers = numbers_regex.findall(fee_group)
    if len(letters) == len(numbers) - 1:
        letters.insert(0, "P")
    return list(zip(letters, numbers))


def update_broker_commission_acronym(fee_group_list):
    new_list = []
    commission = 0
    for item in fee_group_list:
        if item[0] == "B":
            commission = money(item[1])
    for item in fee_group_list:
        commission_gst_calc = determine_sign(item[1]) * 10
        if item[0] == "G" and (commission - 1) < commission_gst_calc < (commission + 1):
            new_list.append(("K", item[1]))
        else:
            new_list.append((item[0], item[1]))
    return new_list


def map_fee_group_to_fields(row, fee_group_list, fee_mapping):
    fees_dict = {}
    for item in fee_group_list:
        acronym = item[0]
        row[fee_mapping[item[0]]] = item[1]
    return row


# In[28]:


def convert_fee_group(rows, fee_mapping):
    return_rows = []
    fee_group_list = []
    for row in rows:
        fee_group_list = build_fee_group_list(row)
        fee_group_list = update_broker_commission_acronym(fee_group_list)
        row = map_fee_group_to_fields(row, fee_group_list, fee_mapping)
        return_rows.append(row)
    return return_rows


# In[29]:


def save_test_file(remittance, tag):
    (Path.cwd() / "test_data" / f"{tag}.json").write_text(
        json.dumps(remittance, indent=4)
    )


# In[30]:


def process_remittance(header, rows, return_columns):
    transformed_rows = []
    add = 0
    subtract = 0
    for row in rows:
        policy_data = row.get("policy_data", False)
        if policy_data:
            row_builder = build_row(policy_data, header["doc_format"])
            if row_builder:
                for k, v in row_builder.items():
                    row[k] = v
        final = {**header, **row}
        transformed_rows.append(final)
    df = pd.DataFrame(transformed_rows)
    columns = [x for x in return_columns if x in df.columns]
    df = df[columns]
    return df


# In[31]:


def calculate_columns(df, columns, money_columns):
    all_money_columns = [x for x in money_columns["all"] if x in df.columns]
    add_columns = [x for x in money_columns["add"] if x in df.columns]
    subtract_columns = [x for x in money_columns["subtract"] if x in df.columns]
    for column in all_money_columns:
        df[column] = df[column].apply(lambda x: determine_sign(x))
    df["calculated_remittance_detail"] = (
        df[add_columns].sum().sum() - df[subtract_columns].sum().sum()
    )
    df["calculated_remittance_total"] = df["line_net"].sum()
    df["total_difference"] = df["remittance_total"] - df["calculated_remittance_total"]
    return_columns = [x for x in columns if x in df.columns]
    return df[return_columns]


# In[67]:


def convert_section_totals(df, remittance):
    try:
        section_totals_df = pd.DataFrame(remittance["section_totals"], index=[0])
        df["remittance_total"] = (
            section_totals_df["total"].apply(lambda x: determine_sign(x)).sum()
        )
    except:
        section_totals_df = pd.DataFrame.from_dict(remittance["section_totals"])
        try:
            df["remittance_total"] = (
                section_totals_df["total"].apply(lambda x: determine_sign(x)).sum()
            )
        except:
            df["remittance_total"] = 0
    return df["remittance_total"]


# In[35]:


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


# In[36]:


def make_hyperlink(folder, value):
    url = f'=HYPERLINK(".\\{folder}\\{value}", "PDF")'
    return url


# In[37]:


def create_mapping(target, cp):
    rows = pd.read_excel(cp / "company_mapping.xlsx", sheet_name=target)
    rows.to_dict(orient="records")
    mapping = {}
    for row in rows.values:
        mapping[row[0]] = row[1]
    return mapping


# In[45]:


def replace_blanks(field, mapping, remittance):
    if field == None:
        for item in mapping.keys():
            if item.lower() in remittance["full_text"].lower():
                return item
    else:
        return field


# In[81]:


def normalise_header(
    header, remittance, strings_to_delete, insurer_short_name_mapping, broker_mapping
):
    header["insurer_short_name"] = insurer_short_name_mapping.get(
        header["insurer_short_name"], header["insurer_short_name"]
    )
    header["broker"] = broker_mapping.get(header["broker"], header["broker"])
    header["broker"] = replace_blanks(header["broker"], broker_mapping, remittance)
    header["new_filename"] = make_filename(header, test_remittance, strings_to_delete)
    header["hyperlink"] = make_hyperlink("source_documents", header["new_filename"])
    return header


# In[73]:


def create_files_grouped_by_column(df, column):
    gb = df.groupby(column)
    [gb.get_group(x) for x in gb.groups]
    return gb


# Used to group by insurer_short_name


# In[74]:


def save_daily_files(all_dfs):
    groups = create_files_grouped_by_column(all_dfs, "insurer_short_name")
    for group in groups:
        display(group[0])
        excel_filename = (op / group[0]).with_suffix(".xlsx")
        group[1].to_excel(excel_filename, index=False)
        display(group[1])


# In[ ]:


# In[ ]:


# In[ ]:
