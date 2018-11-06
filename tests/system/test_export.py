import json
import yaml

from apmserver import ServerSetUpBaseTest


class SubCommandTest(ServerSetUpBaseTest):
    def wait_until_started(self):
        self.apmserver_proc.check_wait()

        # command and go test output is combined in log, pull out the command output
        log = self.get_log()
        pos = -1
        for _ in range(2):
            # export always uses \n, not os.linesep
            pos = log[:pos].rfind("\n")
        self.command_output = log[:pos]
        for trimmed in log[pos:].strip().splitlines():
            # ensure only skipping expected lines
            assert trimmed.split(None, 1)[0] in ("PASS", "coverage:"), trimmed


class ExportConfigDefaultTest(SubCommandTest):
    """
    Test export config subcommand.
    """

    def start_args(self):
        return {
            "extra_args": ["export", "config"],
            "logging_args": None,
        }

    def test_export_config(self):
        """
        Test export default config
        """
        config = yaml.load(self.command_output)
        # logging settings
        self.assertDictEqual(
            {"metrics": {"enabled": False}}, config["logging"]
        )

        # template settings
        self.assertDictEqual(
            {
                "template": {
                    "settings": {
                        "index": {
                            "codec": "best_compression",
                            "mapping": {
                                "total_fields": {"limit": 2000}
                            },
                            "number_of_shards": 1,
                        },
                    },
                },
            }, config["setup"])


class ExportConfigTest(SubCommandTest):
    """
    Test export config subcommand.
    """

    def start_args(self):
        return {
            "extra_args": ["export", "config",
                           "-E", "logging.metrics.enabled=true",
                           "-E", "setup.template.settings.index.mapping.total_fields.limit=5",
                           ],
            "logging_args": None,
        }

    def test_export_config(self):
        """
        Test export customized config
        """
        config = yaml.load(self.command_output)
        # logging settings
        self.assertDictEqual(
            {"metrics": {"enabled": True}}, config["logging"]
        )

        # template settings
        self.assertDictEqual(
            {
                "template": {
                    "settings": {
                        "index": {
                            "codec": "best_compression",
                            "mapping": {
                                "total_fields": {"limit": 5}
                            },
                            "number_of_shards": 1,
                        },
                    },
                },
            }, config["setup"])


class ExportTemplateDefaultTest(SubCommandTest):
    """
    Test export template subcommand.
    """

    def start_args(self):
        return {
            "extra_args": ["export", "template"],
            "logging_args": None,
        }

    def test_export_template(self):
        """
        Test export default template
        """
        template = yaml.load(self.command_output)
        settings = template["settings"]
        self.assertDictEqual(
            {
                "index": {
                    "codec": "best_compression",
                    "mapping": {
                        "total_fields": {"limit": 2000}
                    },
                    "number_of_routing_shards": 30,
                    "number_of_shards": 1,
                    "refresh_interval": "5s",
                },
            }, settings)


class ExportTemplateTest(SubCommandTest):
    """
    Test export template subcommand.
    """

    def start_args(self):
        return {
            "extra_args": ["export", "template",
                           "-E", "setup.template.settings.index.mapping.total_fields.limit=5",
                           ],
            "logging_args": None,
        }

    def test_export_template(self):
        """
        Test export customized template
        """
        template = yaml.load(self.command_output)
        settings = template["settings"]
        self.assertDictEqual(
            {
                "index": {
                    "codec": "best_compression",
                    "mapping": {
                        "total_fields": {"limit": 5}
                    },
                    "number_of_routing_shards": 30,
                    "number_of_shards": 1,
                    "refresh_interval": "5s",
                },
            }, settings)
