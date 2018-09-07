# (c) 2018 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: yang_spec
    author: Ansible Network
    version_added: "2.6"
    short_description:  This plugin reads the content of given yang document and generates json and xml
                        configuration skeleton and a tree structure of yang document.
    description:
      - This plugin parses yang document and generates json and xml configuration skeleton and a tree
        structure of yang document. The tree structure document is as per RFC 8340 which helps to consume
        the yang document along with json and xml configuration skeleton.
    options:
      _terms:
        description: The path points to the location of the top level yang module which
        is to be transformed into to Ansible spec.
        required: True
      search_path:
        description:
          - is a colon C(:) separated list of directories to search for imported yang modules
            in the yang file mentioned in C(path) option. If the value is not given it will search in
            the current directory.
      defaults:
        description:
          - This boolean flag indicates if the generated json and xml configuration schema should have
            fields initialized with default values or not.
        default: False
      doctype:
        description:
          - Identifies the root node of the configuration skeleton. If value is C(config) only configuration
            data will be present in skeleton, if value is C(data) both config and state data fields will be present
            in output.
        default: config
        choices: ['config', 'data']
      annotations:
        description:
          - The boolean flag identifies if the xml skeleton should have comments describing the field or not.
        default: False
        type: bool
      keep_tmp_files:
        description:
          - This is a boolean flag to indicate if the intermediate files generated while creating spec
            should be kept or deleted. If the value is C(true) the files will not be deleted else by
            default all the intermediate files will be deleted irrespective of whether task run is
            successful or not. The intermediate files are stored in path C(~/.ansible/tmp/yang_spec), this
            option is mainly used for debugging purpose.
        default: False
        type: bool
"""

EXAMPLES = """
- name: Get interface yang config spec without defaults
  set_fact:
    interfaces_spec: "{{ lookup('yang_spec', 'openconfig/public/release/models/interfaces/openconfig-interfaces.yang',
                            search_path='openconfig/public/release/models:pyang/modules/', defaults=True, doctype='data') }}"

- name: Get interface yang spec with defaults and state data
  set_fact:
    interfaces_spec: "{{ lookup('yang_spec', 'openconfig/public/release/models/interfaces/openconfig-interfaces.yang',
                            search_path='openconfig/public/release/models:pyang/modules/', defaults=True, doctype='data') }}"
"""

RETURN = """
  _list:
    description:
      - It returns json skeleton configuration schema, xml skeleton schema and tree structure (as per RFC 8340)
        for given yang schema.
    type: complex
    contains:
      tree:
        description: The tree representation of yang scehma as per RFC 8340
        returned: success
        type: dict
        sample: |
            module: openconfig-interfaces
              +--rw interfaces
                 +--rw interface* [name]
                    +--rw name             -> ../config/name
                    +--rw config
                    |  +--rw name?            string
                    |  +--rw type             identityref
                    |  +--rw mtu?             uint16
                    |  +--rw loopback-mode?   boolean
                    |  +--rw description?     string
                    |  +--rw enabled?         boolean
                    +--ro state
                    |  +--ro name?            string
                    |  +--ro type             identityref
                    |  +--ro mtu?             uint16
                    |  +--ro loopback-mode?   boolean
                    |  +--ro description?     string
                    |  +--ro enabled?         boolean
                    |  +--ro ifindex?         uint32
                    |  +--ro admin-status     enumeration
                    |  +--ro oper-status      enumeration
                    |  +--ro last-change?     oc-types:timeticks64
      json_skeleton:
        description: The json configuration skeleton generated from yang document
        returned: success
        type: dict
        sample: |
            {
                "openconfig-interfaces:interfaces": {
                    "interface": [
                        {
                            "hold-time": {
                                "config": {
                                    "down": "",
                                    "up": ""
                                }
                            },
                            "config": {
                                "description": "",
                                "type": "",
                                "enabled": "",
                                "mtu": "",
                                "loopback-mode": "",
                                "name": ""
                            },
                            "name": "",
                            "subinterfaces": {
                                "subinterface": [
                                    {
                                        "index": "",
                                        "config": {
                                            "index": "",
                                            "enabled": "",
                                            "description": ""
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
      xml_skeleton:
        description: The xml configuration skeleton generated from yang document
        returned: success
        type: dict
        sample: |
            <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
              <interfaces xmlns="http://openconfig.net/yang/interfaces">
                <interface>
                  <name/>
                  <config>
                    <name/>
                    <type/>
                    <mtu/>
                    <loopback-mode></loopback-mode>
                    <description/>
                    <enabled>True</enabled>
                  </config>
                  <hold-time>
                    <config>
                      <up></up>
                      <down></down>
                    </config>
                  </hold-time>
                  <subinterfaces>
                    <subinterface>
                      <index/>
                      <config>
                        <index></index>
                        <description/>
                        <enabled></enabled>
                      </config>
                    </subinterface>
                  </subinterfaces>
                </interface>
              </interfaces>
            </config>
"""

import os
import optparse
import sys
import shutil
import json
import uuid

import subprocess
from copy import deepcopy
from collections import Sequence

from ansible.plugins.lookup import LookupBase
from ansible.module_utils.six import StringIO, iteritems, string_types, PY3
from ansible.utils.path import unfrackpath, makedirs_safe
from ansible.errors import AnsibleError

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

try:
    from pyang import plugin, error
    from pyang import statements
    from pyang.util import unique_prefixes
    from pyang.types import Decimal64Value
except ImportError:
    raise AnsibleError("pyang is not installed")

YANG_SPEC_DIR_PATH = "~/.ansible/tmp/yang_spec"


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):

        res = []
        output = {}
        try:
            yang_file = terms[0]
        except IndexError:
            raise AnsibleError('the yang file must be specified')

        yang_file = os.path.realpath(os.path.expanduser(yang_file))
        if not os.path.isfile(yang_file):
            raise AnsibleError('%s invalid file path' % yang_file)

        search_path = kwargs.pop('search_path', '')
        annotations = kwargs.pop('annotations', '')

        for path in search_path.split(':'):
            path = os.path.realpath(os.path.expanduser(path))
            if path is not '' and not os.path.isdir(path):
                raise AnsibleError('%s is invalid directory path' % path)

        keep_tmp_files = kwargs.pop('keep_tmp_files', False)
        defaults = kwargs.pop('defaults', False)
        doctype = kwargs.pop('doctype', 'config')

        valid_doctype = ['config', 'data']
        if doctype not in valid_doctype:
            raise AnsibleError('doctpe value %s is invalid, valid value are %s' % (path, ', '.join(valid_doctype)))

        pyang_exec_path = find_file_in_path('pyang')

        saved_arg = deepcopy(sys.argv)
        sys.stdout = sys.stderr = StringIO()

        plugindir = unfrackpath(YANG_SPEC_DIR_PATH)
        makedirs_safe(plugindir)

        tree_file_path = os.path.join(YANG_SPEC_DIR_PATH, '%s.%s' % (str(uuid.uuid4()), 'txt'))
        xml_file_path = os.path.join(YANG_SPEC_DIR_PATH, '%s.%s' % (str(uuid.uuid4()), 'xml'))
        json_file_path = os.path.join(YANG_SPEC_DIR_PATH, '%s.%s' % (str(uuid.uuid4()), 'json'))
        tree_file_path = os.path.realpath(os.path.expanduser(tree_file_path))
        xml_file_path = os.path.realpath(os.path.expanduser(xml_file_path))
        json_file_path = os.path.realpath(os.path.expanduser(json_file_path))

        # fill in the sys args before invoking pyang to retrieve xml skeleton
        sample_xml_skeleton_cmd = [pyang_exec_path, '-f', 'sample-xml-skeleton', '-o', xml_file_path, yang_file, '-p', search_path,
                                   "--sample-xml-skeleton-doctype", doctype, "--lax-quote-checks"]

        if defaults:
            sample_xml_skeleton_cmd.append("--sample-xml-skeleton-defaults")

        if annotations:
            sample_xml_skeleton_cmd.append("--sample-xml-skeleton-annotations")

        try:
            subprocess.check_output(' '.join(sample_xml_skeleton_cmd), stderr=subprocess.STDOUT, shell=True)
        except SystemExit:
            pass
        except Exception as e:
            if not keep_tmp_files:
                shutil.rmtree(os.path.realpath(os.path.expanduser(YANG_SPEC_DIR_PATH)), ignore_errors=True)
            raise AnsibleError('Error while generating skeleton xml file: %s' % e)
        finally:
            err = sys.stdout.getvalue()
            if err and 'error' in err.lower():
                if not keep_tmp_files:
                    shutil.rmtree(os.path.realpath(os.path.expanduser(YANG_SPEC_DIR_PATH)), ignore_errors=True)
                raise AnsibleError('Error while generating skeleton xml file: %s' % err)

        sys.stdout.flush()
        sys.stderr.flush()

        # fill in the sys args before invoking pyang to retrieve tree structure
        tree_cmd = [pyang_exec_path, '-f', 'tree', '-o', tree_file_path, yang_file, '-p', search_path, "--lax-quote-checks"]

        try:
            subprocess.check_output(' '.join(tree_cmd), stderr=subprocess.STDOUT, shell=True)
        except SystemExit:
            pass
        except Exception as e:
            if not keep_tmp_files:
                shutil.rmtree(os.path.realpath(os.path.expanduser(YANG_SPEC_DIR_PATH)), ignore_errors=True)
            raise AnsibleError('Error while generating tree file: %s' % e)
        finally:
            err = sys.stdout.getvalue()
            if err and 'error' in err.lower():
                if not keep_tmp_files:
                    shutil.rmtree(os.path.realpath(os.path.expanduser(YANG_SPEC_DIR_PATH)), ignore_errors=True)
                raise AnsibleError('Error while generating tree file: %s' % err)

        sys.stdout.flush()
        sys.stderr.flush()

        plugin_file_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yang_spec.py')
        shutil.copy(plugin_file_src, plugindir)

        # fill in the sys args before invoking pyang to retrieve json skeleton
        sample_json_skeleton_cmd = [pyang_exec_path, '--plugindir', plugindir, '-f', 'sample-json-skeleton', '-o', json_file_path,
                                    yang_file, '-p', search_path, '--lax-quote-checks', '--sample-json-skeleton-doctype', doctype]

        if defaults:
            sample_json_skeleton_cmd.append("--sample-json-skeleton-defaults")

        try:
            subprocess.check_output(' '.join(sample_json_skeleton_cmd), stderr=subprocess.STDOUT, shell=True)
        except SystemExit:
            pass
        except Exception as e:
            if not keep_tmp_files:
                shutil.rmtree(os.path.realpath(os.path.expanduser(YANG_SPEC_DIR_PATH)), ignore_errors=True)
            raise AnsibleError('Error while generating skeleton json file: %s' % e)
        finally:
            err = sys.stdout.getvalue()
            if err and 'error' in err.lower():
                if not keep_tmp_files:
                    shutil.rmtree(os.path.realpath(os.path.expanduser(YANG_SPEC_DIR_PATH)), ignore_errors=True)
                raise AnsibleError('Error while generating tree json: %s' % err)

        with open(tree_file_path, 'r') as f:
            output['tree'] = f.read()

        with open(xml_file_path, 'r') as f:
            output['xml_skeleton'] = f.read()

        with open(json_file_path, 'r') as f:
            output['json_skeleton'] = json.load(f)

        if not keep_tmp_files:
            shutil.rmtree(plugindir, ignore_errors=True)
        res.append(output)
        return res


def find_file_in_path(filename):
    # Check $PATH first, followed by same directory as sys.argv[0]
    paths = os.environ['PATH'].split(os.pathsep) + [os.path.dirname(sys.argv[0])]
    for dirname in paths:
        fullpath = os.path.join(dirname, filename)
        if os.path.isfile(fullpath):
            return fullpath


def pyang_plugin_init():
    plugin.register_plugin(SampleJSONSkeletonPlugin())


def to_list(val):
    if isinstance(val, Sequence):
        return list(val)
    elif val is not None:
        return [val]
    else:
        return list()


class SampleJSONSkeletonPlugin(plugin.PyangPlugin):

    def add_opts(self, optparser):
        optlist = [
            optparse.make_option("--sample-json-skeleton-doctype",
                                 dest="doctype",
                                 default="data",
                                 help="Type of sample JSON document " +
                                 "(data or config)."),
            optparse.make_option("--sample-json-skeleton-defaults",
                                 action="store_true",
                                 dest="sample_defaults",
                                 default=False,
                                 help="Insert data with defaults values."),
        ]
        g = optparser.add_option_group(
            "Sample-json-skeleton output specific options")
        g.add_options(optlist)

    def add_output_format(self, fmts):
        self.multiple_modules = True
        fmts['sample-json-skeleton'] = self

    def setup_fmt(self, ctx):
        ctx.implicit_errors = False

    def emit(self, ctx, modules, fd):
        """Main control function.
        """
        for (epos, etag, eargs) in ctx.errors:
            if error.is_error(error.err_level(etag)):
                raise error.EmitError("sample-json-skeleton plugin needs a valid module")
        tree = {}
        self.defaults = ctx.opts.sample_defaults
        self.doctype = ctx.opts.doctype
        if self.doctype not in ("config", "data"):
            raise error.EmitError("Unsupported document type: %s" %
                                  self.doctype)

        for module in modules:
            self.process_children(module, tree, None)
        json.dump(tree, fd, indent=4)

    def process_children(self, node, parent, pmod):
        """Process all children of `node`, except "rpc" and "notification".
        """
        for ch in node.i_children:
            if self.doctype == 'config' and not ch.i_config:
                continue
            if ch.keyword in ["rpc", "notification"]:
                continue
            if ch.keyword in ["choice", "case"]:
                self.process_children(ch, parent, pmod)
                continue
            if ch.i_module.i_modulename == pmod:
                nmod = pmod
                nodename = ch.arg
            else:
                nmod = ch.i_module.i_modulename
                nodename = "%s:%s" % (nmod, ch.arg)
            if ch.keyword == "container":
                ndata = dict()
                self.process_children(ch, ndata, nmod)
                parent[nodename] = ndata
            elif ch.keyword == "list":
                ndata = list()
                ndata.append({})
                self.process_children(ch, ndata[0], nmod)
                parent[nodename] = ndata
            elif ch.keyword == "leaf":
                if ch.arg == 'keepalive-interval':
                    pass
                ndata = str(ch.i_default) if (self.defaults and ch.i_default is not None) else ""
            elif ch.keyword == "leaf-list":
                ndata = to_list(str(ch.i_default)) if (self.defaults and ch.i_default is not None) else [""]
            parent[nodename] = ndata

    def base_type(self, type):
        """Return the base type of `type`."""
        while 1:
            if type.arg == "leafref":
                node = type.i_type_spec.i_target_node
            elif type.i_typedef is None:
                break
            else:
                node = type.i_typedef
            type = node.search_one("type")
        if type.arg == "decimal64":
            return [type.arg, int(type.search_one("fraction-digits").arg)]
        elif type.arg == "union":
            return [type.arg, [self.base_type(x) for x in type.i_type_spec.types]]
        else:
            return type.arg
