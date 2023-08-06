#!/usr/bin/env python
# coding: utf-8

# # Remittance processor
#
# This application reads a list of remittances from Docparser and creates a dataframe saved as an Excel file.

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
import semi_structured_text_extractor as sste
import split_alphanumeric as sa

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
    filename = Path(remittance["file_name"]).stem
    filename = make_text_file_ready(filename, strings_to_delete)
    try:
        filename = filename.rsplit("_")[1]
    except:
        pass

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


# In[17]:


def build_row(text, doc_format):
    lines = sste.split_text(text, "^^^")
    dates = sste.find_objects(lines, "dates")
    numbers = sste.find_objects(lines, "numbers")
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


# In[20]:


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


# In[24]:


def convert_fee_group(rows, fee_mapping):
    return_rows = []
    for row in rows:
        fee_group_list = sa.build_fee_group_list(row["fee_group"])
        mapped_group = sa.map_fee_group_to_fields(fee_group_list, fee_mapping)
        for name, value in mapped_group.items():
            row[name] = value
        return_rows.append(row)
    return return_rows


# In[26]:


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


# In[27]:


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


# In[29]:


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


# In[30]:


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


# In[31]:


def make_hyperlink(folder, value):
    url = f'=HYPERLINK(".\\{folder}\\{value}", "PDF")'
    return url


# In[32]:


def create_mapping(target, cp):
    rows = pd.read_excel(cp / "company_mapping.xlsx", sheet_name=target)
    rows.to_dict(orient="records")
    mapping = {}
    for row in rows.values:
        mapping[row[0]] = row[1]
    return mapping


# In[34]:


def replace_blanks(field, mapping, remittance):
    if field == None:
        for item in mapping.keys():
            if item.lower() in remittance["full_text"].lower():
                print(item)
                return item
    else:
        return field


# In[36]:


def normalise_header(
    header, remittance, strings_to_delete, insurer_short_name_mapping, broker_mapping
):
    header["insurer_short_name"] = insurer_short_name_mapping.get(
        header["insurer_short_name"], header["insurer_short_name"]
    )
    header["broker"] = broker_mapping.get(header["broker"], header["broker"])
    header["broker"] = replace_blanks(header["broker"], broker_mapping, remittance)
    header["new_filename"] = make_filename(header, remittance, strings_to_delete)
    return header
