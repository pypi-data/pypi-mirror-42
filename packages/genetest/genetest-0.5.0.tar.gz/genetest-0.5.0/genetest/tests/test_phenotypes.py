

# This file is part of genetest.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to Creative
# Commons, PO Box 1866, Mountain View, CA 94042, USA.


import os
import unittest
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

from ..phenotypes.core import PhenotypesContainer
from ..phenotypes.text import TextPhenotypes


__copyright__ = "Copyright 2016, Beaulieu-Saucier Pharmacogenomics Centre"
__license__ = "Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)"


class TestCore(unittest.TestCase):
    def test_get_phenotypes(self):
        """Tests that 'get_phenotypes' raises a NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            PhenotypesContainer().get_phenotypes()

    def test_close(self):
        """Tests that 'close' raises a NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            PhenotypesContainer().close()

    def test_get_sex_no_attribute(self):
        """Tests when the '_sex_column' attribute is missing."""
        with self.assertRaises(ValueError):
            PhenotypesContainer().get_sex()


class TestText(unittest.TestCase):
    def setUp(self):
        self.tmpdir = TemporaryDirectory(prefix="genetest_")

        # The phenotype file
        pheno_file = os.path.join(self.tmpdir.name, "pheno.txt")
        with open(pheno_file, "w") as f:
            print("sample", "V1", "V2", "V3", "sex", file=f)
            print("s1", "1", "1.2", "a", "0", file=f)
            print("s2", "234", "34.3", "sdc", "1", file=f)
            print("s3", "-999999", "", "csgb", "1", file=f)
            print("s4", "5463", "16.8", "999999", "0", file=f)
            print("s5", "2356", "574.8", "jyrhg", "0", file=f)
            print("s6", "", "567.2", "bvnchy", "1", file=f)
            print("s7", "57634", "3134.3", "", "0", file=f)
            print("s8", "346", "999999", "dfgfjgsd", "", file=f)
            print("s9", "34626", "3421.3", "fhyrj", "0", file=f)

        # The expected data frame
        self.expected_pheno = pd.DataFrame(
            [("s1", 1, 1.2, "a", 0),
             ("s2", 234, 34.3, "sdc", 1),
             ("s3", -999999, np.nan, "csgb", 1),
             ("s4", 5463, 16.8, "999999", 0),
             ("s5", 2356, 574.8, "jyrhg", 0),
             ("s6", np.nan, 567.2, "bvnchy", 1),
             ("s7", 57634, 3134.3, np.nan, 0),
             ("s8", 346, 999999, "dfgfjgsd", np.nan),
             ("s9", 34626, 3421.3, "fhyrj", 0)],
            columns=["sample", "V1", "V2", "V3", "sex"],
        ).set_index("sample")

        # The TextPhenotypes parameters
        self.parameters = dict(
            filename=pheno_file,
            sample_column="sample",
            field_separator=" ",
            missing_values=None,
            repeated_measurements=False,
            sex_column="sex",
        )

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_normal_functionality(self):
        """Tests normal functionality."""
        observed_pheno = TextPhenotypes(**self.parameters)

        self.assertTrue(
            self.expected_pheno.equals(observed_pheno.get_phenotypes())
        )
        self.assertEqual(9, observed_pheno.get_nb_samples())
        self.assertFalse(observed_pheno.is_repeated())

    def test_subset_phenotypes(self):
        """Tests asking for a subset of phenotypes."""
        container = TextPhenotypes(**self.parameters)

        subset = ("V1", "V3")
        expected = self.expected_pheno.loc[:, ["V1", "V3"]]
        self.assertTrue(
            expected.equals(container.get_phenotypes(subset))
        )

    def test_bad_subset_phenotypes(self):
        """Tests asking for a subset with unavailable phenotypes."""
        container = TextPhenotypes(**self.parameters)
        with self.assertRaises(KeyError):
            container.get_phenotypes(("V1", "V3", "VX"))

    def test_get_sex(self):
        """Tests asking for the sex series."""
        container = TextPhenotypes(**self.parameters)

        expected = self.expected_pheno.loc[:, "sex"]
        self.assertTrue(
            expected.equals(container.get_sex()),
        )

    def test_repeated_measurements(self):
        """Tests when there are repeated measurements available."""
        with open(self.parameters["filename"], "w") as f:
            print("sample", "Time", "V1", "V2", "V3", "sex", file=f)
            print("s1", "13", "1", "1.2", "a", "0", file=f)
            print("s1", "125", "1", "1.2", "a", "0", file=f)
            print("s1", "356", "1", "1.2", "a", "0", file=f)
            print("s2", "12", "5463", "16.8", "b", "1", file=f)
            print("s2", "34", "5463", "16.8", "b", "1", file=f)
            print("s2", "67", "5463", "16.8", "b", "1", file=f)
            print("s3", "1", "57634", "3134.3", "c", "", file=f)
            print("s3", "5", "57634", "3134.3", "c", "", file=f)
            print("s3", "10", "57634", "3134.3", "c", "", file=f)
            print("s4", "2", "57635", "3134.6", "b", "1", file=f)
            print("s4", "6", "57635", "3134.6", "b", "1", file=f)
            print("s4", "11", "57635", "3134.6", "b", "1", file=f)

        expected_pheno = pd.DataFrame(
            [("s1", 13, 1, 1.2, "a", 0),
             ("s1", 125, 1, 1.2, "a", 0),
             ("s1", 356, 1, 1.2, "a", 0),
             ("s2", 12, 5463, 16.8, "b", 1),
             ("s2", 34, 5463, 16.8, "b", 1),
             ("s2", 67, 5463, 16.8, "b", 1),
             ("s3", 1, 57634, 3134.3, "c", np.nan),
             ("s3", 5, 57634, 3134.3, "c", np.nan),
             ("s3", 10, 57634, 3134.3, "c", np.nan),
             ("s4", 2, 57635, 3134.6, "b", 1),
             ("s4", 6, 57635, 3134.6, "b", 1),
             ("s4", 11, 57635, 3134.6, "b", 1)],
            columns=["sample", "Time", "V1", "V2", "V3", "sex"],
        ).set_index("sample")

        # Changing the parameters
        self.parameters["repeated_measurements"] = True

        # Getting the observed phenotypes
        observed_pheno = TextPhenotypes(**self.parameters)

        # Checking the values
        self.assertTrue(expected_pheno.equals(observed_pheno.get_phenotypes()))
        self.assertEqual(4, observed_pheno.get_nb_samples())
        self.assertTrue(observed_pheno.is_repeated())

        # Checking the sex specifically
        expected_sex = pd.Series(
            [0, 1, np.nan, 1], index=["s1", "s2", "s3", "s4"],
        )
        self.assertTrue(expected_sex.equals(observed_pheno.get_sex()))

    def test_one_other_missing_value(self):
        """Tests when there are other missing values."""
        # Changing the parameters
        self.parameters["missing_values"] = "999999"

        # Getting the observed phenotypes
        observed_pheno = TextPhenotypes(**self.parameters).get_phenotypes()

        # Changing the expected phenotypes
        self.expected_pheno.loc["s4", "V3"] = np.nan
        self.expected_pheno.loc["s8", "V2"] = np.nan

        # Comparing
        self.assertTrue(self.expected_pheno.equals(observed_pheno))

    def test_multiple_missing_values(self):
        """Tests when there are multiple missing values."""
        # Changing the parameters
        self.parameters["missing_values"] = ["-999999", "999999"]

        # Getting the observed phenotypes
        observed_pheno = TextPhenotypes(**self.parameters).get_phenotypes()

        # Changing the expected phenotypes
        self.expected_pheno.loc["s3", "V1"] = np.nan
        self.expected_pheno.loc["s4", "V3"] = np.nan
        self.expected_pheno.loc["s8", "V2"] = np.nan

        # Comparing
        self.assertTrue(self.expected_pheno.equals(observed_pheno))

    def test_specific_column_missing_value(self):
        """Tests when there are specific missing values for some columns."""
        # Changing the parameters
        self.parameters["missing_values"] = {"V3": ["999999"]}

        # Getting the observed phenotypes
        observed_pheno = TextPhenotypes(**self.parameters).get_phenotypes()

        # Changing the expected phenotypes
        self.expected_pheno.loc["s4", "V3"] = np.nan

        # Comparing
        self.assertTrue(self.expected_pheno.equals(observed_pheno))

    def test_string_representation(self):
        """Checks the string representation."""
        with TextPhenotypes(**self.parameters) as text_pheno:
            self.assertEqual(
                "TextPhenotypes(9 samples, 4 variables)",
                str(text_pheno),
            )

    def test_invalid_sex(self):
        """Tests when other values than 0, 1 and NaN are in the sex column."""
        with open(self.parameters["filename"], "w") as f:
            print("sample", "V1", "V2", "V3", "sex", file=f)
            print("s1", "1", "1.2", "a", "0", file=f)
            print("s2", "234", "34.3", "sdc", "1", file=f)
            print("s3", "-999999", "", "csgb", "1", file=f)
            print("s4", "5463", "16.8", "999999", "2", file=f)
            print("s5", "2356", "574.8", "jyrhg", "0", file=f)
            print("s6", "", "567.2", "bvnchy", "1", file=f)
            print("s7", "57634", "3134.3", "", "0", file=f)
            print("s8", "346", "999999", "dfgfjgsd", "", file=f)
            print("s9", "34626", "3421.3", "fhyrj", "0", file=f)

        container = TextPhenotypes(**self.parameters)
        with self.assertRaises(ValueError):
            container.get_sex()

    def test_undefined_sex_column(self):
        """Tests when the sex column wasn't specified."""
        del self.parameters["sex_column"]

        container = TextPhenotypes(**self.parameters)
        with self.assertRaises(ValueError):
            container.get_sex()

    def test_duplicated_sex(self):
        """Tests when there are repeated (different) sex for a sample."""
        with open(self.parameters["filename"], "w") as f:
            print("sample", "Time", "V1", "V2", "V3", "sex", file=f)
            print("s1", "13", "1", "1.2", "a", "0", file=f)
            print("s1", "125", "1", "1.2", "a", "0", file=f)
            print("s1", "356", "1", "1.2", "a", "1", file=f)
            print("s2", "12", "5463", "16.8", "b", "1", file=f)
            print("s2", "34", "5463", "16.8", "b", "1", file=f)
            print("s2", "67", "5463", "16.8", "b", "", file=f)
            print("s3", "1", "57634", "3134.3", "c", "", file=f)
            print("s3", "5", "57634", "3134.3", "c", "", file=f)
            print("s3", "10", "57634", "3134.3", "c", "", file=f)

        # Changing the parameters
        self.parameters["repeated_measurements"] = True

        # Getting the observed phenotypes
        container = TextPhenotypes(**self.parameters)
        with self.assertRaises(ValueError) as cm:
            container.get_sex()
        self.assertEqual(
            str(cm.exception), "Samples with duplicated different sex: s1,s2",
        )
