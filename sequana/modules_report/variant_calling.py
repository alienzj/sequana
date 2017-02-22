# coding: utf-8
#
#  This file is part of Sequana software
#
#  Copyright (c) 2016 - Sequana Development Team
#
#  File author(s):
#      Dimitri Desvillechabrol <dimitri.desvillechabrol@pasteur.fr>,
#          <d.desvillechabrol@gmail.com>
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
"""Module to write variant calling report"""
import ast

import pandas as pd

from sequana.modules_report.base_module import SequanaBaseModule


class SequanaModule(SequanaBaseModule):
    """ Write HTML report of variant calling. This class takes a csv file
    generated by sequana_variant_filter.
    """
    def __init__(self, data):
        """
        """
        super().__init__()
        self.filename = data
        self.title = "Variant Calling Report"
        try:
            with open(self.filename, "r") as fp:
                line = fp.readline()
                if line.startswith("# sequana_variant_calling"):
                    string_dict = line.split(";")[-1].strip()
                    try:
                        self.filter_dict = ast.literal_eval(string_dict)
                    except ValueError:
                        self.filter_dict = None
                    self.df = pd.read_csv(fp)
        except FileNotFoundError:
            msg = ("The csv file is not present. Please, check if your"
                   " file is present.")
            raise FileNotFoundError(msg)
        self.create_report_content()
        self.create_html("variant_calling.html")

    def create_report_content(self):
        self.sections = list()

        if self.filter_dict:
            self.filters_information()
        self.variant_calling()

    def filters_information(self):
        """ Add information of filter.
        """
        self.sections.append({
            'name': "Filter Options",
            'anchor': 'filters_option',
            'content': (
                "<p>All filters parameters used is presented in this list:</p>"
                "\n<ul><li>freebayes_score: {freebayes_score}</li>\n"
                "<li>frequency: {frequency}</li>\n"
                "<li>min_depth: {min_depth}</li>\n"
                "<li>forward_depth: {forward_depth}</li>\n"
                "<li>reverse_depth: {reverse_depth}</li>\n"
                "<li>strand_ratio: {strand_ratio}</li></ul>\n"
                "Note:<ul><li>frequency: alternate allele / depth</li>\n"
                "<li>min_depth: minimum alternate allele present</li>\n"
                "<li>forward_depth: minimum alternate allele present on "
                "forward strand</li>\n"
                "<li>reverse_depth: minimum alternate allele present on "
                "reverse strand</li>\n"
                "<li>strand_ratio: alternate allele forward / (alternate "
                "allele forward + alternate allele reverse)</li>"
                "</ul>".format(**self.filter_dict))
            })

    def variant_calling(self):
        """ Variants detected section.
        """
        html_table = self.dataframe_to_html_table(self.df, {'index': False})
        nb_variants = len(self.df)
        csv_link = self.create_link('link', self.filename)
        vcf_link = self.create_link('here', 'test.vcf')
        self.sections.append({
            'name': "Variants detected",
            'anchor': 'basic_stats',
            'content': (
                "<p>This table present variant detected by freebayes after "
                "filtering. There are {0} variants detected. You can download "
                "the table as csv format on this {1} and the vcf file {2}."
                "</p>\n{3}\n<p>Note: the freebayes score can be understood as "
                "1 - P(locus is homozygous given the data)</p>".format(
                    nb_variants, csv_link, vcf_link, html_table))
        })
