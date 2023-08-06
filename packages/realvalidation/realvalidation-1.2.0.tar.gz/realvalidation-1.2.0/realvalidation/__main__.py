from .argparser import parser
from .realvalidation import RealValidation
from .utils import write_rows_to_workbook
from . import logger

import logging
import tempfile

log = logging.getLogger(__name__)


def main():
    args = parser.parse_args()

    realvalidation = RealValidation(
        workbooks=args.workbook,
        token=args.api_token,
        url=args.api_url,
        staging=args.staging
    )

    res = realvalidation.lookup_phones_from_workbooks()

    temp_dir = tempfile.mkdtemp(prefix='realvalidation')

    write_rows_to_workbook(res.get('valid'), temp_dir, 'valid')
    write_rows_to_workbook(res.get('invalid'), temp_dir, 'invalid')

    log.debug('written to "{}"'.format(temp_dir))


if __name__ == '__main__':
    main()
