# -*- coding: utf-8 -*-

import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO

from shapely.geometry import LineString, Point, Polygon
from lxml import etree
from pyramid.path import AssetResolver
from pyramid_oereb.lib.renderer.extract.xml_ import Renderer
from pyramid_oereb.lib.renderer.versions.xml_ import Renderer as VersionsRenderer
from pyramid_oereb.views.webservice import Parameter
from tests import params, schema_xml_versions, schema_xml_extract
from tests.mockrequest import MockRequest
from tests.renderer import DummyRenderInfo, get_default_extract,\
    get_empty_glossary_extract, get_none_glossary_extract
from mako.lookup import TemplateLookup
import pytest


@pytest.fixture
def xml_templates():
    a = AssetResolver('pyramid_oereb')
    resolver = a.resolve('lib/renderer/extract/templates/xml')
    templates = TemplateLookup(
        directories=[resolver.abspath()],
        output_encoding='utf-8',
        input_encoding='utf-8'
    )
    return templates


def test_get_gml_id():
    renderer = Renderer(None)
    assert renderer._get_gml_id() == 'gml1'
    assert renderer._get_gml_id() == 'gml2'
    assert renderer._get_gml_id() == 'gml3'


@pytest.mark.parametrize('parameters', params)  # noqa
def test_line(parameters, xml_templates):
    line = LineString(((0, 0), (1, 1)))
    template = xml_templates.get_template('geometry/line.xml')

    def get_gml_id():
        return 'gml1'

    content = template.render(**{
        'params': parameters,
        'default_language': 'de',
        'line': line,
        'get_gml_id': get_gml_id
    }).decode('utf-8').split('\n')
    expected_content = """
    <gml:LineString gml:id="gml1">
        <gml:pos>0.0 0.0</gml:pos>
        <gml:pos>1.0 1.0</gml:pos>
    </gml:LineString>
    """.split('\n')
    expected_lines = []
    for line in expected_content:
        expected_lines.append(line.strip())
    content_lines = []
    for line in content:
        content_lines.append(line.strip())
    assert expected_lines == content_lines


@pytest.mark.parametrize('parameters', params)  # noqa
def test_point(parameters, xml_templates):
    point = Point((0, 0))
    template = xml_templates.get_template('geometry/point.xml')
    content = template.render(**{
        'params': parameters,
        'default_language': 'de',
        'point': point
    }).decode('utf-8').split('\n')
    expected_content = """
    <gml:pos>0.0 0.0</gml:pos>""".split('\n')
    expected_lines = []
    for line in expected_content:
        expected_lines.append(line.strip())
    content_lines = []
    for line in content:
        content_lines.append(line.strip())
    assert expected_lines == content_lines


@pytest.mark.parametrize('parameters', params)  # noqa
def test_polygon(parameters, xml_templates):
    polygon = Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)))
    template = xml_templates.get_template('geometry/polygon.xml')

    def get_gml_id():
        return 'gml1'

    content = template.render(**{
        'params': parameters,
        'default_language': 'de',
        'polygon': polygon,
        'get_gml_id': get_gml_id
    }).decode('utf-8').split('\n')
    expected_content = """
    <gml:Polygon gml:id="gml1">
        <gml:exterior>
            <gml:LinearRing>
                <gml:pos>0.0 0.0</gml:pos>
                <gml:pos>0.0 1.0</gml:pos>
                <gml:pos>1.0 1.0</gml:pos>
                <gml:pos>1.0 0.0</gml:pos>
                <gml:pos>0.0 0.0</gml:pos>
            </gml:LinearRing>
        </gml:exterior>
        <gml:interior>
            <gml:LinearRing>
                <gml:pos>0.0 0.0</gml:pos>
                <gml:pos>0.0 1.0</gml:pos>
                <gml:pos>1.0 1.0</gml:pos>
                <gml:pos>1.0 0.0</gml:pos>
                <gml:pos>0.0 0.0</gml:pos>
            </gml:LinearRing>
        </gml:interior>
    </gml:Polygon>""".split('\n')
    expected_lines = []
    for line in expected_content:
        expected_lines.append(line.strip())
    content_lines = []
    for line in content:
        content_lines.append(line.strip())
    assert expected_lines == content_lines


def test_version_against_schema():
    versions = {
        u'GetVersionsResponse': {
            u'supportedVersion': [
                {
                    u'version': u'1.0',
                    u'serviceEndpointBase': u'https://example.com'
                }
            ]
        }
    }
    renderer = VersionsRenderer(DummyRenderInfo())
    rendered = renderer._render(versions)

    xmlschema_doc = etree.parse(schema_xml_versions)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    buffer = StringIO(rendered) if sys.version_info.major == 2 else BytesIO(rendered)
    doc = etree.parse(buffer)
    assert xmlschema.validate(doc)


@pytest.mark.parametrize('parameter, test_extract', [
    (
            Parameter('reduced', 'xml', False, False, 'BL0200002829', '1000', 'CH775979211712', 'de'),
            get_default_extract()
    ),
    (
            Parameter('reduced', 'xml', False, False, 'BL0200002829', '1000', 'CH775979211712', 'de'),
            get_empty_glossary_extract()
    ),
    (
            Parameter('reduced', 'xml', False, False, 'BL0200002829', '1000', 'CH775979211712', 'de'),
            get_none_glossary_extract()
    )
])
def test_extract_against_schema(parameter, test_extract):
    extract = test_extract
    renderer = Renderer(DummyRenderInfo())
    renderer._language = u'de'
    renderer._request = MockRequest()
    renderer._request.route_url = lambda url, **kwargs: "http://example.com/current/view"
    rendered = renderer._render(extract, parameter)

    xmlschema_doc = etree.parse(schema_xml_extract)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    buffer = StringIO(rendered) if sys.version_info.major == 2 else BytesIO(rendered)
    doc = etree.parse(buffer)
    xmlschema.assertValid(doc)
