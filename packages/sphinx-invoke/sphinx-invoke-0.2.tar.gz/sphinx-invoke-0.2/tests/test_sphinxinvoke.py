import os
import xml.etree.ElementTree as etree
import pytest


__copyright__ = 'Copyright (C) 2019, Nokia'

TESTDOCS = os.path.join(os.path.dirname(__file__), 'testdocs')
EXPECTED = os.path.join(os.path.dirname(__file__), 'expected')


@pytest.mark.parametrize('xml', ['cli.xml', 'cli_noargs.xml'])
def test_sphinxinvoke(script_runner, tmpdir, xml):
    build = tmpdir.dirname

    ret = script_runner.run('sphinx-build', '-E', '-b', 'xml', TESTDOCS, build)

    assert ret.success, (ret.stdout, ret.stderr)
    for subsec, expsubsec in zip(get_subsections(os.path.join(build, xml)),
                                 get_subsections(os.path.join(EXPECTED, xml))):
        assert_elements_equal(subsec, expsubsec)


def get_subsections(xmlfile):
    section = etree.parse(xmlfile).getroot().findall('section')[0]
    return section.findall('section')


def assert_elements_equal(e1, e2):
    assert (e1.tag == e2.tag and
            e1.text == e2.text and
            e1.attrib == e2.attrib)
    for sube1, sube2 in zip(e1, e2):
        assert_elements_equal(sube1, sube2)
