# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import re

import yaml

TABLE_START = "<!-- NOTEBOOK_TABLE_START -->"
TABLE_END = "<!-- NOTEBOOK_TABLE_END -->"


def generate_table(meta_file="metadata/notebooks_meta.yaml"):
    with open(meta_file) as f:
        entries = yaml.safe_load(f)

    table = []
    header = (
        "| **Notebook title and documentation** | **Open in (Google Colab)** | "
        "**Additional resources** | **Discussion / Research Paper / Repository / Implementation** |\n"
        "| :---------------------------- | :-------------------------- | :------------------------ | :------------------------------------------------------------ |\n"
    )
    table.append(header)

    for entry in entries:
        doc_link = f'<a href="{entry["doc"]}">{entry["title"]}</a>'

        colab_link = (
            f'<a href="https://colab.research.google.com/github/ultralytics/{entry["colab"]}">'
            f'<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>'
        )

        youtube = entry.get("youtube")
        yt_badge = (
            (
                f'<a href="https://youtu.be/{youtube}">'
                f'<img src="https://img.shields.io/badge/Watch_on-YouTube-red?logo=youtube" alt="YouTube Video"></a>'
            )
            if youtube
            else "N/A"
        )

        discussion = f'<a href="{entry["discussion"]}">Discussion</a>'
        paper = entry.get("paper")
        paper_badge = ""
        if paper:
            if "arxiv.org" in paper:
                paper_id = paper.strip("/").split("/")[-1]
                paper_badge = (
                    f' • <a href="{paper}">'
                    f'<img src="https://img.shields.io/badge/arXiv-{paper_id}-B31B1B?logo=arxiv" alt="arXiv Paper"></a>'
                )
            else:
                paper_badge = f' • <a href="{paper}">Research Paper</a>'

        table.append(f"| {doc_link} | {colab_link} | {yt_badge} | {discussion}{paper_badge} |\n")

    return "".join(table)


def update_readme(readme_path="README.md", meta_path="metadata/notebooks_meta.yaml"):
    with open(readme_path) as f:
        content = f.read()

    table = generate_table(meta_path)

    new_content = re.sub(
        f"{TABLE_START}.*?{TABLE_END}",
        f"{TABLE_START}\n{table}\n{TABLE_END}",
        content,
        flags=re.DOTALL,
    )

    with open(readme_path, "w") as f:
        f.write(new_content)

    print("✅ README.md updated with badges!")


if __name__ == "__main__":
    update_readme()
