

# This file is part of genetest.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to Creative
# Commons, PO Box 1866, Mountain View, CA 94042, USA.


import unittest

import numpy as np
import pandas as pd
from scipy.stats import binom

from geneparse import parsers

from .. import modelspec as spec
from ..phenotypes.dummy import _DummyPhenotypes
from ..statistics.models.linear import StatsLinear


__copyright__ = "Copyright 2016, Beaulieu-Saucier Pharmacogenomics Centre"
__license__ = "Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)"


class TestGrammar(unittest.TestCase):
    """Tests the grammar for the ModelSpec class."""
    @classmethod
    def setUpClass(cls):
        # Creating random data
        cls.data = pd.DataFrame(
            dict(
                pheno=np.random.randint(1, 100, 100),
                var1=np.random.randint(1, 100, 100),
                var2=np.random.rand(100),
                var3=["x{}".format(i) for i in np.random.randint(0, 3, 100)],
                var4=["y{}".format(i) for i in np.random.randint(0, 2, 100)],
                var5=np.random.randint(0, 4, 100),
                snp=binom.rvs(2, 0.3, size=100),
            ),
            index=["sample_{}".format(i+1) for i in range(100)],
        )

        # Changing one factor to categorical data
        cls.data.loc[:, "var5"] = cls.data.var5.astype("category")

        # Creating the dummy phenotype container
        phenotypes = ["pheno"] + ["var{}".format(i+1) for i in range(5)]
        cls.phenotypes = _DummyPhenotypes()
        cls.phenotypes.data = cls.data[phenotypes].copy()

        # Creating the dummy genotype container
        map_info = pd.DataFrame(
            {"chrom": ["3"],
             "pos": [1234],
             "a1": ["T"],
             "a2": ["C"]},
            index=["snp"],
        )
        cls.genotypes = parsers["dataframe"](
            dataframe=cls.data[["snp"]].copy(),
            map_info=map_info,
        )

    def setUp(self):
        # Resetting the model specification
        spec._reset()

        # Reordering the columns and the rows of the phenotype data frame
        self.phenotypes.data = self.phenotypes.data.iloc[
            np.random.permutation(self.phenotypes.data.shape[0]),
            np.random.permutation(self.phenotypes.data.shape[1])
        ]

    def test_simple_formula(self):
        """Tests a simple ModelSpec object."""
        # Parsing the formula and removing the conditions
        model = spec.parse_formula("pheno ~ g(snp) + var1 + var2")
        model["test"] = StatsLinear
        del model["conditions"]

        # Creating the model
        modelspec = spec.ModelSpec(**model)

        # Gathering the observed matrix
        matrix = modelspec.create_data_matrix(
            self.phenotypes, self.genotypes,
        )

        # Checking the shape of the matrix
        self.assertEqual((self.data.shape[0], 5), matrix.shape,
                         "The observed matrix is not of the right shape")

        # Checking the intercept
        self.assertEqual([1], matrix.intercept.unique().tolist(),
                         "The intercept is not as expected")

        # Checking the outcome
        outcome_col = spec.phenotypes.pheno.id
        outcomes = matrix.loc[self.data.index, outcome_col]
        self.assertTrue(outcomes.equals(self.data.pheno),
                        "The outcomes are not as expected")

        # Checking the predictors
        predictors = [spec.genotypes.snp, spec.phenotypes.var1,
                      spec.phenotypes.var2]
        translations = modelspec.get_translations()
        for predictor in predictors:
            # Getting the name of the predictor
            name = translations[predictor.id]

            # Comparing the values
            np.testing.assert_array_equal(
                matrix.loc[self.data.index, predictor.id].values,
                self.data[name].values,
                err_msg="The predictor '{}' is not as expected".format(name),
            )

    def test_pow(self):
        """Tests a power transformation."""
        # Parsing the formula and removing the conditions
        model = spec.parse_formula("pheno ~ g(snp) + pow(var1, 4)")
        model["test"] = StatsLinear
        del model["conditions"]

        # Creating the model
        modelspec = spec.ModelSpec(**model)

        # Gathering the observed matrix
        matrix = modelspec.create_data_matrix(
            self.phenotypes, self.genotypes,
        )

        # Checking the shape of the matrix
        self.assertEqual((self.data.shape[0], 4), matrix.shape,
                         "The observed matrix is not of the right shape")

        # Checking the intercept
        self.assertEqual([1], matrix.intercept.unique().tolist(),
                         "The intercept is not as expected")

        # Checking the outcome
        outcome_col = spec.phenotypes.pheno.id
        outcomes = matrix.loc[self.data.index, outcome_col]
        self.assertTrue(outcomes.equals(self.data.pheno),
                        "The outcomes are not as expected")

        # Checking the predictors
        predictors = [spec.genotypes.snp, spec.pow(spec.phenotypes.var1, 4)]
        for predictor, power, name in zip(predictors, (1, 4), ("snp", "var1")):
            # Comparing the values
            np.testing.assert_array_equal(
                matrix.loc[self.data.index, predictor.id].values,
                self.data[name].values**power,
                err_msg="The predictor '{}**{}' is not as "
                        "expected".format(name, power),
            )

    def test_log(self):
        """Tests log transformations (log10 and ln)."""
        # Parsing the formula and removing the conditions
        model = spec.parse_formula(
            "pheno ~ g(snp) + var1 + log10(var1) + ln(var1)"
        )
        model["test"] = StatsLinear
        del model["conditions"]

        # Creating the model
        modelspec = spec.ModelSpec(**model)

        # Gathering the observed matrix
        matrix = modelspec.create_data_matrix(
            self.phenotypes, self.genotypes,
        )

        # Checking the shape of the matrix
        self.assertEqual((self.data.shape[0], 6), matrix.shape,
                         "The observed matrix is not of the right shape")

        # Checking the intercept
        self.assertEqual([1], matrix.intercept.unique().tolist(),
                         "The intercept is not as expected")

        # Checking the outcome
        outcome_col = spec.phenotypes.pheno.id
        outcomes = matrix.loc[self.data.index, outcome_col]
        self.assertTrue(outcomes.equals(self.data.pheno),
                        "The outcomes are not as expected")

        # Checking the predictors
        translations = modelspec.get_translations()
        for predictor in (spec.genotypes.snp, spec.phenotypes.var1):
            # Getting the name of the predictor
            name = translations[predictor.id]

            # Comparing the values
            np.testing.assert_array_equal(
                matrix.loc[self.data.index, predictor.id].values,
                self.data[name].values,
                err_msg="The predictor '{}' is not as expected".format(name),
            )

        # Checking the log transform
        predictors = (spec.log10(spec.phenotypes.var1),
                      spec.ln(spec.phenotypes.var1))
        for predictor, transform, name in zip(predictors, (np.log10, np.log),
                                              ("var1", "var1")):
            # Comparing the values
            np.testing.assert_array_equal(
                matrix.loc[self.data.index, predictor.id].values,
                transform(self.data[name].values),
                err_msg="The predictor '{}({})' is not as "
                        "expected".format(transform.__name__, name),
            )

    def test_encode_factor(self):
        """Tests with factor."""
        # Parsing the formula and removing the conditions
        model = spec.parse_formula(
            "pheno ~ factor(var3) + factor(var4) + factor(var5)"
        )
        model["test"] = StatsLinear
        del model["conditions"]

        # Creating the model
        modelspec = spec.ModelSpec(**model)

        # Gathering the observed matrix
        matrix = modelspec.create_data_matrix(
            self.phenotypes, self.genotypes,
        )

        # Checking the shape of the matrix
        self.assertEqual((self.data.shape[0], 8), matrix.shape,
                         "The observed matrix is not of the right shape")

        # Checking the intercept
        self.assertEqual([1], matrix.intercept.unique().tolist(),
                         "The intercept is not as expected")

        # Checking the outcome
        outcome_col = spec.phenotypes.pheno.id
        outcomes = matrix.loc[self.data.index, outcome_col]
        self.assertTrue(outcomes.equals(self.data.pheno),
                        "The outcomes are not as expected")

        # Checking the factors
        var_names = ("var3", "var4", "var5")
        predictor_zipped = zip(
            tuple(spec.factor(spec.phenotypes[p]) for p in var_names),
            var_names,
            (("x1", "x2"), ("y1", ), (1, 2, 3)),
        )
        for predictor, name, levels in predictor_zipped:
            for level in levels:
                # Getting the name of the column containing the level data
                matrix_col = "{}:level.{}".format(predictor.id, level)

                # Comparing the results
                np.testing.assert_array_equal(
                    matrix.loc[self.data.index, matrix_col].values,
                    (self.data[name] == level).astype(float).values,
                    err_msg="The predictor '{}' (level '{}') is not as "
                            "expected".format(name, level),
                )

    def test_simple_interaction(self):
        """Tests simple interaction."""
        # Parsing the formula and removing the conditions
        model = spec.parse_formula(
            "pheno ~ g(snp) + var1 + g(snp)*var1"
        )
        model["test"] = StatsLinear
        del model["conditions"]

        # Creating the model
        modelspec = spec.ModelSpec(**model)

        # Gathering the observed matrix
        matrix = modelspec.create_data_matrix(
            self.phenotypes, self.genotypes,
        )

        # Checking the shape of the matrix
        self.assertEqual((self.data.shape[0], 5), matrix.shape,
                         "The observed matrix is not of the right shape")

        # Checking the intercept
        self.assertEqual([1], matrix.intercept.unique().tolist(),
                         "The intercept is not as expected")

        # Checking the outcome
        outcome_col = spec.phenotypes.pheno.id
        outcomes = matrix.loc[self.data.index, outcome_col]
        self.assertTrue(outcomes.equals(self.data.pheno),
                        "The outcomes are not as expected")

        # Checking the predictors
        for predictor in (spec.genotypes.snp, spec.phenotypes.var1):
            # Getting the name of the predictor
            name = modelspec.get_translations()[predictor.id]

            # Comparing the values
            np.testing.assert_array_equal(
                matrix.loc[self.data.index, predictor.id].values,
                self.data[name].values,
                err_msg="The predictor '{}' is not as expected".format(name),
            )

        # Checking the interaction
        interaction = spec.interaction(spec.genotypes.snp,
                                       spec.phenotypes.var1)
        np.testing.assert_array_equal(
            matrix.loc[self.data.index, interaction.id].values,
            (self.data.snp * self.data.var1).values,
            err_msg="The interaction 'snp*var1' is not as expected",
        )

    def test_multiple_interaction(self):
        """Tests simple interaction."""
        # Parsing the formula and removing the conditions
        model = spec.parse_formula(
            "pheno ~ g(snp) + var1 + var2 + g(snp)*var1*var2"
        )
        model["test"] = StatsLinear
        del model["conditions"]

        # Creating the model
        modelspec = spec.ModelSpec(**model)

        # Gathering the observed matrix
        matrix = modelspec.create_data_matrix(
            self.phenotypes, self.genotypes,
        )

        # Checking the shape of the matrix
        self.assertEqual((self.data.shape[0], 6), matrix.shape,
                         "The observed matrix is not of the right shape")

        # Checking the intercept
        self.assertEqual([1], matrix.intercept.unique().tolist(),
                         "The intercept is not as expected")

        # Checking the outcome
        outcome_col = spec.phenotypes.pheno.id
        outcomes = matrix.loc[self.data.index, outcome_col]
        self.assertTrue(outcomes.equals(self.data.pheno),
                        "The outcomes are not as expected")

        # Checking the predictors
        predictors = (spec.genotypes.snp, spec.phenotypes.var1,
                      spec.phenotypes.var2)
        for predictor in predictors:
            # Getting the name of the predictor
            name = modelspec.get_translations()[predictor.id]

            # Comparing the values
            np.testing.assert_array_equal(
                matrix.loc[self.data.index, predictor.id].values,
                self.data[name].values,
                err_msg="The predictor '{}' is not as expected".format(name),
            )

        # Checking the interaction
        interaction = spec.interaction(
            spec.genotypes.snp, spec.phenotypes.var1, spec.phenotypes.var2,
        )
        np.testing.assert_array_equal(
            matrix.loc[self.data.index, interaction.id].values,
            (self.data.snp * self.data.var1 * self.data.var2).values,
            err_msg="The interaction 'snp*var1*var2' is not as expected",
        )

    def test_factor_interaction(self):
        """Tests interaction between a term and a factor."""
        # Parsing the formula and removing the conditions
        model = spec.parse_formula(
            "pheno ~ g(snp) + factor(var5) + g(snp)*factor(var5)"
        )
        model["test"] = StatsLinear
        del model["conditions"]

        # Creating the model
        modelspec = spec.ModelSpec(**model)

        # Gathering the observed matrix
        matrix = modelspec.create_data_matrix(
            self.phenotypes, self.genotypes,
        )

        # Checking the shape of the matrix
        self.assertEqual((self.data.shape[0], 9), matrix.shape,
                         "The observed matrix is not of the right shape")

        # Checking the intercept
        self.assertEqual([1], matrix.intercept.unique().tolist(),
                         "The intercept is not as expected")

        # Checking the outcome
        outcome_col = spec.phenotypes.pheno.id
        outcomes = matrix.loc[self.data.index, outcome_col]
        self.assertTrue(outcomes.equals(self.data.pheno),
                        "The outcomes are not as expected")

        # Checking the predictor
        np.testing.assert_array_equal(
            matrix.loc[self.data.index, spec.genotypes.snp.id].values,
            self.data.snp.values,
            err_msg="The predictor 'snp' is not as expected",
        )

        # For all level:
        factor = spec.factor(spec.phenotypes.var5)
        interaction = spec.interaction(spec.genotypes.snp, factor)
        for level in (1, 2, 3):
            # Creating the expected level
            expected_factor_values = (self.data.var5 == level).astype(float)

            # Checking the factor
            col = factor.id + ":level.{}".format(level)
            np.testing.assert_array_equal(
                matrix.loc[self.data.index, col].values,
                expected_factor_values.values,
                err_msg="The predictor 'var5' (level '{}') is not as "
                        "expected".format(level),
            )

            # Checking the interaction
            col = interaction.id + ":level.{}".format(level)
            np.testing.assert_array_equal(
                matrix.loc[self.data.index, col].values,
                (expected_factor_values * self.data.snp).values,
                err_msg="The interaction 'snp*var5' (var5 level '{}') is not "
                        "as expected".format(level),
            )

    def test_complex_interaction(self):
        """Tests a complex interaction between terms and factors."""
        # Parsing the formula and removing the conditions
        model = spec.parse_formula(
            "pheno ~ g(snp) + var2 + factor(var3) + factor(var4) + "
            "        factor(var5) + "
            "        g(snp)*var2*factor(var3)*factor(var4)*factor(var5)"
        )
        model["test"] = StatsLinear
        del model["conditions"]

        # Creating the model
        modelspec = spec.ModelSpec(**model)

        # Gathering the observed matrix
        matrix = modelspec.create_data_matrix(
            self.phenotypes, self.genotypes,
        )

        # Checking the shape of the matrix
        self.assertEqual((self.data.shape[0], 16), matrix.shape,
                         "The observed matrix is not of the right shape")

        # Checking the intercept
        self.assertEqual([1], matrix.intercept.unique().tolist(),
                         "The intercept is not as expected")

        # Checking the outcome
        outcome_col = spec.phenotypes.pheno.id
        outcomes = matrix.loc[self.data.index, outcome_col]
        self.assertTrue(outcomes.equals(self.data.pheno),
                        "The outcomes are not as expected")

        # Checking the predictors
        translations = modelspec.get_translations()
        for predictor in (spec.genotypes.snp, spec.phenotypes.var2):
            # Getting the name of the predictor
            name = translations[predictor.id]

            # Comparing the values
            np.testing.assert_array_equal(
                matrix.loc[self.data.index, predictor.id].values,
                self.data[name].values,
                err_msg="The predictor '{}' is not as expected".format(name),
            )

        # Checking the factors
        var_names = ("var3", "var4", "var5")
        predictor_zipped = zip(
            tuple(spec.factor(spec.phenotypes[name]) for name in var_names),
            var_names,
            (("x1", "x2"), ("y1", ), (1, 2, 3)),
        )
        for predictor, name, levels in predictor_zipped:
            for level in levels:
                # Getting the name of the column containing the level data
                matrix_col = "{}:level.{}".format(predictor.id, level)

                # Comparing the factor
                np.testing.assert_array_equal(
                    matrix.loc[self.data.index, matrix_col].values,
                    (self.data[name] == level).astype(float).values,
                    err_msg="The predictor '{}' (level '{}') is not as "
                            "expected".format(name, level),
                )

        # Checking the interaction
        interaction = spec.interaction(
            spec.genotypes.snp, spec.phenotypes.var2,
            spec.factor(spec.phenotypes.var3),
            spec.factor(spec.phenotypes.var4),
            spec.factor(spec.phenotypes.var5),
        )
        for var3_l in ("x1", "x2"):
            for var4_l in ("y1", ):
                for var5_l in (1, 2, 3):
                    # The expected factor values
                    expected_var3 = (self.data.var3 == var3_l).astype(float)
                    expected_var4 = (self.data.var4 == var4_l).astype(float)
                    expected_var5 = (self.data.var5 == var5_l).astype(float)

                    # The expected interaction
                    expected_interaction = (
                        self.data.snp * self.data.var2 * expected_var3 *
                        expected_var4 * expected_var5
                    )

                    # Checking the interaction
                    matrix_col = "{}:level.{}:level.{}:level.{}".format(
                        interaction.id, var3_l, var4_l, var5_l,
                    )
                    np.testing.assert_array_equal(
                        matrix.loc[self.data.index, matrix_col].values,
                        expected_interaction.values,
                        err_msg=(
                            "The interaction 'snp*var2*var3*var4*var5*' "
                            "(var3 level '{}', var4 level '{} and var5 "
                            "level '{}' is not as expected".format(
                                var3_l, var4_l, var5_l,
                            )
                        ),
                    )
