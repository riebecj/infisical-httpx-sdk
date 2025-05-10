python_requirements(
    name="pyproject",
    source="pyproject.toml",
)

files(
    name="build_files",
    sources=["pyproject.toml", "README.md", "LICENSE"],
)

python_distribution(
    name="infisical-httpx-sdk",
    dependencies=["src/infisical", ":build_files"],
    provides=python_artifact(),
    generate_setup = False,
    repositories=[
        "https://upload.pypi.org/legacy/",
    ],
)
