import os
import json
from ._helpers import AnalyzerHelpers, ReportingHelpers
from ._parser import SwiftFileParser
from ._metrics import Framework, Metrics
from functional import seq


class Inspector:
    def __init__(self, directory, artifacts, tests_default_suffixes, exclude_paths):
        self.exclude_paths = exclude_paths
        self.directory = directory
        self.artifacts = artifacts
        self.tests_default_suffixes = tests_default_suffixes
        self.frameworks = []
        self.report = None

    def analyze(self) -> bool:
        if self.directory is not None:
            # Initialize report
            self.__analyze_directory(self.directory, self.exclude_paths, self.tests_default_suffixes)
            if len(self.frameworks) > 0:
                self.report = self._generate_report()
                self._save_report(self.artifacts)
                return True
        return False

    def filtered_frameworks(self, is_test=False):
        return seq(self.frameworks) \
            .filter(lambda f: f.is_test_framework == is_test) \
            .list()

    def _generate_report(self):
        report = _Report()

        for f in sorted(self.frameworks, key=lambda fr: fr.name, reverse=False):
            analysis = self.__framework_analysis(f)
            if f.is_test_framework:
                report.tests_framework.append(analysis)
                report.test_framework_aggregate.append_framework(f)
            else:
                report.non_test_framework.append(analysis)
                report.non_test_framework_aggregate.append_framework(f)

        return report

    def _save_report(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, 'output.json'), 'w') as fp:
            json.dump(self.report.as_dict, fp, indent=4)

    # Analysis

    def __framework_analysis(self, framework):
        """
        :param framework: The framework to analyze
        :return: The architectural analysis of the framework
        """
        loc = framework.loc
        noc = framework.noc
        poc = Metrics.percentage_of_comments(framework.noc, framework.loc)
        analysis = Metrics.poc_analysis(poc)
        n_a = framework.number_of_interfaces
        n_c = framework.number_of_concrete_data_structures
        nom = framework.number_of_methods
        dependencies = Metrics.total_dependencies(framework)
        n_of_tests = framework.number_of_tests
        n_of_imports = framework.number_of_imports

        # Non-test framework analysis
        non_test_analysis = {}
        if not framework.is_test_framework:
            non_test_analysis["fan_in"] = Metrics.fan_in(framework, self.frameworks)
            non_test_analysis["fan_out"] = Metrics.fan_out(framework)
            i = Metrics.instability(framework, self.frameworks)
            a = Metrics.abstractness(framework)
            non_test_analysis["i"] = ReportingHelpers.decimal_format(i)
            non_test_analysis["a"] = ReportingHelpers.decimal_format(a)
            non_test_analysis["d_3"] = ReportingHelpers.decimal_format(
                Metrics.distance_main_sequence(framework, self.frameworks))
            analysis += Metrics.ia_analysis(i, a)

        base_analysis = {
            "loc": loc,
            "noc": noc,
            "poc": ReportingHelpers.decimal_format(poc),
            "n_a": n_a,
            "n_c": n_c,
            "nom": nom,
            "not": n_of_tests,
            "noi": n_of_imports,
            "analysis": analysis,
            "dependencies": dependencies,
        }

        return {
            framework.name: {**base_analysis, **non_test_analysis}
        }

    def instability(self, framework):
        return Metrics.instability(framework, self.frameworks)

    def abstractness(self, framework):
        return Metrics.abstractness(framework)

    # Directory inspection

    def __analyze_directory(self, directory, exclude_paths, tests_default_paths):
        for subdir, _, files in os.walk(directory):
            for file in files:
                if file.endswith(AnalyzerHelpers.SWIFT_FILE_EXTENSION) and \
                        not AnalyzerHelpers.is_path_in_list(subdir, exclude_paths):
                    full_path = os.path.join(subdir, file)
                    is_in_test_path = AnalyzerHelpers.is_path_in_list(subdir, tests_default_paths)
                    swift_file = SwiftFileParser(file=full_path, base_path=directory, is_test=is_in_test_path).parse()
                    self.__append_dependency(swift_file, is_in_test_path)
        self.__cleanup_external_dependencies()

    def __append_dependency(self, swift_file, is_in_test_path):
        framework = self.__get_or_create_framework(swift_file.framework_name)
        framework.number_of_files += 1
        framework.loc += swift_file.loc
        framework.noc += swift_file.n_of_comments
        framework.number_of_interfaces += len(swift_file.interfaces)
        framework.number_of_concrete_data_structures += len(swift_file.structs + swift_file.classes)
        framework.number_of_methods += len(swift_file.methods)
        framework.number_of_tests += len(swift_file.tests)
        # This covers the scenario where a test framework might contain no tests
        framework.is_test_framework = is_in_test_path

        for f in swift_file.imports:
            imported_framework = self.__get_or_create_framework(f)
            if imported_framework is None:
                imported_framework = Framework(f)
            framework.append_import(imported_framework)

    def __cleanup_external_dependencies(self):
        # It will remove external dependencies built as source
        self.frameworks = seq(self.frameworks) \
            .filter(lambda f: f.number_of_files > 0) \
            .list()

    def __get_or_create_framework(self, framework_name):
        framework = self.__get_framework(framework_name)
        if framework is None:
            # not found, create a new one
            framework = Framework(framework_name)
            self.frameworks.append(framework)
        return framework

    def __get_framework(self, name):
        for f in self.frameworks:
            if f.name == name:
                return f
        return None


# Report generation


class _AggregateData:
    def __init__(self, loc=0, noc=0, n_a=0, n_c=0, nom=0, n_o_t=0, n_o_i=0):
        self.loc = loc
        self.noc = noc
        self.n_a = n_a
        self.n_c = n_c
        self.nom = nom
        self.n_o_t = n_o_t
        self.n_o_i = n_o_i

    def append_framework(self, f: 'Framework'):
        self.loc += f.loc
        self.noc += f.noc
        self.n_a += f.number_of_interfaces
        self.n_c += f.number_of_concrete_data_structures
        self.nom += f.number_of_methods
        self.n_o_t += f.number_of_tests
        self.n_o_i += f.number_of_imports

    @property
    def poc(self):
        return Metrics.percentage_of_comments(self.noc, self.loc)

    @property
    def as_dict(self):
        return {
            "loc": self.loc,
            "noc": self.noc,
            "n_a": self.n_a,
            "n_c": self.n_c,
            "nom": self.nom,
            "not": self.n_o_t,
            "noi": self.n_o_i,
            "poc": ReportingHelpers.decimal_format(self.poc)
        }

    @staticmethod
    def merged_data(first, second):
        return _AggregateData(loc=first.loc + second.loc,
                              noc=first.noc + second.noc,
                              n_a=first.n_a + second.n_a,
                              n_c=first.n_c + second.n_c,
                              nom=first.nom + second.nom,
                              n_o_t=first.n_o_t + second.n_o_t,
                              n_o_i=first.n_o_i + second.n_o_i)


class _Report:
    def __init__(self):
        self.non_test_framework = list()
        self.tests_framework = list()
        self.non_test_framework_aggregate = _AggregateData()
        self.test_framework_aggregate = _AggregateData()
        # Constants for report
        self.non_test_frameworks_key = "non-test-frameworks"
        self.tests_frameworks_key = "tests-frameworks"
        self.aggregate_key = "aggregate"

    @property
    def as_dict(self):
        return {
            self.non_test_frameworks_key: self.non_test_framework,
            self.tests_frameworks_key: self.tests_framework,
            self.aggregate_key: {
                self.non_test_frameworks_key: self.non_test_framework_aggregate.as_dict,
                self.tests_frameworks_key: self.test_framework_aggregate.as_dict,
                "total": _AggregateData.merged_data(self.non_test_framework_aggregate,
                                                    self.test_framework_aggregate).as_dict
            }
        }
