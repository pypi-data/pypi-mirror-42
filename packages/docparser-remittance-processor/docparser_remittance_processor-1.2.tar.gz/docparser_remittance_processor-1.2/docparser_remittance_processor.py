#!/usr/bin/env python
# coding: utf-8

# In[6]:


import json
import pandas as pd
import re
import requests

from datetime import date, timedelta
from pathlib import Path

from money2float import money


# In[90]:


def get_day(days_back):
    if days_back > 0:
        day = (date.today() - timedelta(days_back)).isoformat()
    else:
        day = date.today().isoformat()
    return day


# In[9]:


def get_content(download_url, auth_key):
    res = requests.get(download_url, auth=(auth_key, ""), timeout=5)
    try:
        content = res.json()
    except:
        content = {}
    return content


# In[10]:


def download_pdf(filename, url):
    response = requests.get(url)
    filename.write_bytes(response.content)


# In[11]:


def make_text_file_ready(text):
    strings_to_delete = [
        "ltd",
        "pty",
        "limited",
        "and",
        "pl",
        "tas",
        "ar",
        "as",
        "auth",
        "rep",
        "of",
        "trading",
        "austagencies",
    ]
    try:
        text = re.sub("[^A-Za-z0-9\. ]+", "", text).lower()
        text_list = text.split()
        good_text = []
        for item in text_list:
            if item not in strings_to_delete:
                good_text.append(item)
                strings_to_delete.append(item)
        text = "_".join(good_text)
    except:
        text = "missing_value"
    return text


# In[13]:


def make_filename(header, remittance):
    insured_shortname = make_text_file_ready(header["insurer_short_name"])
    broker = make_text_file_ready(remittance.get("broker", ""))
    remittance_date = make_text_file_ready(remittance.get("remittance_date", "missing"))
    filename = make_text_file_ready(remittance["remote_id"])
    return "_".join([insured_shortname, broker, remittance_date, filename])


# In[14]:


def make_header(remittance):
    header = {}
    try:
        header["insurer"] = " ".join(remittance.get("insurer").split())
    except:
        header["insurer"] = ""
    header["insurer_short_name"] = make_text_file_ready(header["insurer"])
    header["broker"] = remittance.get("broker", "")
    header["broker_abn"] = remittance.get("broker_abn", "")
    header["remittance_date"] = remittance.get("remittance_date", "")
    header["remittance_total"] = remittance.get("remittance_total", "")
    header["doc_format"] = remittance.get("tagger", "")
    header["new_filename"] = make_filename(header, remittance)
    header["original_filename"] = remittance.get("file_name", "")
    header["full_text"] = remittance.get("full_text", "")
    return header


# In[15]:


all_columns = [
    "insurer",
    "insurer_short_name",
    "broker",
    "remittance_date",
    "doc_format",
    "branch",
    "broker_abn",
    "policy_number",
    "insured_name",
    "risk_type",
    "type",
    "broker_reference",
    "invoice_number",
    "effective_date",
    "gross_premium_ex_commission",
    "net_premium_ex_commission",
    "premium_ex_gst",
    "premium_inc_commission_inc_gst",
    "underwriting_fee",
    "gst_premium",
    "gst_premium_ex_commission",
    "levies",
    "levies_01",
    "levies_02",
    "levies_03",
    "broker_commission",
    "gst_broker_commission",
    "earlier_paid",
    "line_net",
    "remittance_total",
    "difference",
    "new_filename",
    "original_filename",
    "hyperlink",
    "full_text",
]


# In[16]:


common_columns = [
    "insurer_short_name",
    "remittance_date",
    "insurer",
    "broker",
    "insured_name",
    "broker_reference",
    "policy_number",
    "type",
    "effective_date",
    "invoice_number",
    "line_net",
    "remittance_total",
    "doc_format",
    "new_filename",
    "original_filename",
]


# In[17]:


money_columns_add = [
    "premium_ex_gst",
    "levies",
    "gst_premium",
    "premium_inc_commission_inc_gst",
    "gross_premium_ex_commission",
    "underwriting_fee",
    "levies_01",
    "levies_02",
    "levies_03",
]
money_columns_subtract = ["broker_commission", "gst_broker_commission", "earlier_paid"]
money_columns_total = ["line_net", "remittance_total"]
money_columns_all = [*money_columns_add, *money_columns_subtract, *money_columns_total]
money_columns_all


# In[86]:


def change_sign(target):
    if "CR" in str(target) or "-" in str(target):
        try:
            target = target.strip("-")
            target = target.strip("CR")
        except:
            pass
        target = money(target) * -1
    return money(target)


def convert_money_columns(df, columns):
    for column in columns:
        if column in df.columns:
            df[column] = df[column].apply(lambda x: money(x))
    return df


# In[88]:


def validate_remittance(df, money_columns_add, money_columns_subtract, header):
    add_columns = [x for x in money_columns_add if x in df.columns]
    add = money(df[add_columns].sum().sum())
    #     display(df[add_columns])
    subtract_columns = [x for x in money_columns_subtract if x in df.columns]
    subtract = money(df[subtract_columns].sum().sum())
    #     display(df[subtract_columns])
    add = money(add)
    subtract = money(subtract)
    line_total = add - subtract
    line_total = money(line_total)
    remittance_total = money(header["remittance_total"])
    remittance_line_total = money(df["line_net"].sum())
    difference = remittance_total - remittance_line_total
    detail_difference = remittance_total - line_total
    difference = money(difference)
    print(f"{add} - {subtract} = {line_total}")
    print(f"Remittance total: {remittance_total}")
    print(f"Difference: {difference}")
    print()
    return difference, detail_difference


# In[67]:


def process_fee_group(row, fee_mapping):
    fee_group = row["fee_group"].replace(" 3 ", " B ")
    fee_group = fee_group.replace(" ", "")
    fee_group = fee_group.replace(",", "")
    fee_group = fee_group.replace("$", "")
    print(fee_group)
    letters = re.compile("[A-Z]")
    numbers = re.compile("[0-9\.]+")
    fees_dict = dict(zip(letters.findall(fee_group), numbers.findall(fee_group)))
    for acronym, value in fees_dict.items():
        print(acronym, value)
        value = change_sign(value)
        row[fee_mapping.get(acronym, "missing")] = value
    return row


# In[75]:


aub_group_columns = [
    "remittance_date",
    "insurer",
    "insurer_short_name",
    "doc_format",
    "broker",
    "insured_name",
    "policy_number",
    "type",
    "effective_date",
    "invoice_number",
    "premium_ex_gst",
    "underwriting_fee",
    "levies_01",
    "levies_02",
    "gst_premium",
    "broker_commission",
    "gst_broker_commission",
    "line_net",
    "remittance_total",
    "original_filename",
    "new_filename",
    "full_text",
]


def process_aub_group_rows(header, rows, full_columns, columns="full"):
    fee_mapping = {
        "P": "premium_ex_gst",
        "U": "underwriting_fee",
        "G": "gst_premium",
        "S": "levies_01",
        "F": "levies_02",
        "B": "broker_commission",
        "N": "gst_broker_commission",
    }
    transformed_rows = []
    for row in rows:
        print(row)
        row = process_fee_group(row, fee_mapping)
        row["line_net"] = change_sign(row["line_net"])
        print("Line Net: ", row["line_net"])
        final = {**header, **row}
        final.pop("fee_group", None)
        transformed_rows.append(final)
    df = pd.DataFrame(transformed_rows)
    df = convert_money_columns(df, money_columns_all)
    try:
        if columns == "full":
            df = df[full_columns]
        else:
            df = df[common_columns]
    except:
        pass
    return df


# In[23]:


portrait_columns = [
    "remittance_date",
    "insurer",
    "insurer_short_name",
    "doc_format",
    "broker",
    "broker_reference",
    "insured_name",
    "policy_number",
    "risk_type",
    "type",
    "effective_date",
    "invoice_number",
    "premium_inc_commission_inc_gst",
    "broker_commission",
    "gst_broker_commission",
    "line_net",
    "remittance_total",
    "original_filename",
    "new_filename",
    "full_text",
]


def process_portrait_rows(header, rows, full_columns, columns="full"):
    transformed_rows = []
    for row in rows:
        final = {**header, **row}
        transformed_rows.append(final)
    df = pd.DataFrame(transformed_rows)
    df = convert_money_columns(df, money_columns_all)
    try:
        if columns == "full":
            df = df[full_columns]
        else:
            df = df[common_columns]
    except:
        pass
    return df


# In[24]:


brokerplus_columns = [
    "remittance_date",
    "insurer",
    "insurer_short_name",
    "doc_format",
    "broker",
    "insured_name",
    "policy_number",
    "type",
    "effective_date",
    "invoice_number",
    "premium_ex_gst",
    "levies_01",
    "gst_premium",
    "levies_02",
    "broker_commission",
    "gst_broker_commission",
    "gross_premium_ex_commission",
    "earlier_paid",
    "line_net",
    "remittance_total",
    "original_filename",
    "new_filename",
    "full_text",
]


def process_brokerplus_rows(header, rows, full_columns, columns="full"):
    transformed_rows = []
    for row in rows:
        final = {**header, **row}
        transformed_rows.append(final)
    df = pd.DataFrame(transformed_rows)
    df = convert_money_columns(df, money_columns_all)
    try:
        if columns == "full":
            df = df[full_columns]
        else:
            df = df[common_columns]
    except:
        pass
    return df


# In[25]:


brokers_advantage_columns = [
    "remittance_date",
    "branch",
    "insurer",
    "doc_format",
    "insurer_short_name",
    "broker",
    "broker_reference",
    "insured_name",
    "policy_number",
    "type",
    "effective_date",
    "invoice_number",
    "premium_ex_gst",
    "underwriting_fee",
    "levies_01",
    "levies_02",
    "levies_03",
    "broker_commission",
    "net_premium_ex_commission",
    "gst_premium_ex_commission",
    "line_net",
    "remittance_total",
    "original_filename",
    "new_filename",
    "full_text",
]


def process_brokers_advantage_rows(header, rows, full_columns, columns="full"):
    transformed_rows = []
    for row in rows:
        final = {**header, **row}
        transformed_rows.append(final)
    df = pd.DataFrame(transformed_rows)
    df = convert_money_columns(df, money_columns_all)
    try:
        if columns == "full":
            df = df[full_columns]
        else:
            df = df[common_columns]
    except:
        pass
    return df


# In[26]:


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


# In[27]:


def create_files_grouped_by_insurer(df):
    gb = df.groupby("insurer_short_name")
    [gb.get_group(x) for x in gb.groups]
    return gb


# In[28]:


def save_daily_files(all_dfs):
    groups = create_files_grouped_by_insurer(all_dfs)
    for group in groups:
        display(group[0])
        excel_filename = (op / group[0]).with_suffix(".xlsx")
        group[1].to_excel(excel_filename, index=False)
        display(group[1])


# In[29]:


def make_hyperlink(folder, value):
    url = f'=HYPERLINK(".\\{folder}\\{value}", "PDF")'
    return url


# In[30]:


def create_mapping(target):
    rows = pd.read_excel(cp / "company_mapping.xlsx", sheet_name=target)
    rows.to_dict(orient="records")
    mapping = {}
    for row in rows.values:
        mapping[row[0]] = row[1]
    return mapping


# In[32]:


def replace_blanks(row, mapping, target):
    if row[target] == None:
        for item in mapping.keys():
            if item in row["full_text"]:
                return item
    else:
        return row[target]


# In[ ]:


# In[ ]:
