from setuptools import setup, find_packages


info = {
	"name": "liberty.py",
	"version": "1.0.3",
	"github_page": "https://github.com/xXxCLOTIxXx/liberty",
	"download_link": "https://github.com/xXxCLOTIxXx/liberty/archive/refs/heads/main.zip",
	"license": "MIT",
	"author": "Xsarz",
	"author_email": "xsarzy@gmail.com",
	"description": "Library for creating web servers.",
	"long_description": None,
	"long_description_file": "README.md",
	"long_description_content_type": "text/markdown",
	"keywords": [
		"web",
		"server",
		"networks"
		"api",
		"python",
		"python3",
		"python3.x",
		"xsarz",
		"official"
	],

	"install_requires": [
	]

}


if info.get("long_description"):
	long_description=info.get("long_description")
else:
	with open(info.get("long_description_file"), "r") as file:
		long_description = file.read()

setup(
	name = info.get("name"),
	version = info.get("version"),
	url = info.get("github_page"),
	download_url = info.get("download_link"),
	license = info.get("license"),
	author = info.get("author"),
	author_email = info.get("author_email"),
	description = info.get("description"),
	long_description = long_description,
	long_description_content_type = info.get("long_description_content_type"),
	keywords = info.get("keywords"),
	install_requires = info.get("install_requires"),
	packages = find_packages()
)
