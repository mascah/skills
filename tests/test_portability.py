"""Exercise the published skill directory as the installation boundary."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]


class PortableSkills(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def validate_skill(self, skill):
        return subprocess.run([sys.executable, str(SOURCE / 'scripts/validate.py'),
                               '--skill', str(skill)], cwd=self.root,
                              capture_output=True, text=True)

    def test_each_skill_installs_alone(self):
        for source in sorted((SOURCE / 'skills').iterdir()):
            with self.subTest(skill=source.name):
                destination = self.root / 'installed' / source.name
                shutil.copytree(source, destination)
                result = self.validate_skill(destination)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn('1 skill; 0 errors', result.stdout)

    def test_link_to_existing_file_outside_skill_is_rejected(self):
        destination = self.root / 'skill'
        destination.mkdir()
        (self.root / 'external.md').write_text('# Existing but not shipped\n')
        (destination / 'SKILL.md').write_text('---\nname: skill\ndescription: Test fixture\n---\n[external](../external.md)\n')
        result = self.validate_skill(destination)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('outside skill', result.stdout)

    def test_symlink_entry_point_outside_skill_is_rejected(self):
        destination = self.root / 'skill'
        destination.mkdir()
        source = self.root / 'external.md'
        source.write_text('---\nname: skill\ndescription: Test fixture\n---\nBody\n')
        (destination / 'SKILL.md').symlink_to(source)
        result = self.validate_skill(destination)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('symlink', result.stdout)

    def test_generated_copy_drift_is_rejected(self):
        package = self.root / 'plugin'
        shutil.copytree(SOURCE, package, ignore=shutil.ignore_patterns('.git', '.claude', '__pycache__'))
        reference = package / 'skills/implement/references/discipline.md'
        self.assertTrue(reference.is_file(), 'bundled reference missing')
        reference.write_text(reference.read_text() + '\nStale manual edit.\n')
        result = subprocess.run([sys.executable, str(package / 'scripts/validate.py')],
                                cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('reference drift', result.stdout)

    def test_generation_is_idempotent_and_tracks_transitive_files(self):
        package = self.root / 'plugin'
        (package / 'references').mkdir(parents=True)
        (package / 'skills/example').mkdir(parents=True)
        (package / 'references/a.md').write_text('[detail][detail]\n\n[detail]: b.md\n')
        (package / 'references/b.md').write_text('# Detail\n')
        (package / 'skills/example/SKILL.md').write_text('[read](references/a.md)\n')
        script = SOURCE / 'scripts/bundle_references.py'
        self.assertTrue(script.exists(), 'bundler missing')
        for _ in range(2):
            subprocess.run([sys.executable, str(script), str(package)], check=True,
                           cwd=self.root, capture_output=True)
        self.assertEqual((package / 'skills/example/references/b.md').read_text(), '# Detail\n')
        (package / 'skills/example/SKILL.md').write_text('# No support now\n')
        subprocess.run([sys.executable, str(script), str(package)], check=True,
                       cwd=self.root, capture_output=True)
        self.assertFalse((package / 'skills/example/references/a.md').exists())

    def test_bundler_refuses_external_destination_symlink(self):
        package = self.root / 'plugin'
        (package / 'references').mkdir(parents=True)
        directory = package / 'skills/example/references'
        directory.mkdir(parents=True)
        (package / 'references/a.md').write_text('# New canonical\n')
        (directory.parent / 'SKILL.md').write_text('[read](references/a.md)\n')
        outside = self.root / 'user-owned.md'
        outside.write_text('# Preserve me\n')
        (directory / 'a.md').symlink_to(outside)
        result = subprocess.run([sys.executable, str(SOURCE / 'scripts/bundle_references.py'),
                                 str(package)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(outside.read_text(), '# Preserve me\n')


if __name__ == '__main__':
    unittest.main()
