# Purpose: Create a structured HTML view of the DXF tags - not a CAD drawing!
# Created: 20.05.13
# Copyright (c) 2013-2018, Manfred Moitzi
# License: MIT License
"""
Creates a structured HTML view of the DXF tags - not a CAD drawing!
"""
import os
from typing import TYPE_CHECKING, Sequence, Tuple, Iterable, Dict, Set
from ezdxf.lldxf.types import tag_type, is_point_code, is_pointer_code, is_binary_data
from ezdxf.lldxf.types import GROUP_MARKERS, HEX_HANDLE_CODES, HANDLE_CODES, BINARY_FLAGS
from ezdxf.tools import escape
from ezdxf.sections.sections import KNOWN_SECTIONS
from ezdxf.lldxf.packedtags import PackedTags

from .reflinks import get_reference_link

if TYPE_CHECKING:  # import forward declarations
    from ezdxf.eztypes import Drawing, Table, DXFEntity, ExtendedTags, DXFTag

# Tag groups

# HTML templates
# Section
ALL_SECTIONS_TPL = '<div class="dxf-sections">\n{content}\n</div>'
COMMON_SECTION_TPL = '<div id="{this_id}" class="dxf-section">' \
                     '<div class="dxf-section-name">SECTION: {ref_link}</div>\n' \
                     '<div class="button-bar">{prev} {next} <a class="link-button" href="#section-links">top<a/></div>\n' \
                     '{{content}}\n</div>\n'
HEADER_SECTION_TPL = '<div id="dxf-header" class="dxf-header">\n{content}\n</div>'
TABLES_SECTION_TPL = '<div id="dxf-tables" class="dxf-tables">{content}</div>'
BLOCKS_SECTION_TPL = '<div id="dxf-blocks" class="dxf-blocks">\n{content}\n</div>'

# Section content
HEADER_VAR_TPL = '<div class="hdr-var" ><span class="tag-code">{code}</span> <span class="var-type">{type}</span>' \
                 ' <span class="tag-value">{value}</span></div>'

CUSTOM_VAR_TPL = '<div class="hdr-var" >Custom Property: <span class="cu-tag">{tag}</span> ::' \
                 ' <span class="cu-tag-value">{value}</span></div>'

TABLE_TPL = '<div id="{name}-table" class="dxf-table">\n' \
            '<div class="dxf-table-name">{ref_link}</div>\n{nav}\n{header}\n{entries}\n</div>'
ENTITIES_TPL = '<div class="dxf-entities">\n{}\n</div>'

# DXF Entities
ENTITY_TPL = '<div class="dxf-entity"><div class="dxf-entity-name">{name}</div>\n{references} {tags}\n</div>'
BLOCK_TPL = '<div class="dxf-block">\n<div class="dxf-block-name">{name}</div>\n{block}\n{entities}\n{endblk}\n</div>'
TAG_LIST_TPL = '<div class="dxf-tags">\n{content}\n</div>'

# Basic Tags
TAG_TPL = '<div class="dxf-tag" ><span class="tag-code">{code}</span> <span class="var-type">{type}</span>' \
          ' <span class="tag-value">{value}</span></div>'
TAG_HANDLE_DEF_TPL = '<div class="dxf-tag"><span id="{value}" class="tag-code">{code}</span>' \
                     ' <span class="var-type">{type}</span> <span class="tag-value">#{value}</span></div>'
TAG_VALID_LINK_TPL = '<div class="dxf-tag"><span class="tag-code">{code}</span> <span class="var-type">{type}</span>' \
                     ' <a class="tag-link" href="#{value}">#{value}</a></div>'

TAG_INVALID_LINK_TPL = '<div class="dxf-tag"><span class="tag-code">{code}</span> <span class="var-type">{type}</span>' \
                       ' <a class="tag-link" href="#{value}">#{value}  [does not exist]</a></div>'

MARKER_TPL = '<div class="tag-group-marker">{tag}</div>'
CONTROL_TPL = '<div class="tag-ctrl-marker">{tag}</div>'

# Links
SECTION_LINKS_TPL = '<div class="button-bar">{buttons}</div>\n'
REF_LINK_TPL = '<a class="dxf-ref-link" href={target} target="_blank" ' \
               'title="Link to DXF-Reference provided by Autodesk®.">{name}</a>'
BUTTON_BAR_TPL = '<div class="button-bar">{content}</div>'
BUTTON_TPL = '<a class="link-button" href="#{target}">{name}</a>'

MAX_STR_LEN = 100


def build_ref_link_button(name: str) -> str:
    """Create a link-button for element *name* to the DXF reference.
    """
    link = get_reference_link(name)
    return REF_LINK_TPL.format(target=link, name=name)


TAG_TYPES = {
    int: '<int>',
    float: '<float>',
    str: '<str>',
}


def tag_type_str(code: int) -> str:
    if code in GROUP_MARKERS:
        return '<ctrl>'
    elif code in HEX_HANDLE_CODES:
        return '<hex>'
    elif is_point_code(code):
        return '<point>'
    elif is_binary_data(code):
        return '<bin>'
    else:
        return TAG_TYPES[tag_type(code)]


def with_bitmask(value: int) -> str:
    return "{0}, b{0:08b}".format(int(value))


class DXF2HtmlConverter:
    def __init__(self, drawing: 'Drawing'):
        self.drawing = drawing
        self.entitydb = drawing.entitydb
        self.section_names_in_write_order = self._section_names_in_write_order()
        self.existing_pointers = self.collect_all_pointers()

    def _section_names_in_write_order(self) -> Sequence[str]:
        sections = self.drawing.sections
        write_order = list(name for name in KNOWN_SECTIONS if name in sections)
        write_order.extend(frozenset(sections.names()) - frozenset(KNOWN_SECTIONS))
        return write_order

    def dxf2html(self) -> str:
        """Creates a structured HTML view of the DXF tags - not a CAD drawing!
        """

        def get_name() -> str:
            if self.drawing.filename is None:
                return "unknown"
            else:
                filename = os.path.basename(self.drawing.filename)
                return os.path.splitext(filename)[0]

        template = load_resource('dxfpp.html')
        return template.format(
            name=get_name(),
            css=load_resource('dxfpp.css'),
            javascript=load_resource('dxfpp.js'),
            dxf_file=self.sections2html(),
            section_links=self.sections_link_bar(),
        )

    def sections2html(self) -> str:
        """Creates a <div> container of all DXF sections.
        """
        sections_html = []
        sections = self.drawing.sections
        for section_name in self.section_names_in_write_order:
            section = sections.get(section_name)
            if section is not None:
                section_template = self.create_section_html_template(section.name)
                sections_html.append(self.section2html(section, section_template))
        return ALL_SECTIONS_TPL.format(content="\n".join(sections_html))

    def create_section_html_template(self, name: str) -> str:
        """Creates a section template with buttons to the previous and next section.
        """

        def nav_targets() -> Tuple[str, str]:
            section_names = self.section_names_in_write_order
            index = section_names.index(name)
            prev_index = max(0, index - 1)
            succ_index = min(len(section_names) - 1, index + 1)
            return section_names[prev_index], section_names[succ_index]

        prev_id, next_id = nav_targets()
        prev_button = BUTTON_TPL.format(target=prev_id, name='previous')
        next_button = BUTTON_TPL.format(target=next_id, name='next')
        return COMMON_SECTION_TPL.format(
            ref_link=build_ref_link_button(name.upper()),
            this_id=name,
            prev=prev_button,
            next=next_button)

    def sections_link_bar(self) -> str:
        """Creates a <div> container as link bar to all DXF sections.
        """
        section_links = []
        for section_name in self.section_names_in_write_order:
            section_links.append(BUTTON_TPL.format(
                name=section_name.upper(),
                target=section_name
            ))
        return SECTION_LINKS_TPL.format(buttons=' \n'.join(section_links))

    def entities(self) -> Iterable['DXFEntity']:
        return iter(self.drawing.entities)

    def section2html(self, section, section_template: str) -> str:
        """Creates a <div> container of a specific DXF sections.
        """
        if section.name == 'HEADER':
            return section_template.format(content=self.hdrvars2html(section.hdrvars, section.custom_vars))
        elif section.name == 'ENTITIES':
            return section_template.format(content=self.entities2html(self.entities(), create_ref_links=True))
        elif section.name == 'CLASSES':
            return section_template.format(content=self.entities2html(section.classes.values()), create_ref_links=False,
                                           show_ref_status=False)
        elif section.name == 'OBJECTS':
            return section_template.format(content=self.entities2html(iter(section), create_ref_links=True,
                                                                      show_ref_status=True))
        elif section.name == 'TABLES':
            return section_template.format(content=self.tables2html(section))  # no iterator!
        elif section.name == 'BLOCKS':
            return section_template.format(content=self.blocks2html(iter(section)))
        else:
            return section_template.format(content=self.tags2html(section.tags()))

    @staticmethod
    def hdrvars2html(hdrvars, custom_vars) -> str:
        """DXF header section as <div> container.
        """

        def vartype(hdrvar) -> str:
            if is_point_code(hdrvar.code):
                dim = len(hdrvar.value) - 2
                return ("<point 2D>", "<point 3D>")[dim]
            else:
                return tag_type_str(hdrvar.code)

        varstrings = [
            HEADER_VAR_TPL.format(code=name, value=escape(str(hdrvar.value)), type=escape(vartype(hdrvar)))
            for name, hdrvar in hdrvars.items()
        ]

        custom_property_strings = [
            CUSTOM_VAR_TPL.format(tag=escape(str(tag)), value=escape(str(value)))
            for tag, value in custom_vars
        ]
        varstrings.extend(custom_property_strings)

        return HEADER_SECTION_TPL.format(content="\n".join(varstrings))

    def entities2html(self, entities: Iterable['DXFEntity'], create_ref_links=False, show_ref_status=False) -> str:
        """DXF entities as <div> container.
        """
        entity_strings = (self.entity2html(entity, create_ref_links, show_ref_status) for entity in entities)
        return ENTITIES_TPL.format("\n".join(entity_strings))

    def entity2html(self, entity: 'DXFEntity', create_ref_links=False, show_ref_status=False):
        """DXF entity as <div> container.
        """
        tags = entity.tags
        name = entity.dxftype()
        if create_ref_links:  # use entity name as link to the DXF reference
            name = build_ref_link_button(name)
        refs = ""
        if show_ref_status:
            handle = tags.get_handle()
            if handle not in self.existing_pointers:
                refs = '<div class="ref-no">[unreferenced]</div>'
            else:
                refs = self.pointers2html(self.existing_pointers[handle])
        return ENTITY_TPL.format(name=name, tags=self.tags2html(tags), references=refs)

    def pointers2html(self, pointers: Iterable[str]) -> str:
        pointers_str = ", ".join(('<a class="tag-link" href="#{value}">{value}</a>'.format(value=ptr) for ptr in
                                  sorted(pointers, key=lambda x: int(x, 16))))
        return '<div class="ref-yes"> referenced by: {pointers}</div>'.format(pointers=pointers_str)

    def tags2html(self, tags: 'ExtendedTags') -> str:
        """DXF tag list as <div> container.
        """

        def tag2html(tag: 'DXFTag') -> str:
            def trim_str(vstr: str) -> str:
                if len(vstr) > MAX_STR_LEN:
                    vstr = vstr[:(MAX_STR_LEN - 15)] + " ... " + vstr[-10:]
                return vstr

            if isinstance(tag, PackedTags):
                # inflate packed tags
                return ''.join(tag2html(tag) for tag in tag.dxftags())

            tpl = TAG_TPL
            if tag.code in HANDLE_CODES:  # is handle definition
                tpl = TAG_HANDLE_DEF_TPL
            elif is_pointer_code(tag.code):  # is handle link
                if tag.value in self.entitydb:
                    tpl = TAG_VALID_LINK_TPL
                else:
                    tpl = TAG_INVALID_LINK_TPL

            if tag.code in BINARY_FLAGS:
                vstr = with_bitmask(tag.value)
            else:
                if hasattr(tag, 'tostring'):
                    s = tag.tostring()
                else:
                    s = str(tag.value)
                vstr = trim_str(s)

            type_str = tag_type_str(tag.code)
            return tpl.format(code=tag.code, value=escape(vstr), type=escape(type_str))

        def group_marker(tag: 'DXFTag', tag_html: str) -> str:
            return tag_html if tag.code not in GROUP_MARKERS else MARKER_TPL.format(tag=tag_html)

        expanded_tags = self.expand_linked_tags(tags)
        tag_strings = (group_marker(tag, tag2html(tag)) for tag in expanded_tags)
        return TAG_LIST_TPL.format(content='\n'.join(tag_strings))

    def tables2html(self, tables: Iterable['Table']) -> str:
        """DXF tables section as <div> container.
        """
        navigation = self.create_table_navigation(tables)
        tables_html_strings = [self.table2html(table, navigation) for table in tables]
        return TABLES_SECTION_TPL.format(content='\n'.join(tables_html_strings))

    @staticmethod
    def create_table_navigation(table_section: Iterable['Table']) -> str:
        """Create a button bar with links to all DXF tables as <div> container.
        """
        buttons = []
        for table in table_section:
            name = table.name.upper()
            link = "{}-table".format(name)
            buttons.append(BUTTON_TPL.format(name=name, target=link))
        return BUTTON_BAR_TPL.format(content="\n".join(buttons))

    def table2html(self, table: 'Table', navigation='') -> str:
        """DXF table as <div> container.
        """
        header = ENTITY_TPL.format(name="TABLE HEADER", tags=self.tags2html(table._table_header), references="")
        entries = self.entities2html(table)
        table_name = table.name.upper()
        return TABLE_TPL.format(name=table_name, ref_link=build_ref_link_button(table_name), nav=navigation,
                                header=header, entries=entries)

    def expand_linked_tags(self, tags: 'ExtendedTags') -> 'DXFTag':
        while True:
            yield from tags
            if not hasattr(tags, 'link') or tags.link is None:
                return
            tags = self.entitydb[tags.link]

    def collect_all_pointers(self) -> Dict[str, Set[str]]:
        existing_pointers = dict()
        for tags in self.entitydb.values():
            handle = tags.get_handle()

            for tag in self.expand_linked_tags(tags):
                if is_pointer_code(tag.code):
                    pointers = existing_pointers.setdefault(tag.value, set())
                    pointers.add(handle)

        return existing_pointers

    def blocks2html(self, blocks: Iterable) -> str:
        """DXF blocks section as <div> container.
        """
        block_strings = (self.block2html(block) for block in blocks)
        return BLOCKS_SECTION_TPL.format(content='\n'.join(block_strings))

    def block2html(self, block_layout) -> str:
        """DXF block entity as <div> container.
        """
        block_html = self.entity2html(block_layout.block, create_ref_links=True)
        if block_layout.name.upper() not in ('*MODEL_SPACE', '*PAPER_SPACE'):
            entities_html = self.entities2html(iter(block_layout), create_ref_links=True)
        else:
            entities_html = ''
        endblk_html = self.entity2html(block_layout.endblk, create_ref_links=True)
        return BLOCK_TPL.format(name=block_layout.name, block=block_html, entities=entities_html, endblk=endblk_html)


def dxfpp(drawing: 'Drawing') -> str:
    """Creates a structured HTML view of the DXF tags - not a CAD drawing!
    """
    return DXF2HtmlConverter(drawing).dxf2html()


def load_resource(filename: str) -> str:
    """Load external resource files.
    """
    src_path = os.path.dirname(__file__)
    src = os.path.join(src_path, filename)
    try:
        with open(src, mode="rt", encoding='utf-8') as fp:
            resource = fp.read()
    except IOError:
        errmsg = "IOError: can not read file '{}'.".format(src)
        print(errmsg)
        resource = errmsg
    return resource
