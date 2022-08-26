# coding=utf-8
import os
from glob import glob
import shutil
import unittest
from io import StringIO

from mock import Mock, patch
from lxml import etree

from data_import import (DXImport,
                         CaseDataExtractor,
                         ResultDataExtractor,
                         process_incoming_data,
                         compress_log)
from zipfile import ZipFile
from settings import test as settings


class DataImportTestCase(unittest.TestCase):

    def setUp(self):
        self.data_import = DXImport(settings, "ref")

    def test_get_handler_mismatch(self):

        self.assertIsNone(self.data_import.get_handler("wrong"))

    def test_get_handler(self):

        handler_opts = self.data_import.get_handler(
            "/var/www/whatever/SendCase_B06IS00_randomstuff.xml")

        self.assertEqual(handler_opts["endpoint"], "/v0/case/")
        self.assertEqual(handler_opts["data_class"], CaseDataExtractor)


class CaseDataExtractorTestCase(unittest.TestCase):

    def setUp(self):

        self.case_xml = etree.fromstring("""
   <Case>
      <LibraDefendantType>
         <PersonEntityType>
            <OrganisationName />
            <Title />
            <Forename1 />
            <Forename2 />
            <Forename3 />
            <Surname>ATwoSurname</Surname>
            <DOB>1971-01-01</DOB>
            <Gender>M</Gender>
            <Address1>A Two address</Address1>
            <Address2 />
            <Address3 />
            <Address4 />
            <Address5 />
            <Postcode>a123</Postcode>
            <NINO />
            <DriverNumber />
            <VehicleRegistration />
            <TelephoneNumberBusiness />
            <TelephoneNumberHome />
            <TelephoneNumberMobile />
            <EmailAddress1 />
            <EmailAddress2 />
         </PersonEntityType>
         <DocumentLanguage>EN</DocumentLanguage>
         <HearingLanguage>EN</HearingLanguage>
      </LibraDefendantType>
      <LibraHearingType>
         <SessionTimes>09:00-13:00</SessionTimes>
      </LibraHearingType>
      <LibraCaseType>
         <CaseNumber>061000000045</CaseNumber>
         <CaseURN>00/AA/00000/00</CaseURN>
         <OUCode>B06IS00</OUCode>
         <CaseInitiationType>C</CaseInitiationType>
      </LibraCaseType>
      <LibraOffenceType>
         <OffenceCode>TH68001</OffenceCode>
         <OffenceShortTitle>Theft from the person of another</OffenceShortTitle>
         <WelshOffenceShortTitle>WELSH</WelshOffenceShortTitle>
         <OffenceWording>Contrary to Section 1(1) and 7 of the Theft Act 1968.</OffenceWording>
         <WelshOffenceWording>WELSH</WelshOffenceWording>
         <OffenceSequenceNumber />
      </LibraOffenceType>
      <LibraOffenceType>
         <OffenceCode>TH68001</OffenceCode>
         <OffenceShortTitle>Theft from the person of another</OffenceShortTitle>
         <WelshOffenceShortTitle>WELSH</WelshOffenceShortTitle>
         <OffenceWording>On 26/08/2010 at asdf stole asdfklj asdflkj  to the value of £123 belonging to asdflkj asdflkj .</OffenceWording>
         <WelshOffenceWording>WELSH</WelshOffenceWording>
         <OffenceSequenceNumber/>
      </LibraOffenceType>
   </Case>""")

        self.result_xml = etree.fromstring("""
    <ResultType>
        <LibraCaseType>
            <CaseNumber>011502602908</CaseNumber>
            <CaseURN>02TJ 0012050029783660 15 EW</CaseURN>
            <OUCode>B01LY02</OUCode>
            <DateOfHearing>2004-11-15</DateOfHearing>
        </LibraCaseType>
        <LibraResultOffence>
            <LibraResultData>
                <ResultCode>FVS</ResultCode>
                <ResultShortTitle>UPD - Victim Surcharge</ResultShortTitle>
                <ResultShortTitleWelsh>UPD - Gordal Dioddefwr</ResultShortTitleWelsh>
                <RegisterWording>To pay victim surcharge of £44.00.</RegisterWording>
                <RegisterWordingWelsh/>
            </LibraResultData>
            <LibraResultData>
                <ResultCode>FCOST</ResultCode>
                <ResultShortTitle>UPD - Costs</ResultShortTitle>
                <ResultShortTitleWelsh>UPD - Costau</ResultShortTitleWelsh>
                <RegisterWording>To pay costs of £85.00.</RegisterWording>
                <RegisterWordingWelsh/>
            </LibraResultData>
            <LibraResultData>
                <ResultCode>GPTAC</ResultCode>
                <ResultShortTitle>Guilty Plea taken into account</ResultShortTitle>
                <ResultShortTitleWelsh/>
                <RegisterWording>
                    Defendant's guilty plea taken into account when imposing sentence.
                </RegisterWording>
                <RegisterWordingWelsh/>
            </LibraResultData>
            <LibraResultData>
                <ResultCode>FCC</ResultCode>
                <ResultShortTitle>UPD - Criminal Courts Charge</ResultShortTitle>
                <ResultShortTitleWelsh>UPD - Ffi'r Llysoedd Troseddol</ResultShortTitleWelsh>
                <RegisterWording>To pay a criminal courts charge of £150.00.</RegisterWording>
                <RegisterWordingWelsh/>
            </LibraResultData>
            <LibraResultData>
                <ResultCode>FO</ResultCode>
                <ResultShortTitle>UPD - Fine</ResultShortTitle>
                <ResultShortTitleWelsh>UPD - Dirwy</ResultShortTitleWelsh>
                <RegisterWording>Fined £440.00.</RegisterWording>
                <RegisterWordingWelsh/>
            </LibraResultData>
            <LibraResultData>
                <ResultCode>LEP</ResultCode>
                <ResultShortTitle>Driving record endorsed with penalty points</ResultShortTitle>
                <ResultShortTitleWelsh>Ardystiwyd y cofnod gyrru â phwyntiau cosb</ResultShortTitleWelsh>
                <RegisterWording>Driving record endorsed with 6 points.</RegisterWording>
                <RegisterWordingWelsh/>
            </LibraResultData>
            <LibraResultData>
                <ResultCode>COLLO</ResultCode>
                <ResultShortTitle>UPD - Collection order made</ResultShortTitle>
                <ResultShortTitleWelsh>UPD - Gwnaethpwyd gorchymyn casglu</ResultShortTitleWelsh>
                <RegisterWording>Collection order made.</RegisterWording>
                <RegisterWordingWelsh/>
            </LibraResultData>
            <LibraOffenceType>
                <OffenceCode>RT00002</OffenceCode>
                <OffenceSequenceNumber/>
            </LibraOffenceType>
        </LibraResultOffence>
        <LibraResultOffence>
            <LibraResultData>
                <ResultCode>FO</ResultCode>
                <ResultShortTitle>UPD - Fine</ResultShortTitle>
                <ResultShortTitleWelsh>UPD - Dirwy</ResultShortTitleWelsh>
                <RegisterWording>Fined £220.00.</RegisterWording>
                <RegisterWordingWelsh/>
            </LibraResultData>
            <LibraResultData>
                <ResultCode>GPTAC</ResultCode>
                <ResultShortTitle>Guilty Plea taken into account</ResultShortTitle>
                <ResultShortTitleWelsh/>
                <RegisterWording>
                    Defendant's guilty plea taken into account when imposing sentence.
                </RegisterWording>
                <RegisterWordingWelsh/>
            </LibraResultData>
            <LibraResultData>
                <ResultCode>LEN</ResultCode>
                <ResultShortTitle>Driving record endorsed (no points)</ResultShortTitle>
                <ResultShortTitleWelsh>Ardystiwyd y cofnod gyrru (dim pwyntiau)</ResultShortTitleWelsh>
                <RegisterWording>Driving record endorsed.</RegisterWording>
                <RegisterWordingWelsh/>
            </LibraResultData>
            <LibraOffenceType>
                <OffenceCode>RC00001</OffenceCode>
                <OffenceSequenceNumber/>
            </LibraOffenceType>
        </LibraResultOffence>
        <LibraPaymentTerm>
            <AccountNumber>xxxxxxyyyyyzzzzz</AccountNumber>
            <Division>654</Division>
            <InstalmentAmount/>
            <LumpSumAmount/>
            <PayByDate>2015-11-18</PayByDate>
            <PaymentType>BD</PaymentType>
        </LibraPaymentTerm>
    </ResultType>""")

    def test_case_extraction(self):
        data = CaseDataExtractor.extract(self.case_xml)

        self.assertEqual(data["urn"],
                         self.case_xml.find("LibraCaseType/CaseURN").text)

        self.assertEqual(data["case_number"],
                         self.case_xml.find("LibraCaseType/CaseNumber").text)

        self.assertEqual(data["initiation_type"], self.case_xml.find("LibraCaseType/CaseInitiationType").text)

        offences = self.case_xml.xpath("LibraOffenceType")

        self.assertEqual(len(data["offences"]), len(offences))

        for i, offence in enumerate(offences):
            self.assertEqual(offence.find("OffenceCode").text, data["offences"][i]["offence_code"])
            self.assertEqual(offence.find("OffenceShortTitle").text, data["offences"][i]["offence_short_title"])
            self.assertEqual(offence.find("OffenceWording").text, data["offences"][i]["offence_wording"])
            self.assertEqual(offence.find("OffenceSequenceNumber").text, data["offences"][i]["offence_seq_number"])
            self.assertEqual(offence.find("WelshOffenceShortTitle").text, data["offences"][i]["offence_short_title_welsh"])
            self.assertEqual(offence.find("WelshOffenceWording").text, data["offences"][i]["offence_wording_welsh"])

    def test_result_extraction(self):
        data = ResultDataExtractor.extract(self.result_xml)

        self.assertEqual(data["urn"],
                         self.result_xml.find("LibraCaseType/CaseURN").text)

        self.assertEqual(data["case_number"],
                         self.result_xml.find("LibraCaseType/CaseNumber").text)

        result_offences = self.result_xml.xpath("LibraResultOffence")

        self.assertEqual(len(data["result_offences"]), len(result_offences))

        for idx, offence in enumerate(data["result_offences"]):
            data_offence = data["result_offences"][idx]
            xml_offence = result_offences[idx]

            self.assertEqual(data_offence["offence_code"],
                             xml_offence.xpath("LibraOffenceType/OffenceCode")[0].text)

            self.assertEqual(data_offence["offence_seq_number"],
                             xml_offence.xpath("LibraOffenceType/OffenceSequenceNumber")[0].text)

            self.assertEqual(data_offence["offence_data"][0]["result_code"],
                             xml_offence.xpath("LibraResultData")[0].xpath("ResultCode")[0].text)


class DXImportTestCase(unittest.TestCase):

    def setUp(self):
        self._setup_directory(settings.INCOMING_DIR)
        self._setup_directory(settings.ARCHIVE_DIR)
        self._setup_directory(settings.LOG_DIR)
        self._setup_directory(settings.STATUS_DIR)

    def _setup_directory(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.mkdir(path)

    def _copy_to_incoming(self, file_name):
        """
        Copy a file from test_data_files to the settings.INCOMING_DIR
        """

        file_path = os.path.join(settings.TEST_DATA_FILES, file_name)

        shutil.copy(file_path, settings.INCOMING_DIR)

    @patch("data_import.glob")
    @patch("data_import.send_email")
    def test_email_is_sent_on_fatal_error(self, send_email, glob_mock):
        glob_mock.side_effect = Exception("PROBLEM")

        with self.assertRaises(SystemExit):
            process_incoming_data(settings)

        self.assertTrue(send_email.called)
        self.assertIn("FATAL ERROR", send_email.call_args[0][0])

    @patch("data_import.glob")
    @patch("data_import.send_email")
    def test_email_sent_on_success(self, send_email, glob_mock):
        glob_mock.side_effect = Exception("PROBLEM")

        with self.assertRaises(SystemExit):
            process_incoming_data(settings)

        self.assertTrue(send_email.called)

        self.assertIn("FATAL ERROR", send_email.call_args[0][0])

    @patch("data_import.requests")
    @patch("data_import.send_email")
    def test_archive_is_created(self, send_email, requests_mock):
        requests_mock.post.return_value.status_code = 400

        self._copy_to_incoming("SendCase_B06IS00_TEST.xml")

        archive_file_name = "archive-{}.tar.gz".format("test_ref")

        log_output = StringIO()

        data_import = DXImport(settings, "test_ref", log_output)

        data_import.process_files()

        self.assertTrue(os.path.isfile(os.path.join(settings.ARCHIVE_DIR, archive_file_name)))

    @patch("data_import.requests")
    @patch("data_import.send_email")
    def test_valid_xml_with_non_200_api_response(self, send_email_mock, requests_mock):

        requests_mock.post.return_value.status_code = 400
        requests_mock.post.return_value.content = "API SAID NO"

        self._copy_to_incoming("SendCase_B06IS00_TEST.xml")

        log_output = StringIO()

        data_import = DXImport(settings, "test_ref", log_output)

        data_import.process_files()

        self.assertEqual(data_import.total_files, 1)
        self.assertEqual(data_import.total_failed, 1)
        self.assertEqual(data_import.total_success, 0)

        self.assertIn("FAILED", log_output.getvalue())
        self.assertIn("API SAID NO", log_output.getvalue())

    @patch("data_import.requests")
    @patch("data_import.send_email")
    def test_incoming_directory_is_empty(self, send_email_mock, requests_mock):
        requests_mock.post.return_value.status_code = 201

        self._copy_to_incoming("SendCase_B06IS00_TEST.xml")

        process_incoming_data(settings)

        self.assertEquals(glob(os.path.join(settings.INCOMING_DIR, "*")), [])

    @patch("data_import.requests")
    @patch("data_import.send_email")
    def test_log_file_is_stored(self, send_email_mock, requests_mock):

        requests_mock.post.return_value.status_code = 201

        self._copy_to_incoming("SendCase_B06IS00_TEST.xml")

        self.assertEqual(0, len(glob(os.path.join(settings.LOG_DIR, "*"))))

        process_incoming_data(settings)

        self.assertEqual(1, len(glob(os.path.join(settings.LOG_DIR, "*"))))

    @patch("data_import.send_email")
    def test_status_file_is_created(self, send_email_mock):

        dir_name = "20150610_manual"

        os.makedirs(
            os.path.join(settings.INCOMING_DIR, dir_name))

        status_path = os.path.join(
            settings.STATUS_DIR,
            "{}-success[{}].txt".format(dir_name, "test_ref"))

        log_output = StringIO()

        data_import = DXImport(settings, "test_ref", log_output)
        data_import.process_files()

        self.assertTrue(os.path.exists(status_path))

    def test_log_unicode_in_urn(self):
        log_output = StringIO()
        data_import = DXImport(settings, "test_ref", log_output)
        data_import.log('TEST', u'00AA1234567 ')

        self.assertIn('"00AA1234567"',log_output.getvalue())

    def test_compress_log(self):
        path = "test/test_data_files/dx_report-2017-08-24_050802.csv"
        zipped = compress_log(path)
        zip = ZipFile(zipped)
        self.assertListEqual(zip.namelist(), ['dx_report-2017-08-24_050802.csv'])
        csv_info = zip.infolist().pop()
        self.assertEqual(csv_info.file_size, 188858)
        self.assertEqual(csv_info.compress_size, 10798)

if __name__ == "__main__":
    unittest.main()
