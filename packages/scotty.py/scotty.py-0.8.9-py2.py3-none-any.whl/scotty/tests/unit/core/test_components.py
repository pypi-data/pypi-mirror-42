import unittest

from scotty.core.components import Component


class CheckoutManagerTest(unittest.TestCase):
    """Testclass for checkout manager."""

    def test_generator_location(self):
        """Run test for generator location."""
        git_url = "git@gitlab.gwdg.de:repository.py.git"
        generator = "git:{}[master]".format(git_url)
        config = {
            "generator": generator
        }
        component = Component()
        component.config = config
        self.assertEqual(component.generator['location'], git_url)

    def test_generator_location_without_reference(self):
        """Run test for generator parameter location without reference."""
        git_url = "ssh://git@gitlab.gwdg.de/repository.py.git"
        generator = "git:{}".format(git_url)
        config = {
            "generator": generator
        }
        component = Component()
        component.config = config
        self.assertEqual(component.generator['location'], git_url)

    def test_generator_reference(self):
        """Run test for generator parameter with reference."""
        git_url = "git@gitlab.gwdg.de:repository.py.git"
        generator = "git:{}[master]".format(git_url)
        config = {
            "generator": generator
        }
        component = Component()
        component.config = config
        self.assertEqual(component.generator['reference'], "master")

    def test_generator_reference_noreference(self):
        """Run test for generator parameter with no reference."""
        git_url = "git@gitlab.gwdg.de:repository.py.git"
        generator = "git:{}".format(git_url)
        config = {
            "generator": generator
        }
        component = Component()
        component.config = config
        self.assertEqual(component.generator['reference'], None)

    def test_generator_type(self):
        """Run test for gernerator type in checkout."""
        git_url = "ssh://git@gitlab.gwdg.de/repository.py.git"
        generator = "git:{}[master]".format(git_url)
        config = {
            "generator": generator
        }
        component = Component()
        component.config = config
        self.assertEqual(component.generator['type'], "git")
