import src.CommandLineInterface as CommandLineInterface
from src.XMLAnalyzerException import *
from src.XMLExtractorException import *
from src import XMLUtil
import constants
import sys
from src import ApplicationInterface

import traceback

def main():
    # to test through here:
    # sys.argv=['Main.py', '../config.xacfg', '../SAP_XMLs/payload18_test.xml', 'None', 'CompoundEmployee', 'person_id_external', '==', '16386']
    # sys.argv=['Main.py', '../config.xacfg', '../SAP_XMLs/payload19_test.xml', 'legacy-boomi-empl-extraction', 'None']
    # sys.argv=['Main.py', '../config.xacfg', 'list']

    with open('../SAP_XMLs/payload19_test.xml', 'r') as f:
        print(ApplicationInterface.extract(f.read(), 'legacy-boomi-empl-extraction', {'EmployeeIDExternal': '00805194'}))

    return -1

    constants.config_filepath= sys.argv[1] if sys.argv[1] != '' else constants.config_filepath
    actual_arguments = sys.argv[2:]

    if len(actual_arguments) == 0:  # no additional arguments were provided
        s = None
        while s != "exit":
            try:
                s = input('~: ')
                out = CommandLineInterface.parse(s)
                print(out)
            except Exception as e:
                print(traceback.format_exc())
                print(e)

        print('program closed')
    elif actual_arguments[0] == 'list':
        sys.stdout.write(XMLUtil.list_templates(constants.config_filepath))
    else:
        if len(actual_arguments) == 6:
            out = CommandLineInterface.call_filter(actual_arguments)
        elif len(actual_arguments) == 3:
            out = CommandLineInterface.call_extraction(actual_arguments)
        else:
            raise IncorrectArgumentNumberException('3 for extraction, 6 for filtering', actual_arguments)

        if 'None' in actual_arguments:
            sys.stdout.write(out)

    return 0

if __name__ == '__main__':
    main()
