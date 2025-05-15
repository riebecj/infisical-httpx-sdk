import textwrap
from pathlib import Path

import mkdocs_gen_files
from handsdown.md_document import MDDocument
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
            output_path=source_path / "docs",
            source_paths=path_finder.glob("**/*.py"),
            project_name="infisical-httpx-sdk",
            source_code_url="https://github.com/riebecj/infisical-httpx-sdk/blob/main/",
            source_code_path="main",
        )

    def _mkdocs_write(self, doc: MDDocument, record: ModuleRecord, content: str) -> None:
        """Write the generated documentation to the output path."""
        write_path = doc.path.relative_to(self._output_path)
        with mkdocs_gen_files.open(write_path, "w") as f:
            f.write(content)
        print(f"Updated doc {write_path} for {record.source_path}")

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
                self._mkdocs_write(md_document, module_record, content)
            elif str(module_record.source_path).endswith("base.py"):
                content = textwrap.dedent(f"""
                # {module_record.title}

                ::: {module_record.import_string.value}
                """)
                self._mkdocs_write(md_document, module_record, content)
            else:
                print(f"Skipping {print_path(module_record.source_path)}")
        else:
            content = textwrap.dedent(f"""
            # {module_record.title}

            ::: {module_record.import_string.value}
            """)
            self._mkdocs_write(md_document, module_record, content)


index_header = textwrap.dedent(f"""---
hide:
    - navigation
---
                            
""")

def _include_extras(path: Path) -> None:
    with path.open("rt") as f:
        content = f.read()
    
    if path.name == "README.md":
        content = index_header + content

    with mkdocs_gen_files.open(path.name, "wt+") as f:
        f.write(content)

handsdown = MkdocstringsGenerator()
handsdown.generate_docs()
_include_extras(Path.cwd() / "stylesheet.css")
_include_extras(Path.cwd() / "README.md")
