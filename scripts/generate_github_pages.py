import shutil
import textwrap
from pathlib import Path

from handsdown.ast_parser.node_records.module_record import ModuleRecord
from handsdown.exceptions import LoaderError
from handsdown.generators.base import BaseGenerator
from handsdown.utils.path import print_path
from handsdown.utils.path_finder import PathFinder


class MkdocstringsGenerator(BaseGenerator):
    def __init__(self):
        source_path = Path.cwd()
        path_finder = PathFinder(source_path)
        super().__init__(
            input_path=source_path,
            output_path=source_path / "gh-pages",
            source_paths=path_finder.glob("**/*.py"),
            project_name="infisical-httpx-sdk",
            source_code_url="https://github.com/riebecj/infisical-httpx-sdk/blob/main/",
            source_code_path="main",
        )

    def _generate_doc(self, module_record: ModuleRecord) -> None:
        md_document = self.get_md_document(module_record)
        self._logger.debug(
            f"Generating doc {print_path(md_document.path)}" f" for {print_path(module_record.source_path)}",
        )
        try:
            self._loader.parse_module_record(module_record)
        except LoaderError as e:
            if self._raise_errors:
                raise

            self._logger.warning(f"Skipping: {e}")
            return

        md_document.source_code_url = self._get_source_code_url(module_record, md_document)

        resources_path = Path.cwd() / "src" / "infisical" / "resources"
        if (
            module_record.source_path.is_relative_to(resources_path)
            and module_record.source_path.parent != resources_path
        ):
            if str(module_record.source_path).endswith("__init__.py"):
                content = textwrap.dedent(f"""
                # {module_record.title}

                ## API

                ::: {module_record.import_string.value}.api

                ## Models

                ::: {module_record.import_string.value}.models
                """)
                if self._write_changed(md_document.path, content):
                    print(f"Updated doc {md_document.path} for {module_record.source_path}")
            elif str(module_record.source_path).endswith("base.py"):
                content = textwrap.dedent(f"""
                # {module_record.title}

                ::: {module_record.import_string.value}
                """)
                if self._write_changed(md_document.path, content):
                    print(f"Updated doc {print_path(md_document.path)} for {print_path(module_record.source_path)}")
            else:
                # import pdb; pdb.set_trace()
                print(f"Skipping {print_path(module_record.source_path)}")
        else:
            content = textwrap.dedent(f"""
            # {module_record.title}

            ::: {module_record.import_string.value}
            """)
            if self._write_changed(md_document.path, content):
                print(f"Updated doc {print_path(md_document.path)} for {print_path(module_record.source_path)}")


shutil.rmtree(Path.cwd() / "gh-pages", ignore_errors=True)
handsdown = MkdocstringsGenerator()
handsdown.generate_docs()
shutil.copyfile(
    Path.cwd() / "stylesheet.css",
    Path.cwd() / "gh-pages" / "stylesheet.css",
)
gh_pages_header = textwrap.dedent(f"""---
hide:
  - navigation
---

""")
with (Path.cwd() / "README.md").open("rt") as readme_file:
    content = readme_file.read()

with (Path.cwd() / "gh-pages" / "README.md").open("wt+") as docs_index:
    docs_index.write(gh_pages_header + content)
