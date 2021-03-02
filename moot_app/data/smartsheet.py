from os import environ
import requests
from flask import abort

def get_auth_header():
    return { 'Authorization': f'Bearer {environ.get("SMARTSHEET_ACCESS_TOKEN")}' }

def build_url(endpoint):
    return 'https://api.smartsheet.com/2.0' + endpoint

def build_headers(headers = {}):
    full_header = get_auth_header()
    full_header.update(headers)
    return full_header

def get_sheets():
    headers = build_headers({'Content-Type':'application/json'})
    url = build_url('/sheets')
    response = requests.get(url, headers=headers)
    sheets = response.json()
    if 'message' in sheets and sheets['message'] != 'SUCCESS':
        abort(500, response)
    sheets = response.json()
    return sheets

def get_sheet_by_id(id):
    headers = build_headers({'Content-Type':'application/json'})
    url = build_url(f'/sheets/{id}')
    response = requests.get(url, headers=headers)
    sheet = response.json()
    if 'message' in sheet and sheet['message'] != 'SUCCESS':
        abort(500, response)
    sheet = response.json()
    return sheet

def get_sheet_id_by_name(name):
    sheets = get_sheets()
    return next((sheet['id'] for sheet in sheets['data'] if sheet['name'] == name), None)

def get_sheet_by_name(name):
    sheet_id = get_sheet_id_by_name(name)
    if sheet_id == None:
        return None
    return get_sheet_by_id(sheet_id)

def get_column_map_for_sheet(sheet):
    return { column['title']:column['id'] for column in sheet['columns'] }

def get_cell_value_by_column_name(row, column_name, column_map):
    column_id = column_map[column_name]
    return next((cell['value'] for cell in row['cells'] if 'value' in cell and cell['columnId'] == column_id), None)

def create_booking(booking):
    sheet_id = get_sheet_id_by_name('Early Bird Bookings - Responses')
    sheet = get_sheet_by_id(sheet_id)
    column_map = get_column_map_for_sheet(sheet)

    headers = build_headers({'Content-Type':'application/json'})
    url = build_url(f'/sheets/{sheet_id}/rows')
    cells = [{'columnId':column_map[column_name], 'value': value} for (column_name,value) in booking.toSheetColumnDict.items()]
    json = {"cells": cells}

    response = requests.post(url, headers=headers, json=json)
    booking = response.json()
    if 'message' in booking and booking['message'] != 'SUCCESS':
        abort(500, response)

    return booking