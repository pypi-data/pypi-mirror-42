import requests
import logging
import re
import os

from .workbook import Workbook

from .utils import sanitize_phone, is_dnc_json_response_on_dnc

from .errors import (
    InvalidTokenError, InvalidPhoneFormatError, InvalidJSONResponseError,
    ResponseCodeNotOkError
)

from .constants import PROD_DNC_URL, MOCK_DNC_URL

log = logging.getLogger(__name__)


class RealValidation:
    """RealValidation Application Object

    Parameters
    ----------
    workbooks : list
        List of workbook paths to validate against RealValidation DNC API
    token : str
        RealValidation API Token. Defaults to environmental variable
        ``RV_TOKEN``
    output : str
        RealValidation API Output. Defaults to ``json``
    url : str
        RealValidation API URL. Defaults to
        ``https://api.realvalidation.com/rpvWebService/DNCLookup.php``
    phone_regex : str
        Regex to use when validating phone numbers. Defaults to ``r'^\d{10}$'``
    staging: bool
        If ``True`` RealValidation utilizes the Mock API, overrides ``url`` parameter

    """
    DEFAULT_OUTPUT = 'json'
    DEFAULT_URL = PROD_DNC_URL

    PHONE_REGEX = r'^\d{10}$'  # 10 numeric digits only

    def _verify_phone(self, phone):
        """Verifies a phone using PHONE_REGEX

        Parameters
        ----------
        phone : str
            Phone to be verified.

        Returns
        -------
        bool
            True if successful, otherwise method raises exception (see below)

        Raises
        ------
        InvalidPhoneFormatException
            If the phone couldn't be verified using PHONE_REGEX

        """
        if re.match(self.phone_regex, phone):
            return True

        raise InvalidPhoneFormatError

    def __init__(self,
                 workbooks=None,
                 token=os.environ.get('RV_TOKEN'),
                 output=DEFAULT_OUTPUT,
                 url=DEFAULT_URL,
                 phone_regex=PHONE_REGEX,
                 staging=False):

        if token is None:
            raise InvalidTokenError

        if workbooks is not None:
            self.workbooks = [Workbook(workbook) for workbook in workbooks]

        self.output = output
        self.token = token
        self.phone_regex = phone_regex

        self.url = url
        if staging:
            self.url = MOCK_DNC_URL

        log.debug('<RealValidation {} >'.format(self.__dict__))

    def lookup_phone(self, phone):
        """Makes a request to the RealValidation DNC API

        Parameters
        ----------
        phone : str
            10 numerical digits representing a phone number.

        Returns
        -------
        dict
            Dictionary representing JSON response from RealValidation DNC API.

        """
        sanitized_phone = sanitize_phone(phone)

        self._verify_phone(sanitized_phone)

        # assemble our request payload
        payload = dict(
            output=self.output,
            token=self.token,
            phone=sanitized_phone
        )

        # initiate our request
        req = requests.get(self.url, params=payload)

        # if request isn't ok raise for status
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        # attempt to decode json from response
        # if we can't, raise error
        try:
            data = req.json()
        except ValueError:
            raise InvalidJSONResponseError

        # if realvalidation RESPONSECODE isn't OK raise error
        if data.get('RESPONSECODE') != 'OK':
            raise ResponseCodeNotOkError

        return data

    def lookup_phones_from_workbooks(self):
        """Validates Workbooks against RealValidation DNC API

        Returns
        -------
        dict
            Dictionary with values of ``valid`` and ``invalid`` rows

        """

        valid_rows = []
        invalid_rows = []

        # for every one of our sheets in `self.workbooks`
        for workbook in self.workbooks:
            for sheet in workbook.sheets:

                # for each row in sheet, lookup phone
                phone_column_index = sheet.phone_column_index
                for row in sheet.get_row_values():

                    if row and row is not None:
                        on_dnc = self.lookup_phone_from_row(row, phone_column_index)

                        # append to respective array if valid/invalid
                        if on_dnc:
                            invalid_rows.append(row)
                        else:
                            valid_rows.append(row)

        return dict(valid=valid_rows, invalid=invalid_rows)

    def lookup_phone_from_row(self, row, phone_column_index):
        """Lookup phone from row at index

        Parameters
        ----------
        row : list
            List of strings containing phone

        phone_column_index : int
            Index/Position of phone in row list

        Returns
        -------
        bool
            True/False value whether phone is on dnc or not

        """
        phone = row[phone_column_index]

        try:
            response = self.lookup_phone(phone)
            on_dnc = is_dnc_json_response_on_dnc(response)

            return on_dnc

        except InvalidPhoneFormatError:
            log.error('InvalidPhoneFormatError phone: "{}"'.format(phone))
