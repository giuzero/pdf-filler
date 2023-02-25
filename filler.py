import jinja2
import pdfkit
import csv
from os import getenv
from datetime import datetime
from dotenv import load_dotenv
from dotenv import dotenv_values
load_dotenv()

template_loader = jinja2.FileSystemLoader('./')
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("assets/template.html")

constants = dict(dotenv_values("assets/constant_config"))
constants['printing_date']=datetime.today().strftime("%d/%m/%Y")

csv_fields = []

with open('assets/variable_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = True
    for row in csv_reader:
        if header:
            csv_fields.extend(row)
            header = False
        else:
            csv_dict = {}
            for field_index in range(len(row)):
                csv_dict.update({csv_fields[field_index]:row[field_index]})
            csv_dict.update(constants)
            
            raw_pdf = template.render(csv_dict)
            config=pdfkit.configuration(wkhtmltopdf=getenv("WKHTMLTOPDF_PATH"))
            pdfkit.from_string(raw_pdf, "{}_{}_RLTS.pdf".format(csv_dict['name'], datetime.now().strftime("%Y%m%d%H%M%S")), configuration=config, css='assets/style.css')
            








