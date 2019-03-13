# (c) 2018 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
lookup: yang_xml2json
author: Ansible Network
version_added: "2.7"
short_description: Converts xml input to json structure output by mapping it against corresponding Yang model
description:
  - This plugin lookups the input xml data, typically Netconf rpc response received from remote host
    and convert it to json format as defined by RFC 7951 JSON Encoding of Data Modeled with YANG
options:
  _terms:
    description:
      - Input xml file path that adheres to a given yang model. This can be a Netconf/Restconf xml rpc response
        that contains operational and configuration data received from remote host.
    required: True
    type: path
  yang_file:
    description:
      - Path to yang model file against which the xml file is validated and converted to json as per json encoding
        of data modeled with YANG.
    required: True
    type: path
  search_path:
    description:
      - This option is a colon C(:) separated list of directories to search for imported yang modules
        in the yang file mentioned in C(path) option. If the value is not given it will search in
        the current directory.
    required: false
  keep_tmp_files:
    description:
      - This is a boolean flag to indicate if the intermediate files generated while validation json
       configuration should be kept or deleted. If the value is C(true) the files will not be deleted else by
        default all the intermediate files will be deleted irrespective of whether task run is
        successful or not. The intermediate files are stored in path C(~/.ansible/tmp/json2xml), this
        option is mainly used for debugging purpose.
    default: False
    type: bool
"""

EXAMPLES = """
- name: translate json to xml
  debug: msg="{{ lookup('yang_xml2json', interfaces_config.xml,
                         yang_file='openconfig/public/release/models/interfaces/openconfig-interfaces.yang',
                         search_path='openconfig/public/release/models:pyang/modules/') }}"
"""

RETURN = """
_raw:
   description: The translated json structure from xml
"""

import os
import imp
import sys
import time
import json
import shutil
import uuid
import glob

from copy import deepcopy

from ansible.plugins.lookup import LookupBase
from ansible.module_utils.six import StringIO
from ansible.utils.path import unfrackpath, makedirs_safe
from ansible.module_utils._text import to_text
from ansible.errors import AnsibleError

try:
    import pyang        # noqa
except ImportError:
    raise AnsibleError("pyang is not installed")

try:
    from lxml import etree
except ImportError:
    raise AnsibleError("lxml is not installed")

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()

XM2JSONL_DIR_PATH = "~/.ansible/tmp/xml2json"


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):

        res = []
        try:
            xml_data = terms[0]
        except IndexError:
            raise AnsibleError("Either xml string or path to xml file must be specified")

        try:
            yang_file = kwargs['yang_file']
        except KeyError:
            raise AnsibleError("value of 'yang_file' must be specified")

        yang_file = os.path.realpath(os.path.expanduser(yang_file))
        if not os.path.isfile(yang_file):
            # Maybe we are passing a glob?
            yang_files = glob.glob(yang_file)
            if not yang_files:
                # Glob returned no files
                raise AnsibleError('%s invalid file path' % yang_file)
        else:
            yang_files = [yang_file]

        search_path = kwargs.pop('search_path', '')
        keep_tmp_files = kwargs.pop('keep_tmp_files', False)

        abs_search_path = None
        for path in search_path.split(':'):
            path = os.path.realpath(os.path.expanduser(path))
            if abs_search_path is None:
                abs_search_path = path
            else:
                abs_search_path += ':' + path
            if path != '' and not os.path.isdir(path):
                raise AnsibleError('%s is invalid directory path' % path)

        search_path = abs_search_path

        plugindir = unfrackpath(XM2JSONL_DIR_PATH)
        makedirs_safe(plugindir)

        if os.path.isfile(xml_data):
            # input is xml file path
            xml_file_path = xml_data
        else:
            # input is xml string, copy it to file in temporary location
            xml_file_path = os.path.join(XM2JSONL_DIR_PATH, '%s.%s' % (str(uuid.uuid4()), 'xml'))
            xml_file_path = os.path.realpath(os.path.expanduser(xml_file_path))
            with open(xml_file_path, 'w') as f:
                if not xml_data.startswith('<?xml version'):
                    xml_data = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_data
                data = xml_data
                f.write(data)

        xml_file_path = os.path.realpath(os.path.expanduser(xml_file_path))

        try:
            # validate xml
            etree.parse(xml_file_path)
            display.vvvv("Parsing xml data from temporary file: %s" % xml_file_path)
        except Exception as exc:
            if not keep_tmp_files:
                shutil.rmtree(os.path.realpath(os.path.expanduser(XM2JSONL_DIR_PATH)), ignore_errors=True)
            raise AnsibleError("Failed to load xml data: %s" % (to_text(exc, errors='surrogate_or_strict')))

        base_pyang_path = sys.modules['pyang'].__file__
        pyang_exec_path = find_file_in_path('pyang')
        pyang_exec = imp.load_source('pyang', pyang_exec_path)

        saved_arg = deepcopy(sys.argv)
        sys.modules['pyang'].__file__ = base_pyang_path

        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        sys.stdout = sys.stderr = StringIO()

        xsl_file_path = os.path.join(XM2JSONL_DIR_PATH, '%s.%s' % (str(uuid.uuid4()), 'xsl'))
        json_file_path = os.path.join(XM2JSONL_DIR_PATH, '%s.%s' % (str(uuid.uuid4()), 'json'))
        xls_file_path = os.path.realpath(os.path.expanduser(xsl_file_path))
        json_file_path = os.path.realpath(os.path.expanduser(json_file_path))

        # fill in the sys args before invoking pyang
        sys.argv = [pyang_exec_path, '-f', 'jsonxsl', '-o', xls_file_path, '-p', search_path,
                    "--lax-quote-checks"] + yang_files
        display.display("Generating xsl file '%s' by executing command '%s'" % (xls_file_path, ' '.join(sys.argv)), log_only=True)
        try:
            pyang_exec.run()
        except SystemExit:
            pass
        except Exception as e:
            if not keep_tmp_files:
                shutil.rmtree(os.path.realpath(os.path.expanduser(XM2JSONL_DIR_PATH)), ignore_errors=True)
            raise AnsibleError('Error while generating intermediate (xsl) file: %s' % e)
        finally:
            err = sys.stderr.getvalue()
            if err and 'error' in err.lower():
                if not keep_tmp_files:
                    shutil.rmtree(os.path.realpath(os.path.expanduser(XM2JSONL_DIR_PATH)), ignore_errors=True)
                raise AnsibleError('Error while generating (xsl) intermediate file: %s' % err)

        xsltproc_exec_path = find_file_in_path('xsltproc')

        # fill in the sys args before invoking xsltproc
        sys.argv = [xsltproc_exec_path, '-o', json_file_path, xsl_file_path, xml_file_path]
        display.display("Generating json data in temp file '%s' by executing command '%s'" % (json_file_path, ' '.join(sys.argv)), log_only=True)
        time.sleep(5)
        try:
            os.system(' '.join(sys.argv))
        except SystemExit:
            pass
        finally:
            err = sys.stderr.getvalue()
            if err and 'error' in err.lower():
                if not keep_tmp_files:
                    shutil.rmtree(os.path.realpath(os.path.expanduser(XM2JSONL_DIR_PATH)), ignore_errors=True)
                raise AnsibleError('Error while translating to json: %s' % err)
            sys.argv = saved_arg
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr

        try:
            display.vvvv("Reading output json data from temporary file: %s" % json_file_path)
            with open(json_file_path) as fp:
                content = json.load(fp)
        except Exception as e:
            raise AnsibleError('Error while reading json document: %s' % e)
        finally:
            if not keep_tmp_files:
                shutil.rmtree(os.path.realpath(os.path.expanduser(XM2JSONL_DIR_PATH)), ignore_errors=True)
        res.append(content)

        return res


def find_file_in_path(filename):
    # Check $PATH first, followed by same directory as sys.argv[0]
    paths = os.environ['PATH'].split(os.pathsep) + [os.path.dirname(sys.argv[0])]
    for dirname in paths:
        fullpath = os.path.join(dirname, filename)
        if os.path.isfile(fullpath):
            return fullpath
