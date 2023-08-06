import re
import os
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image
import progressbar
import tempfile
try:
    from sdsparser.configs import SDSRegexes
except ModuleNotFoundError:
    from configs import SDSRegexes
from threading import Thread


class SDSParser:

    def __init__(self, request_keys=[], sds_txt_dir='', file_info=False):
        """
        define a set of data request keys
        """

        if request_keys:
            self.request_keys = request_keys
        else:
            self.request_keys = SDSRegexes.REQUEST_KEYS

        self.sds_txt_dir = sds_txt_dir

        self.ocr_override = True
        self.ocr_ran = False
        self.force_ocr = False

        self.file_info = file_info

    def get_sds_data(self, sds_file_path, extract_method=''):
        """
        retrieve requested sds data
        """

        self.reset_state()

        self.sds_file_path = sds_file_path

        self.set_extract_method(extract_method)

        self.sds_text = self.get_sds_text(sds_file_path)

        self.manufacturer = self.get_manufacturer(self.sds_text)

        regexes = SDSParser.define_regexes(self.manufacturer)

        self.sds_data = self.search_sds_text(self.sds_text, regexes)

        data_not_listed = self.data_not_listed

        if data_not_listed() and not self.ocr_ran and self.ocr_override:
            self.sds_data = self.get_sds_data(sds_file_path, extract_method='ocr')

        if self.file_info:
            self.sds_data.update(self.get_file_info())

        return self.sds_data

    def data_not_listed(self):
        """
        check if data not listed
        """

        for _, data in self.sds_data.items():
            if data.lower() != 'data not listed':
                return False
        return True

    def reset_state(self):
        self.ocr_override = True
        self.ocr_ran = False
        self.force_ocr = False

    def set_extract_method(self, extract_method):
        if extract_method == 'ocr':
            self.force_ocr = True
        if extract_method == 'text':
            self.ocr_override = False

    def get_sds_text(self, sds_file_path):
        """
        execute the text extraction function corresponding to the
        specified extract method
        """

        txt_file_path = self.find_matching_txt_file_path()

        if txt_file_path is not None:
            sds_text = SDSParser.get_text_from_file(txt_file_path)

        elif self.force_ocr is True:
            sds_text = self.get_sds_image_text(sds_file_path)
        else:
            sds_text = SDSParser.get_sds_pdf_text(sds_file_path)
            if sds_text == '' and self.ocr_override and not self.ocr_ran:
                sds_text = self.get_sds_image_text(sds_file_path)

        return sds_text

    def find_matching_txt_file_path(self):
        """
        find txt file with same name as sds file
        and return the path to the txt file if found
        """
        sds_file_name = os.path.split(self.sds_file_path)[1]
        sds_file_key = os.path.splitext(sds_file_name)[0]
        for root, dirs, txt_files in os.walk(self.sds_txt_dir):
            for txt_file in txt_files:
                if txt_file.startswith(sds_file_key):
                    return os.path.join(root, txt_file)
        return None

    @staticmethod
    def get_text_from_file(txt_file_path):
        with open(txt_file_path, 'r') as text_file:
            return text_file.read()

    def get_sds_image_text(self, sds_file_path):
        """
        extract text from pdf file by applying ocr
        """

        print('=======================================================')
        print('Processing:', sds_file_path.split('/')[-1] + '...')

        sds_text = ''

        def ocr_task(_temp_path):
            nonlocal sds_text
            sds_text += image_to_string(Image.open(_temp_path))

        with tempfile.TemporaryDirectory() as path:

            page_images = convert_from_path(sds_file_path,
                                            fmt='jpeg',
                                            output_folder=path,
                                            dpi=300)

            for i, image in enumerate(page_images):
                page_images[i] = image.convert('L')

            dir_list = SDSParser.get_sorted_dir_list(path)

            # initialize progress bar
            progress_bar = progressbar.ProgressBar().start()
            num_pages = len(dir_list)

            threads = []
            for page_image in dir_list:

                _temp_path = os.path.join(path, page_image)
                thread = Thread(target=ocr_task, args=(_temp_path,))
                threads.append(thread)

            for thread in threads:
                thread.start()

            for idx, thread in enumerate(threads):
                thread.join()
                progress_bar.update((idx/num_pages)*100)
            progress_bar.update(100)
            print()

            self.ocr_ran = True

            return sds_text

    @staticmethod
    def get_sorted_dir_list(path):

        dir_list = os.listdir(path)
        regex = re.compile(r"[\d]*(?=\.jpg)")
        dir_list.sort(key=lambda x: regex.search(x)[0])
        return dir_list

    @staticmethod
    def get_sds_pdf_text(sds_file_path):
        """
        extract text directly from pdf file
        """

        text = ''
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        try:
            with open(sds_file_path, 'rb') as fh:
                for page in PDFPage.get_pages(fh,
                                              caching=True,
                                              check_extractable=True):
                    page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()

        except PDFTextExtractionNotAllowed:
            pass
        # close open handles
        converter.close()
        fake_file_handle.close()

        return text

    @staticmethod
    def get_manufacturer(sds_text):
        """
        define set of regular expressions to be used for data matching by searching
        for the manufacturer name within the sds text
        """

        for manufacturer, regexes in SDSRegexes.SDS_FORMAT_REGEXES.items():

            regex = re.compile(*regexes['manufacturer'])

            match = regex.search(sds_text)

            if match:
                return manufacturer

        return None

    def define_regexes(manufacturer):

        if manufacturer is not None:
            return SDSParser.compile_regexes(SDSRegexes.SDS_FORMAT_REGEXES[manufacturer])
        else:
            return SDSParser.compile_regexes(SDSRegexes.DEFAULT_SDS_FORMAT)

    @staticmethod
    def compile_regexes(regexes):
        """
        return a dictionary of compiled regular expressions
        """

        compiled_regexes = {}

        for name, regex in regexes.items():

            compiled_regexes[name] = re.compile(*regex)

        return compiled_regexes

    def search_sds_text(self, sds_text, regexes):
        """
        construct a dictionary by iterating over each data request and
        performing a regular expression match
        """

        sds_data = {}

        for request_key in self.request_keys:

            if request_key in regexes:

                regex = regexes[request_key]
                match = SDSParser.find_match(sds_text, regex)

                sds_data[request_key] = match

        return sds_data

    @staticmethod
    def find_match(sds_text, regex):
        """
        perform a regular expression match and return matched data
        """

        matches = regex.search(sds_text)

        if matches is not None:

            return SDSParser.get_match_string(matches)

        else:

            return 'Data not listed'

    @staticmethod
    def get_match_string(matches):
        """
        retrieve matched group string
        """

        group_matches = 0
        match_string = ''

        for name, group in matches.groupdict().items():
            if group is not None:

                group = group.replace('\n', '').strip()

                if group_matches > 0:
                    match_string += ', ' + group
                else:
                    match_string += group

                group_matches += 1

        if not match_string:
            match_string = 'No data available'

        return match_string

    def get_file_info(self):
        file_info = {
                     'format': self.manufacturer,
                     'file_name': self.sds_file_path.split('/')[-1],
                     'ocr_ran': self.get_extract_method(),
                     }
        return file_info

    def get_extract_method(self):
        text_file_path = self.find_matching_txt_file_path()
        if text_file_path is not None:
            ocr_ran = 'ocr' in os.path.split(text_file_path)[1]
        else:
            ocr_ran = self.ocr_ran

        return ocr_ran
