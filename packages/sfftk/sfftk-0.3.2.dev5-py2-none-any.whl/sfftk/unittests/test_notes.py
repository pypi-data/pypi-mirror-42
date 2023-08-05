#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for :py:mod:`sfftk.core.notes` package"""

from __future__ import division, print_function

import os
import shlex
import shutil
import sys
import unittest
from urllib import urlencode

import __init__ as tests
from .. import BASE_DIR
from .. import schema
from ..core import utils
from ..core.parser import parse_args
from ..notes import find, modify, view, RESOURCE_LIST

__author__ = "Paul K. Korir, PhD"
__email__ = "pkorir@ebi.ac.uk, paul.korir@gmail.com"
__date__ = "2017-05-15"


# :TODO: rewrite to use sfftk.notes.modify.SimpleNote


class TestNotesModifyExternalReference(unittest.TestCase):
    def test_ols(self):
        """Test that sfftk.notes.modify.ExternalReference object works correctly"""
        type_ = u'ncit'
        otherType = u'http://purl.obolibrary.org/obo/NCIT_C62195'
        value = u'NCIT_C62195'
        # likely to change
        label = u'Wild Type'
        description = u'The naturally-occurring, normal, non-mutated version of a gene or genome.'
        urlenc = urlencode({u'iri': otherType.encode(u'idna')})
        urlenc2 = urlencode({u'iri': urlenc.split(u'=')[1]})
        urlenc3 = urlenc2.split(u'=')[1].decode(u'utf-8')
        extRef = modify.ExternalReference(
            type_=type_,
            otherType=otherType,
            value=value,
        )
        self.assertEqual(extRef.type, type_)
        self.assertEqual(extRef.otherType, otherType)
        self.assertEqual(extRef.value, value)
        self.assertEqual(extRef.label, label)
        self.assertEqual(extRef.description,
                         description)
        self.assertItemsEqual(extRef._get_text(), [label, description])
        self.assertEqual(extRef.iri, urlenc3)

    def test_emdb(self):
        """Test that sfftk.notes.modify.ExternalReference object works correctly"""
        type_ = u'EMDB'
        otherType = u'https://www.ebi.ac.uk/pdbe/emdb/EMD-8654'
        value = u'EMD-8654'
        # likely to change
        label = u'EMD-8654'
        description = u'Zika virus-infected Vero E6 cell at 48 hpi: dual-axis tilt series tomogram from 3 serial sections'
        extRef = modify.ExternalReference(
            type_=type_,
            otherType=otherType,
            value=value,
        )
        self.assertEqual(extRef.type, type_)
        self.assertEqual(extRef.otherType, otherType)
        self.assertEqual(extRef.value, value)
        self.assertEqual(extRef.label, label)
        self.assertEqual(extRef.description,
                         description)
        self.assertItemsEqual(extRef._get_text(), [label, description])

    def test_pdb(self):
        """Test that sfftk.notes.modify.ExternalReference object works correctly"""
        type_ = u'PDB'
        otherType = u'https://www.ebi.ac.uk/pdbe/entry/pdb/4gzw'
        value = u'4gzw'
        # likely to change
        label = u'N2 neuraminidase D151G mutant of A/Tanzania/205/2010 H3N2 in complex with avian sialic acid receptor'
        description = u'H3N2 subtype'
        extRef = modify.ExternalReference(
            type_=type_,
            otherType=otherType,
            value=value,
        )
        self.assertEqual(extRef.type, type_)
        self.assertEqual(extRef.otherType, otherType)
        self.assertEqual(extRef.value, value)
        self.assertEqual(extRef.label, label)
        self.assertEqual(extRef.description,
                         description)
        self.assertItemsEqual(extRef._get_text(), [label, description])

    def test_uniprot(self):
        """Test that sfftk.notes.modify.ExternalReference object works correctly"""
        type_ = u'UniProt'
        otherType = u'https://www.uniprot.org/uniprot/A0A1Q8WSX6'
        value = u'A0A1Q8WSX6'
        # likely to change
        label = u'A0A1Q8WSX6_9ACTO'
        description = u'Type I-E CRISPR-associated protein Cas5/CasD (Organism: Actinomyces oris)'
        extRef = modify.ExternalReference(
            type_=type_,
            otherType=otherType,
            value=value,
        )
        self.assertEqual(extRef.type, type_)
        self.assertEqual(extRef.otherType, otherType)
        self.assertEqual(extRef.value, value)
        self.assertEqual(extRef.label, label)
        self.assertEqual(extRef.description,
                         description)
        self.assertItemsEqual(extRef._get_text(), [label, description])


class TestNotesFindSearchResource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_fn = os.path.join(BASE_DIR, 'sff.conf')

    def test_unknown_resource(self):
        """Test exception raised formed unknown resource"""
        with self.assertRaises(SystemExit):
            args, config = parse_args(shlex.split(
                'notes search --resource xxx "something" --config-path {}'.format(self.config_fn)
            ))

    def test_configs_attribute(self):
        """Test the value of the configs attribute"""
        args, configs = parse_args(shlex.split(
            'notes search --resource ols "mitochondria" --config-path {}'.format(self.config_fn)
        ))
        resource = find.SearchResource(args, configs)
        self.assertEqual(resource.configs, configs)

    def test_result_path(self):
        """Test result path attr"""
        args, configs = parse_args(shlex.split(
            "notes search -R ols 'mitochondria' --config-path {}".format(self.config_fn)
        ))
        resource = find.SearchResource(args, configs)
        self.assertEqual(resource.result_path, RESOURCE_LIST['ols']['result_path'])

    def test_result_count(self):
        """Test result_count attr"""
        args, configs = parse_args(shlex.split(
            "notes search -R ols 'mitochondria' --config-path {}".format(self.config_fn)
        ))
        resource = find.SearchResource(args, configs)
        self.assertEqual(resource.result_count, RESOURCE_LIST['ols']['result_count'])

    def test_format(self):
        """Test format attr"""
        args, configs = parse_args(shlex.split(
            "notes search -R ols 'mitochondria' --config-path {}".format(self.config_fn)
        ))
        resource = find.SearchResource(args, configs)
        self.assertEqual(resource.format, RESOURCE_LIST['ols']['format'])

    def test_response(self):
        """Test response attr"""
        args, configs = parse_args(shlex.split(
            "notes search -R ols 'mitochondria' --config-path {}".format(self.config_fn)
        ))
        resource = find.SearchResource(args, configs)
        self.assertIsNone(resource.response)
        resource.search()
        url = resource.get_url()
        print('url: ' + url, file=sys.stderr)
        import requests
        import json
        R = requests.get(url)
        resource_results = utils.get_path(json.loads(resource.response), resource.result_path)
        test_results = utils.get_path(json.loads(R.text), resource.result_path)
        self.assertItemsEqual(resource_results, test_results)

    def test_get_url_ols_list_ontologies(self):
        """Test url correctness for OLS"""
        resource_name = 'ols'
        args, configs = parse_args(shlex.split(
            "notes search -R {resource_name} 'mitochondria' -L --config-path {config_fn}".format(
                resource_name=resource_name,
                config_fn=self.config_fn,
            ),
        ))
        resource = find.SearchResource(args, configs)
        url = "{root_url}ontologies?size=1000".format(
            root_url=RESOURCE_LIST[resource_name]['root_url'],
        )
        self.assertEqual(resource.get_url(), url)

    def test_get_url_ols(self):
        """Test url correctness for OLS"""
        resource_name = 'ols'
        args, configs = parse_args(shlex.split(
            "notes search -R {resource_name} 'mitochondria' -O go -x -o --config-path {config_fn}".format(
                resource_name=resource_name,
                config_fn=self.config_fn,
            ),
        ))
        resource = find.SearchResource(args, configs)
        url = "{root_url}search?q={search_term}&start={start}&rows={rows}&ontology={ontology}&exact=on&obsoletes=on".format(
            root_url=RESOURCE_LIST[resource_name]['root_url'],
            search_term=args.search_term,
            start=args.start - 1,
            rows=args.rows,
            ontology=args.ontology,
        )
        self.assertEqual(resource.get_url(), url)

    def test_get_url_emdb(self):
        """Test url correctness for EMDB"""
        resource_name = 'emdb'
        args, configs = parse_args(shlex.split(
            "notes search -R {resource_name} 'mitochondria' --config-path {config_fn}".format(
                resource_name=resource_name,
                config_fn=self.config_fn,
            ),
        ))
        resource = find.SearchResource(args, configs)
        url = "{root_url}?q={search_term}&start={start}&rows={rows}".format(
            root_url=RESOURCE_LIST[resource_name]['root_url'],
            search_term=args.search_term,
            start=args.start,
            rows=args.rows,
        )
        self.assertEqual(resource.get_url(), url)

    def test_get_url_uniprot(self):
        """Test url correctness for UniProt"""
        resource_name = 'uniprot'
        args, configs = parse_args(shlex.split(
            "notes search -R {resource_name} 'mitochondria' --config-path {config_fn}".format(
                resource_name=resource_name,
                config_fn=self.config_fn,
            ),
        ))
        resource = find.SearchResource(args, configs)
        url = "{root_url}?query={search_term}&format=tab&offset={start}&limit={rows}&columns=id,entry_name,protein_names,organism".format(
            root_url=RESOURCE_LIST[resource_name]['root_url'],
            search_term=args.search_term,
            start=args.start,
            rows=args.rows,
        )
        self.assertEqual(resource.get_url(), url)

    def test_get_url_pdb(self):
        """Test url correctness for PDB"""
        resource_name = 'pdb'
        args, configs = parse_args(shlex.split(
            "notes search -R {resource_name} 'mitochondria' --config-path {config_fn}".format(
                resource_name=resource_name,
                config_fn=self.config_fn,
            ),
        ))
        resource = find.SearchResource(args, configs)
        url = "{root_url}?q={search_term}&wt=json&fl=pdb_id,title,organism_scientific_name&start={start}&rows={rows}".format(
            root_url=RESOURCE_LIST[resource_name]['root_url'],
            search_term=args.search_term,
            start=args.start,
            rows=args.rows,
        )
        self.assertEqual(resource.get_url(), url)


# class TestNotesFindSearchResource(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.config_fn = os.path.join(BASE_DIR, 'sff.conf')
#
#     def test_search_args_attr(self):
#         """Test that search_args attr works"""
#         args, configs = parse_args(shlex.split(
#             "notes search -R emdb mitochondria --config-path {}".format(self.config_fn)
#         ))
#         resource = find.SearchResource(args, configs)
#         self.assertEqual(resource.search_args, args)


class TestNotesFindTableField(unittest.TestCase):
    def test_init_name(self):
        """Test instantiation of TableField object"""
        with self.assertRaisesRegexp(ValueError,
                                     "key and text are mutually exclusive; only define one or none of them"):
            find.TableField('my-field', key='k', text='t')

    def test_init_width_type(self):
        """Test check on width type"""
        with self.assertRaisesRegexp(ValueError, "field width must be int or long"):
            find.TableField('my-field', width=1.3)

    def test_init_width_value(self):
        """Test check on width value"""
        with self.assertRaisesRegexp(ValueError, "field width must be greater than 0"):
            find.TableField('my-field', width=0)

    def test_init_pc_type(self):
        """Test pc type"""
        with self.assertRaises(ValueError):
            find.TableField('my-field', pc='1.3')
        with self.assertRaises(ValueError):
            find.TableField('my-field', pc=u'1.3')
        with self.assertRaises(ValueError):
            find.TableField('my-field', pc=list())
        with self.assertRaises(ValueError):
            find.TableField('my-field', pc=dict())
        with self.assertRaises(ValueError):
            find.TableField('my-field', pc=tuple())

    def test_init_pc_value(self):
        """Test pc value"""
        with self.assertRaises(ValueError):
            find.TableField('my-field', pc=-1)
        with self.assertRaises(ValueError):
            find.TableField('my-field', pc=100)
        self.assertIsInstance(find.TableField('my-field', pc=50), find.TableField)

    def test_init_justify(self):
        """Test value for justify"""
        self.assertIsInstance(find.TableField('my-field', text='t', justify='left'), find.TableField)
        self.assertIsInstance(find.TableField('my-field', text='t', justify='right'), find.TableField)
        self.assertIsInstance(find.TableField('my-field', text='t', justify='center'), find.TableField)


class TestNotes_view(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_fn = os.path.join(BASE_DIR, 'sff.conf')

    def setUp(self):
        self.segment_id = 15559
        self.sff_file = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')

    def test_list_default(self):
        """Test that we can view the list of segmentations with annotations"""
        args, configs = parse_args(shlex.split("notes list {} --config-path {}".format(
            self.sff_file,
            self.config_fn,
        )))
        status = view.list_notes(args, configs)
        # assertions
        self.assertEqual(status, 0)

    def test_long_list(self):
        """Test that we can long list (-l) the list of segmentations with annotations"""
        args, configs = parse_args(shlex.split("notes list -l {} --config-path {}".format(
            self.sff_file,
            self.config_fn,
        )))
        status = view.list_notes(args, configs)
        # assertions
        self.assertEqual(status, 0)

    def test_show_default(self):
        """Test that we can show annotations in a single segment"""
        args, configs = parse_args(shlex.split("notes show -i {} {} --config-path {}".format(
            self.segment_id,
            self.sff_file,
            self.config_fn,
        )))
        status = view.show_notes(args, configs)
        self.assertEqual(status, 0)

    def test_long_show(self):
        """Test that we can show in long format annotations in a single segment"""
        args, configs = parse_args(shlex.split("notes show -l -i {} {} --config-path {}".format(
            self.segment_id,
            self.sff_file,
            self.config_fn,
        )))
        status = view.show_notes(args, configs)
        self.assertEqual(status, 0)


class TestNotes_modify(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_fn = os.path.join(BASE_DIR, 'sff.conf')
        cls.sff_file = None
        cls.output = None
        cls.annotated_sff_file = None

    # test filetypeA to filetypeB
    def setUp(self):
        self.segment_id = 15559

    def _test_add(self):
        """Test that we can add a note"""
        segment_name = 'the segment name'
        desc = 'a short description'
        num = tests._random_integer()
        extref = ['lsfj', 'sljfs', 'ldjls']
        complexes = ['09ej', 'euoisd', 'busdif']
        macromolecules = ['xuidh', '29hf98e', 'ygce']
        cmd = shlex.split(
            "notes add -i {} -s '{}' -d '{}' -E {} -n {} -C {} -M {} {} --config-path {}".format(
                self.segment_id,
                segment_name,
                desc,
                " ".join(extref),
                num,
                ','.join(complexes),
                ','.join(macromolecules),
                self.sff_file,
                self.config_fn,
            )
        )
        args, configs = parse_args(cmd)
        status = modify.add_note(args, configs)
        seg = schema.SFFSegmentation(self.sff_file)
        segment = seg.segments.get_by_id(self.segment_id)
        self.assertEqual(status, 0)
        self.assertEqual(segment.biologicalAnnotation.description, desc)
        self.assertEqual(segment.biologicalAnnotation.numberOfInstances, num)
        self.assertEqual(segment.biologicalAnnotation.externalReferences[0].type, extref[0])
        self.assertEqual(segment.biologicalAnnotation.externalReferences[0].otherType, extref[1])
        self.assertEqual(segment.biologicalAnnotation.externalReferences[0].value, extref[2])
        self.assertEqual(segment.complexesAndMacromolecules.complexes[0], complexes[0])
        self.assertEqual(segment.complexesAndMacromolecules.complexes[1], complexes[1])
        self.assertEqual(segment.complexesAndMacromolecules.complexes[2], complexes[2])
        self.assertEqual(segment.complexesAndMacromolecules.macromolecules[0], macromolecules[0])
        self.assertEqual(segment.complexesAndMacromolecules.macromolecules[1], macromolecules[1])
        self.assertEqual(segment.complexesAndMacromolecules.macromolecules[2], macromolecules[2])

    def _test_edit(self):
        """Test that we can edit a note"""
        segment_name = "the segments name"
        desc = 'a short description'
        num = tests._random_integer()
        extref = ['lsfj', 'sljfs', 'ldjss']
        complexes = ['09ej', 'euoisd', 'busdif']
        macromolecules = ['xuidh', '29hf98e', 'ygce']
        # add
        cmd = shlex.split(
            "notes add -i {} -s '{}' -D '{}' -E {} -n {} -C {} -M {} {} --config-path {}".format(
                self.segment_id,
                segment_name,
                desc,
                " ".join(extref),
                num,
                ','.join(complexes),
                ','.join(macromolecules),
                self.sff_file,
                self.config_fn,
            )
        )
        args, configs = parse_args(cmd)
        modify.add_note(args, configs)
        segment_name1 = segment_name[::-1]
        desc1 = desc[::-1]
        num1 = tests._random_integer()
        extref1 = map(lambda e: e[::-1], extref)
        cmd1 = shlex.split(
            "notes edit -i {} -s '{}' -d '{}' -e 0 -E {} -n {} -c 1 -C {} -m 2 -M {} {} --config-path {}".format(
                self.segment_id,
                segment_name1,
                desc1,
                " ".join(extref1),
                num1,
                complexes[1][::-1],
                macromolecules[2][::-1],
                self.sff_file,
                self.config_fn,
            ))
        args1, configs = parse_args(cmd1)
        # edit
        status1 = modify.edit_note(args1, configs)
        seg = schema.SFFSegmentation(self.sff_file)
        segment = seg.segments.get_by_id(self.segment_id)
        self.assertEqual(status1, 0)
        self.assertEqual(segment.biologicalAnnotation.name, segment_name1)
        self.assertEqual(segment.biologicalAnnotation.description, desc1)
        self.assertEqual(segment.biologicalAnnotation.numberOfInstances, num1)
        self.assertEqual(segment.biologicalAnnotation.externalReferences[0].type, extref1[0])
        self.assertEqual(segment.biologicalAnnotation.externalReferences[0].otherType, extref1[1])
        self.assertEqual(segment.biologicalAnnotation.externalReferences[0].value, extref1[2])
        self.assertEqual(segment.complexesAndMacromolecules.complexes[1], complexes[1][::-1])
        self.assertEqual(segment.complexesAndMacromolecules.macromolecules[2], macromolecules[2][::-1])

    def _test_del(self):
        """Test that we can delete a note"""
        segment_name = 'the segment name'
        desc = 'a short description'
        num = tests._random_integer()
        extref = ['lsfj', 'sljfs', 'dsljfl']
        complexes = ['09ej', 'euoisd', 'busdif']
        macromolecules = ['xuidh', '29hf98e', 'ygce']
        cmd = shlex.split(
            "notes add -i {} -D '{}' -E {} -n {} -C {} -M {} {} --config-path {}".format(
                self.segment_id,
                desc,
                " ".join(extref),
                num,
                ','.join(complexes),
                ','.join(macromolecules),
                self.sff_file,
                self.config_fn,
            )
        )
        args, configs = parse_args(cmd)
        # add
        modify.add_note(args, configs)
        # delete
        cmd1 = shlex.split("notes del -i {} -D -e 0 -n -c 0 -m 1 {} --config-path {}".format(
            self.segment_id,
            self.sff_file,
            self.config_fn,
        ))
        args1, configs = parse_args(cmd1)
        status1 = modify.del_note(args1, configs)
        seg = schema.SFFSegmentation(self.sff_file)
        segment = seg.segments.get_by_id(self.segment_id)
        self.assertEqual(status1, 0)
        self.assertIsNone(segment.biologicalAnnotation.name)
        self.assertIsNone(segment.biologicalAnnotation.description)
        self.assertIsNone(segment.biologicalAnnotation.numberOfInstances)
        self.assertEqual(len(segment.biologicalAnnotation.externalReferences), 0)
        self.assertEqual(len(segment.complexesAndMacromolecules.complexes), 2)
        self.assertEqual(len(segment.complexesAndMacromolecules.macromolecules), 2)

    def _test_merge(self):
        """Test that we can merge notes"""
        segment_name = 'my very nice segment'
        desc = 'a short description'
        num = tests._random_integer()
        extref = ['lsfj', 'sljfs', 'ldjss']
        complexes = ['09ej', 'euoisd', 'busdif']
        macromolecules = ['xuidh', '29hf98e', 'ygce']
        # add
        cmd = shlex.split(
            "notes add -i {} -s '{}' -d '{}' -E {} -n {} -C {} -M {} {} --config-path {}".format(
                self.segment_id,
                segment_name,
                desc,
                " ".join(extref),
                num,
                ','.join(complexes),
                ','.join(macromolecules),
                self.sff_file,
                self.config_fn,
            )
        )
        args, configs = parse_args(cmd)
        status = modify.add_note(args, configs)
        self.assertEqual(status, 0)
        # merge
        cmd1 = shlex.split(
            'notes merge --source {source} {other} --output {output} --config-path {config_fn}'.format(
                source=self.sff_file,
                other=self.other,
                output=self.output,
                config_fn=self.config_fn,
            )
        )
        args1, configs1 = parse_args(cmd1)
        status1 = modify.merge(args1, configs1)
        self.assertEqual(status1, 0)
        source_seg = schema.SFFSegmentation(self.sff_file)
        output_seg = schema.SFFSegmentation(self.output)
        source_segment = source_seg.segments.get_by_id(self.segment_id)
        # print('description: ' + source_segment.biologicalAnnotation.description, file=sys.stderr)
        output_segment = output_seg.segments.get_by_id(self.segment_id)
        self.assertEqual(source_segment.biologicalAnnotation.name, segment_name)
        self.assertEqual(source_segment.biologicalAnnotation.description, desc)
        self.assertEqual(source_segment.biologicalAnnotation.description,
                         output_segment.biologicalAnnotation.description)
        self.assertEqual(source_segment.biologicalAnnotation.numberOfInstances, num)
        self.assertEqual(source_segment.biologicalAnnotation.numberOfInstances,
                         output_segment.biologicalAnnotation.numberOfInstances)
        self.assertEqual(source_segment.biologicalAnnotation.externalReferences[0].type, extref[0])
        self.assertEqual(source_segment.biologicalAnnotation.externalReferences[0].otherType, extref[1])
        self.assertEqual(source_segment.biologicalAnnotation.externalReferences[0].value, extref[2])
        self.assertEqual(source_segment.biologicalAnnotation.externalReferences[0].type,
                         output_segment.biologicalAnnotation.externalReferences[0].type)
        self.assertEqual(source_segment.complexesAndMacromolecules.complexes[0], complexes[0])
        self.assertEqual(source_segment.complexesAndMacromolecules.complexes[1], complexes[1])
        self.assertEqual(source_segment.complexesAndMacromolecules.complexes[2], complexes[2])
        self.assertEqual(source_segment.complexesAndMacromolecules.macromolecules[0], macromolecules[0])
        self.assertEqual(source_segment.complexesAndMacromolecules.macromolecules[1], macromolecules[1])
        self.assertEqual(source_segment.complexesAndMacromolecules.macromolecules[2], macromolecules[2])
        self.assertEqual(source_segment.complexesAndMacromolecules.complexes[0],
                         output_segment.complexesAndMacromolecules.complexes[0])
        self.assertEqual(source_segment.complexesAndMacromolecules.complexes[1],
                         output_segment.complexesAndMacromolecules.complexes[1])
        self.assertEqual(source_segment.complexesAndMacromolecules.complexes[2],
                         output_segment.complexesAndMacromolecules.complexes[2])
        self.assertEqual(source_segment.complexesAndMacromolecules.macromolecules[0],
                         output_segment.complexesAndMacromolecules.macromolecules[0])
        self.assertEqual(source_segment.complexesAndMacromolecules.macromolecules[1],
                         output_segment.complexesAndMacromolecules.macromolecules[1])
        self.assertEqual(source_segment.complexesAndMacromolecules.macromolecules[2],
                         output_segment.complexesAndMacromolecules.macromolecules[2])

    def _test_clear(self):
        """Test that we can clear notes"""
        segment_name = 'my very nice segment'
        desc = 'a short description'
        num = tests._random_integer()
        extref = ['lsfj', 'sljfs', 'ldjss']
        complexes = ['09ej', 'euoisd', 'busdif']
        macromolecules = ['xuidh', '29hf98e', 'ygce']
        # add
        cmd = shlex.split(
            "notes add -i {} -s '{}' -D '{}' -E {} -n {} -C {} -M {} {} --config-path {}".format(
                self.segment_id,
                segment_name,
                desc,
                " ".join(extref),
                num,
                ','.join(complexes),
                ','.join(macromolecules),
                self.sff_file,
                self.config_fn,
            )
        )
        args, configs = parse_args(cmd)
        status = modify.add_note(args, configs)
        self.assertEqual(status, 0)
        # clear
        cmd1 = shlex.split(
            'notes clear --all {} --config-path {config_fn}'.format(
                self.sff_file,
                config_fn=self.config_fn,
            )
        )
        args1, configs1 = parse_args(cmd1)
        status1 = modify.clear_notes(args1, configs1)
        self.assertEqual(status1, 0)
        seg = schema.SFFSegmentation(self.sff_file)
        segment = seg.segments.get_by_id(self.segment_id)
        self.assertEqual(len(segment.biologicalAnnotation.externalReferences), 0)

    def _test_copy(self):
        """Test that we can copy notes"""
        # we have an annotated EMDB-SFF file
        # make a copy of the file for the test
        annotated_sff_file = os.path.join(os.path.dirname(self.annotated_sff_file),
                                          'temp_' + os.path.basename(self.annotated_sff_file))
        shutil.copy2(self.annotated_sff_file, annotated_sff_file)
        # use the file copy
        # before copy
        seg = schema.SFFSegmentation(annotated_sff_file)
        source_segment = seg.segments.get_by_id(15559)
        # copy
        cmd = "notes copy -i 15559 -t 15578 {} --config-path {}".format(
            annotated_sff_file,
            self.config_fn
        )
        status1 = modify.copy_notes(*parse_args(cmd, use_shlex=True))
        # debug
        cmd2 = "notes list {} --config-path {}".format(annotated_sff_file, self.config_fn)
        view.list_notes(*parse_args(cmd2, use_shlex=True))
        self.assertEqual(status1, 0)

        copied_seg = schema.SFFSegmentation(annotated_sff_file)
        copied_segment = copied_seg.segments.get_by_id(15578)
        self.assertEqual(len(source_segment.biologicalAnnotation.externalReferences),
                         len(copied_segment.biologicalAnnotation.externalReferences))
        self.assertEqual(source_segment.biologicalAnnotation.externalReferences[0].type,
                         copied_segment.biologicalAnnotation.externalReferences[0].type)
        self.assertEqual(source_segment.biologicalAnnotation.externalReferences[0].otherType,
                         copied_segment.biologicalAnnotation.externalReferences[0].otherType)
        self.assertEqual(source_segment.biologicalAnnotation.externalReferences[0].value,
                         copied_segment.biologicalAnnotation.externalReferences[0].value)
        # # get rid of the copy
        os.remove(annotated_sff_file)


class TestNotes_modify_sff(TestNotes_modify):
    def setUp(self):
        super(TestNotes_modify_sff, self).setUp()
        self.sff_file = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.sff')
        self.other = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'other_emd_1014.sff')
        self.output = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'output_emd_1181.sff')
        self.annotated_sff_file = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'annotated_emd_1014.sff')

    def tearDown(self):
        seg = schema.SFFSegmentation(self.sff_file)
        # remove all annotations
        for segment in seg.segments:
            segment.biologicalAnnotation = schema.SFFBiologicalAnnotation()
            segment.complexesAndMacromolecules = schema.SFFComplexesAndMacromolecules()
        seg.export(self.sff_file)

    def test_add(self):
        super(TestNotes_modify_sff, self)._test_add()

    def test_edit(self):
        super(TestNotes_modify_sff, self)._test_edit()

    def test_del(self):
        super(TestNotes_modify_sff, self)._test_del()

    def test_merge(self):
        super(TestNotes_modify_sff, self)._test_merge()

    def test_clear(self):
        super(TestNotes_modify_sff, self)._test_clear()

    def test_copy(self):
        super(TestNotes_modify_sff, self)._test_copy()


# fixme: hff tests work but quadruple size of file


class TestNotes_modify_hff(TestNotes_modify):
    def setUp(self):
        super(TestNotes_modify_hff, self).setUp()
        self.sff_file = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.hff')
        self.other = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'other_emd_1014.hff')
        self.output = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'output_emd_1014.hff')
        self.annotated_sff_file = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'annotated_emd_1014.hff')

    def tearDown(self):
        seg = schema.SFFSegmentation(self.sff_file)
        # remove all annotations
        for segment in seg.segments:
            segment.biologicalAnnotation = schema.SFFBiologicalAnnotation()
            segment.complexesAndMacromolecules = schema.SFFComplexesAndMacromolecules()
        seg.export(self.sff_file)

    def test_add(self):
        super(TestNotes_modify_hff, self)._test_add()

    def test_edit(self):
        super(TestNotes_modify_hff, self)._test_edit()

    def test_del(self):
        super(TestNotes_modify_hff, self)._test_del()

    def test_clear(self):
        super(TestNotes_modify_hff, self)._test_clear()

    # fixme: can't figure out why this fails
    # def test_copy(self):
    #     super(TestNotes_modify_hff, self)._test_copy()


class TestNotes_modify_json(TestNotes_modify):
    def setUp(self):
        super(TestNotes_modify_json, self).setUp()
        self.sff_file = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'emd_1014.json')
        self.other = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'other_emd_1014.json')
        self.output = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'output_emd_1181.json')
        self.annotated_sff_file = os.path.join(tests.TEST_DATA_PATH, 'sff', 'v0.7', 'annotated_emd_1014.json')

    def tearDown(self):
        seg = schema.SFFSegmentation(self.sff_file)
        # remove all annotations
        for segment in seg.segments:
            segment.biologicalAnnotation = schema.SFFBiologicalAnnotation()
            segment.complexesAndMacromolecules = schema.SFFComplexesAndMacromolecules()
        seg.export(self.sff_file)

    def test_add(self):
        super(TestNotes_modify_json, self)._test_add()

    def test_edit(self):
        super(TestNotes_modify_json, self)._test_edit()

    def test_del(self):
        super(TestNotes_modify_json, self)._test_del()

    def test_merge(self):
        super(TestNotes_modify_json, self)._test_merge()

    def test_clear(self):
        super(TestNotes_modify_json, self)._test_clear()

    def test_copy(self):
        super(TestNotes_modify_json, self)._test_copy()


class TestNotes_find(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_fn = os.path.join(BASE_DIR, 'sff.conf')

    def test_search_default(self):
        """Test default search parameters"""
        args, configs = parse_args(shlex.split("notes search 'mitochondria' --config-path {}".format(self.config_fn)))
        resource = find.SearchResource(args, configs)
        try:
            results = resource.search()
            self.assertGreater(len(results), 0)
        except ValueError as v:
            print(str(v), file=sys.stderr)
            self.assertTrue(False)

    def test_search_no_results(self):
        """Test search that returns no results"""
        # I'm not sure when some biological entity with such a name will be discovered!
        args, configs = parse_args(
            shlex.split("notes search 'nothing' --exact --config-path {}".format(self.config_fn)))
        resource = find.SearchResource(args, configs)
        try:
            results = resource.search()
            self.assertEqual(len(results), 0)
        except ValueError as v:
            print(str(v), file=sys.stderr)
            self.assertTrue(False)

    def test_search_exact_result(self):
        """Test that we get an exact result
            
        NOTE: this test is likely to break as the ontologies get updated
        """
        # this usually returns a single result
        args, configs = parse_args(shlex.split(
            "notes search 'DNA replication licensing factor MCM6' --exact --config-path {}".format(self.config_fn)))
        resource = find.SearchResource(args, configs)
        results = resource.search()
        self.assertEqual(len(results), 2)  # funny!

    def test_search_ontology(self):
        """Test that we can search an ontology"""
        #  this search should bring at least one result
        args, configs = parse_args(
            shlex.split("notes search 'mitochondria' --exact -O omit --config-path {}".format(self.config_fn)))
        resource = find.SearchResource(args, configs)
        try:
            results = resource.search()
            self.assertGreaterEqual(len(results), 1)
        except ValueError as v:
            print(str(v), file=sys.stderr)
            self.assertTrue(False)

    def test_search_from_start(self):
        """Test that we can search from the starting index"""
        # this search usually has close to 1000 results; 100 is a reasonable start
        random_start = tests._random_integer(1, 970)
        args, configs = parse_args(shlex.split("notes search 'mitochondria' --start {} --config-path {}".format(
            random_start,
            self.config_fn,
        )))
        resource = find.SearchResource(args, configs)
        try:
            results = resource.search()
            self.assertGreaterEqual(results.structured_response['response']['start'], random_start - 1)
        except ValueError as v:
            print(str(v), file=sys.stderr)
            self.assertTrue(False)

    def test_search_result_rows(self):
        """Test that we get as many result rows as specified"""
        # this search usually has close to 1000 results; 100 is a reasonable start
        random_rows = tests._random_integer(10, 100)
        args, configs = parse_args(shlex.split("notes search 'mitochondria' --rows {} --config-path {}".format(
            random_rows,
            self.config_fn,
        )))
        resource = find.SearchResource(args, configs)
        try:
            results = resource.search()
            self.assertGreaterEqual(len(results), random_rows)
        except ValueError as v:
            print(str(v), file=sys.stderr)
            self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
