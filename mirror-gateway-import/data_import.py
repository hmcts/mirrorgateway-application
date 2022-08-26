#!/usr/bin/env python

"""
The DX data import script.

Processes files placed by DX in the ftp upload directory, and attempts to insert case data
into the MaP system via its REST API.

This script should be run via cron each night.

"""

from custom_logger import CustomLogger
import boto3
import csv
import datetime as dt
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from glob import glob
import os
import json
import sys
from io import StringIO, BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import tarfile
import traceback
from urllib.parse import urljoin
from lxml import etree
import gnupg
import requests


def is_success(code):
    return 200 <= code <= 299


def send_email(subject, body, settings=None, files=None):
    """
    Send a file, optionally with attachment.

    Uses AWS boto and SES.

    AWS access keys will default to None if not supplied in settings
    in which case the correct AWS EC2 role permissions will be required
    to allow SES use.
    """

    recipients = settings.EMAIL_TO.split(", ")
    msg = MIMEMultipart()
    msg["Subject"] = "[{}] {}".format(settings.RELEASE_STAGE, subject)
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = recipients[0]

    if len(recipients) > 1:
        msg["Cc"] = ", ".join(recipients[1:])

    part = MIMEText(body)
    msg.attach(part)

    # the attachment
    if files:
        for file_, name in files:

            part = MIMEApplication(file_)
            part.add_header("Content-Disposition", "attachment", filename=name)
            msg.attach(part)

    connection = boto3.client('ses', region_name="eu-west-1")
    connection.send_raw_email(
        RawMessage={'Data': msg.as_string()},
        Source=msg["From"],
        Destinations=recipients,
    )


def insert_data(args):
        """
        Submit the data to the API endpoint
        """
        (data, endpoint, file_name, username, password) = args

        response = requests.post(
            endpoint,
            data=json.dumps(data),
            auth=(username, password),
            headers={"Content-type": "application/json"},
            verify=False)

        return response


class CaseDataExtractor(object):
    """
    The Case data extractor

    Usage:
        data = CaseDataExtractor.extract(node)
    """

    CASE_MAP = {
        "urn": "LibraCaseType/CaseURN",
        "case_number": "LibraCaseType/CaseNumber",
        "initiation_type": "LibraCaseType/CaseInitiationType",
        "date_of_hearing": "LibraCaseType/DateOfHearing",
        "ou_code": "LibraCaseType/OUCode",
        "language": "LibraDefendantType/HearingLanguage"
    }

    CASE_EXTRA_MAP = {
        "OrganisationName": "LibraDefendantType/PersonEntityType/OrganisationName",
        "Title": "LibraDefendantType/PersonEntityType/Title",
        "Forename1": "LibraDefendantType/PersonEntityType/Forename1",
        "Forename2": "LibraDefendantType/PersonEntityType/Forename2",
        "Forename3": "LibraDefendantType/PersonEntityType/Forename3",
        "Surname": "LibraDefendantType/PersonEntityType/Surname",
        "DOB": "LibraDefendantType/PersonEntityType/DOB",
        "Gender": "LibraDefendantType/PersonEntityType/Gender",
        "Address1": "LibraDefendantType/PersonEntityType/Address1",
        "Address2": "LibraDefendantType/PersonEntityType/Address2",
        "Address3": "LibraDefendantType/PersonEntityType/Address3",
        "Address4": "LibraDefendantType/PersonEntityType/Address4",
        "Address5": "LibraDefendantType/PersonEntityType/Address5",
        "PostCode": "LibraDefendantType/PersonEntityType/Postcode",
        "DateOfHearing": "LibraCaseType/DateOfHearing",
        "NINO": "LibraDefendantType/PersonEntityType/NINO",
        "VehicleRegistration": "LibraDefendantType/PersonEntityType/VehicleRegistration",
        "TelephoneNumberBusiness": "LibraDefendantType/PersonEntityType/TelephoneNumberBusiness",
        "TelephoneNumberHome": "LibraDefendantType/PersonEntityType/TelephoneNumberHome",
        "TelephoneNumberMobile": "LibraDefendantType/PersonEntityType/TelephoneNumberMobile",
        "EmailAddress1": "LibraDefendantType/PersonEntityType/EmailAddress1",
        "EmailAddress2": "LibraDefendantType/PersonEntityType/EmailAddress2",
        "HearingLanguage": "LibraDefendantType/PersonEntityType/HearingLanguage",
    }

    CASE_OFFENCE_MAP = {
        "offence_code": "OffenceCode",
        "offence_short_title": "OffenceShortTitle",
        "offence_wording": "OffenceWording",
        "offence_seq_number": "OffenceSequenceNumber",
        "offence_short_title_welsh": "WelshOffenceShortTitle",
        "offence_wording_welsh": "WelshOffenceWording"}

    @classmethod
    def extract(cls, node):
        """
        Take an XML node and return a JSON string which can be submitted to the
        API endpoint
        """

        data = {}
        extra_data = {}
        offences = []

        for key, path in cls.CASE_MAP.items():
            elem = node.xpath(path)

            if elem:
                if key == "language":
                    data[key] = elem[0].text.lower()
                else:
                    data[key] = elem[0].text

        for key, path in cls.CASE_EXTRA_MAP.items():
            elem = node.xpath(path)

            if elem and elem[0].text and elem[0].text.strip():
                extra_data[key] = elem[0].text

        data["extra_data"] = extra_data

        for offence in node.xpath("LibraOffenceType"):
            offence_data = {}

            for key, path in cls.CASE_OFFENCE_MAP.items():
                elem = offence.xpath(path)

                if elem:
                    offence_data[key] = elem[0].text

            if offence_data:
                offences.append(offence_data)

        data["offences"] = offences
        return data


class ResultDataExtractor(object):
    """
    The Result data extractor

    Usage:
        data = ResultDataExtractor.extract(node)
    """

    RESULT_MAP = {
        "urn": "LibraCaseType/CaseURN",
        "case_number": "LibraCaseType/CaseNumber",
        "ou_code": "LibraCaseType/OUCode",
        "date_of_hearing": "LibraCaseType/DateOfHearing",
        "account_number": "LibraPaymentTerm/AccountNumber",
        "division": "LibraPaymentTerm/Division",
        "instalment_amount": "LibraPaymentTerm/InstalmentAmount",
        "lump_sum_amount": "LibraPaymentTerm/LumpSumAmount",
        "pay_by_date": "LibraPaymentTerm/PayByDate",
        "payment_type": "LibraPaymentTerm/PaymentType",
    }

    RESULT_OFFENCE_MAP = {
        "offence_code": "LibraOffenceType/OffenceCode",
        "offence_seq_number": "LibraOffenceType/OffenceSequenceNumber",
        "offence_data": {
            "result_code": "ResultCode",
            "result_short_title": "ResultShortTitle",
            "result_short_title_welsh": "ResultShortTitleWelsh",
            "result_wording": "RegisterWording",
            "result_wording_welsh": "RegisterWordingWelsh"}}

    @classmethod
    def extract(cls, node):
        """
        Take an XML node and return a JSON string which can be submitted to the
        API endpoint
        """

        data = {}
        offences = []

        for key, path in cls.RESULT_MAP.items():
            elem = node.xpath(path)

            if elem:
                data[key] = elem[0].text

        for offence_xml in node.xpath("LibraResultOffence"):
            offence = {}

            for key, path in cls.RESULT_OFFENCE_MAP.items():
                if key == "offence_data":
                    offence_data = []
                    for onode in offence_xml.xpath("LibraResultData"):
                        odata = {}
                        for okey, opath in path.items():
                            elem = onode.xpath(opath)

                            if elem:
                                if okey == "result_wording" and elem[0].text is None or elem[0].text == "":
                                    odata = {}
                                    break
                                else:
                                    odata[okey] = elem[0].text

                        if odata:
                            offence_data.append(odata)

                    offence["offence_data"] = offence_data
                else:
                    elem = offence_xml.xpath(path)

                    if elem:
                        offence[key] = elem[0].text

            if offence:
                offences.append(offence)

        data["result_offences"] = offences
        return data


class DXImport(object):

    def __init__(self, settings,  import_ref, log_file=None):
        """
        settings - the settings module
        import_ref - a reference (e.g. timestamp)
        log_file - a file handler for writing log information
        """

        self.settings = settings
        self.import_ref = import_ref
        self.log_file = log_file or StringIO()

        case_schema = etree.XMLSchema(etree.parse(settings.CASE_SCHEMA_PATH))
        result_schema = etree.XMLSchema(etree.parse(settings.RESULT_SCHEMA_PATH))

        # NOTE: for the time being we're only processing SendCase_B05I200* files
        # which cover the Manchester region. This will need to be refactored
        # when we start receiving DX data for other regions.

        self.file_map = {
            "SendCase_": {
                "endpoint": "/v0/case/",
                "data_class": CaseDataExtractor,
                "parser": etree.XMLParser(schema=case_schema),
            },
            "SendResult_": {
                "endpoint": "/v0/result/",
                "data_class": ResultDataExtractor,
                "parser": etree.XMLParser(schema=result_schema),
            }
        }

        self.incoming_dir = glob(os.path.join(self.settings.INCOMING_DIR, "*"))

        self.total_files = 0
        self.total_failed_files = 0
        self.total_skipped_files = 0
        self.total_success = 0
        self.total_failed = 0
        self.file_list = []

        self.csv_output = csv.writer(
            self.log_file, quoting=csv.QUOTE_ALL)

        self.csv_output.writerow(["Status", "URN", "File", "Info"])

    def clear_incoming_directory(self):
        files = os.listdir(self.settings.INCOMING_DIR)

        for f in files:
            path = os.path.join(self.settings.INCOMING_DIR, f)
            if os.path.isdir(path):

                # don't delete the status directory
                if path != os.path.normpath(self.settings.STATUS_DIR):
                    shutil.rmtree(path)
            else:
                os.unlink(path)

    def archive_incoming_files(self):
        """
        tar and gzip all files in the incoming directory, move to the archive
        directory, and clear the incoming directory.
        """

        if not self.incoming_dir:
            return

        if self.settings.ENCRYPT_ARCHIVE_DATA:
            gpg = gnupg.GPG(gnupghome=self.settings.GPG_HOME_DIRECTORY)
            gpg.encoding = 'utf-8'

        archive_path = os.path.join(
            self.settings.ARCHIVE_DIR,
            "archive-{}.tar.gz".format(self.import_ref))

        with tarfile.open(archive_path, "w:gz") as tar:
            for path in self.incoming_dir:
                if path == os.path.normpath(self.settings.STATUS_DIR):
                    continue

                tar.add(path, recursive=True)

        self.clear_incoming_directory()

        if self.settings.ENCRYPT_ARCHIVE_DATA:
            with open(archive_path, "rb") as file_:
                encrypted_data = gpg.encrypt_file(
                    file_,
                    recipients=[self.settings.GPG_RECIPIENT],
                    output=archive_path+".gpg",
                    always_trust=True)

            if encrypted_data.ok:
                os.unlink(archive_path)
            else:
                raise Exception("Unable to encrypt {} - reason: {}".format(
                    archive_path,
                    encrypted_data.status))

    def get_handler(self, file_name):
        """
        Get the relevant handler - e.g. Case or Result
        """

        for file_match, opts in self.file_map.items():
            if file_match in file_name:
                regions = opts.get("regions", None)

                if regions:
                    for region in regions:
                        if region in file_name:
                            return opts
                else:
                    return opts

        return None

    def create_status_files(self):
        """
        Create a status file in the relevant directory to indicate
        that we processed a directory, e.g. :

        {ftp-root}/status/20150610-[our-ref]-success.txt
        """

        if self.settings.CREATE_STATUS_FILES:

            for path in self.incoming_dir:

                path = os.path.normpath(path)

                if os.path.isdir(path) and path != os.path.normpath(self.settings.STATUS_DIR):

                    dir_name = os.path.basename(path)

                    status_path = os.path.join(
                        self.settings.STATUS_DIR,
                        "{}-success[{}].txt".format(dir_name, self.import_ref))

                    open(status_path, "a").close()

    def load_data(self, file_path, parser):
        """
        Returns an XSD validated LXML object
        """

        return etree.parse(file_path, parser)

    def log(self, status, urn="", file_name="", note="", exc=None):
        """
        Record failed/success

        status: the status of the action, e.g. PASSED/FAILED
        urn: the urn (optional)
        file_name: the name of the file, again optional
        note: additional information
        """

        # fix for RST-647 bad libra input
        urn = urn.encode('ascii', 'ignore').decode()

        self.csv_output.writerow([status, urn, file_name, note])

    def process_files(self, manual_run=False):
        """
        Iterate over files in the incoming directory and attempt to extract
        data and insert into the API.
        """
        grand_total = 0

        for file_path in self.get_incoming_file_list():
            file_name = file_path.replace(self.settings.INCOMING_DIR, "")

            self.total_files += 1

            handler_opts = self.get_handler(file_name)

            if not handler_opts:

                self.log("SKIPPED", "", file_name, "Not processing this file.")

                self.total_skipped_files += 1

                continue

            if manual_run:
                print("Processing {}".format(file_path))

            try:
                xml_obj = self.load_data(file_path, handler_opts["parser"])
            except (etree.XMLSyntaxError, IOError):

                ex_type, ex, tb = sys.exc_info()

                self.log("FAILED", "", file_name, "File does not match schema")

                self.total_failed_files += 1

                continue

            total = 0
            requests = []

            endpoint = urljoin(self.settings.API_ENDPOINT, handler_opts["endpoint"])

            for node in xml_obj.getroot():

                data = handler_opts["data_class"].extract(node)
                if data["urn"]:
                    requests.append((data, endpoint, file_name, self.settings.API_USERNAME, self.settings.API_PASSWORD))
                else:
                    self.log("FAILED", "", file_name, "URN missing")

                    self.total_failed += 1

                total += 1

            for request_data in requests:
                urn = request_data[0]["urn"]
                response = insert_data(request_data)
                if is_success(response.status_code):
                    self.log("SUCCESS", urn, file_name)

                    self.total_success += 1

                else:
                    if manual_run:
                        print(response.content)
                    self.log("FAILED", urn, file_name, response.content.decode())

                    self.total_failed += 1

            grand_total += total

            if manual_run:
                print("Processed {} records".format(total))

        if manual_run:
            print("All records: {}".format(grand_total))

        self.create_status_files()
        self.archive_incoming_files()

    def get_summary(self):
        return "\n".join([
            "total files: {}".format(self.total_files),
            "total skipped files: {}".format(self.total_skipped_files),
            "total failed files: {}".format(self.total_failed_files),
            "total successful case creations: {}".format(self.total_success),
            "total failed case creations: {}".format(self.total_failed),
            "files received from LIBRA: \n\t{}".format("\n\t".join(self.file_list)),
        ])

    def get_incoming_file_list(self):
        """
        Return a list of files in the incoming dir or sub dirs in the
        incoming dir.

        Will only scan directories one level deep.
        """
        for path in self.incoming_dir:
            if os.path.isdir(path):
                if path == os.path.normpath(self.settings.STATUS_DIR):
                    # don't process the status/receipt dir
                    continue
                for file_ in glob(os.path.join(path, "*")):
                    if not os.path.isdir(file_):
                        self.file_list.append(file_)
                        yield file_
            else:
                self.file_list.append(path)
                yield path

def compress_log(log_path):
    zipped = BytesIO()

    with ZipFile(zipped, 'w', ZIP_DEFLATED) as myzip:
        myzip.write(log_path, os.path.basename(log_path))

    zipped.seek(0)
    return zipped

def process_incoming_data(settings):
    import_ref = dt.datetime.now().strftime("%Y-%m-%d_%H%m%S")

    log_path = os.path.join(settings.LOG_DIR,
                            "DX-import-log_{}.csv".format(import_ref))
    try:
        log_file = open(log_path, "w")
    except IOError:

        sys.stderr.write("Unable to create log file: {}".format(log_path))
        sys.exit(1)

    try:
        data_import = DXImport(settings, import_ref, log_file)
        data_import.process_files(settings.MANUAL_RUN)

    except Exception:
        ex_type, ex, tb = sys.exc_info()

        tb_formatted = "\n".join(traceback.format_tb(tb))

        error_msg = """
        Type: {0}
        Exception: {1}
        Traceback:
        {2}
        """.format(ex_type, ex, tb_formatted)

        # send_email("FATAL ERROR ref: {}".format(import_ref),
        #            error_msg, settings=settings)

        sys.exit(1)

    finally:
        log_file.close()

    compressed = compress_log(log_path)
    # send_email(
    #     "DX data import ref: {}".format(import_ref),
    #     data_import.get_summary(),
    #     settings=settings,
    #     files=([compressed.read(), "dx_report-{}.csv.zip".format(import_ref)], ))

    # CGI have configured the soap gateway so that we will always receive a set
    # of files.  During weekends and holiday periods those files may be empty,
    # but as long as we have some files, we can be certain that the process is working.
    # This will not help us if we have only received a partial set of files, but CGI
    # currently do an adequate job of detecting and resending files in this situation.
    #
    # This logging message is so that Sensu can be configured to alert if it hasn't seen
    # "DATA IMPORT SUCCESS" once every 24 hours.  Note, this message will appear in the
    # makeaplea_mgw_import container, not an external log file.
    if data_import.total_files:
        CustomLogger(basename="makeaplea_dx::data_import.py").logger.info("SOAP GATEWAY: DATA IMPORT SUCCESS")


if __name__ == "__main__":

    from settings import main as settings

    process_incoming_data(settings)
