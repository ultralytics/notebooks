# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

# Programmatically updating the notebooks table within the README.md file.
# It ensures that any newly added or modified notebooks are automatically
# reflected in the documentation.

import yaml

with open("docs/notebooks-data.yml") as f:  # Load notebooks from YAML
    data = yaml.safe_load(f)

# Generate table
table = [
    "| Notebook | Open in colab / kaggle | Supporting materials / blog / docs / video | Discussion / arXiv / repository / code |",
    "|--------|:-----------------------:|:--------------------:|:--------------------------------:|",
]

for nb in data["notebooks"]:
    # Title link
    if nb.get("link"):
        title_link = f'<a href="{nb["link"]}">{nb["title"]}</a>'
    else:
        github_url = f"https://github.com/ultralytics/notebooks/blob/main/{nb['file']}"
        title_link = f"[{nb['title']}]({github_url})"

    # Badges
    colab_badge = f'<a href="https://colab.research.google.com/github/ultralytics/notebooks/blob/main/{nb["file"]}"><img src="https://colab.research.google.com/assets/colab-badge.svg"></a>'
    kaggle_badge = (
        f'<a href="{nb.get("kaggle", "")}"><img src="https://kaggle.com/static/images/open-in-kaggle.svg"></a>'
        if nb.get("kaggle")
        else ""
    )

    youtube_badge = (
        f'<a href="{nb.get("youtube", "")}"><img src="https://badges.aleen42.com/src/youtube.svg"></a>'
        if nb.get("youtube")
        else ""
    )
    dataset_badge = (
        f'<a href="{nb.get("dataset", "")}"><img src="https://github.com/user-attachments/assets/73d3a0e3-99ff-421d-84cd-c8ad2585d1b0"></a>'
        if nb.get("dataset")
        else ""
    )
    blog_badge = (
        f'<a href="{nb.get("blog", "")}"><img src="https://github.com/user-attachments/assets/c60c360b-69de-4228-8545-f83096d5a9ce"></a>'
        if nb.get("blog")
        else ""
    )

    arxiv_badge = ""
    if nb.get("arxiv"):
        arxiv_id = nb["arxiv"].split("/")[-1]
        arxiv_badge = f"[![arXiv](https://img.shields.io/badge/arXiv-{arxiv_id}-b31b1b.svg)]({nb['arxiv']})"

    discussion_badge = (
        f'<a href="{nb.get("discussion", "")}"><img src="https://github.com/user-attachments/assets/c4a1b18a-c4db-4bb7-b539-313e11171619"></a>'
        if nb.get("discussion")
        else ""
    )
    github_badge = (
        f'<a href="{nb.get("github", "")}"><img src="https://badges.aleen42.com/src/github.svg"></a>'
        if nb.get("github")
        else ""
    )

    # Add row
    table.append(
        f"| {title_link} | "
        f"{colab_badge} {kaggle_badge} | "
        f"{youtube_badge} {dataset_badge} {blog_badge} | "
        f"{arxiv_badge} {discussion_badge} {github_badge} |"
    )

table_md = "\n".join(table)
with open("README.md") as f:  # Update README
    readme = f.read()

start = readme.find("<!-- TABLE_START -->")
end = readme.find("<!-- TABLE_END -->")

if start != -1 and end != -1:
    new_readme = readme[: start + 20] + "\n\n" + table_md + "\n\n" + readme[end:]

    with open("README.md", "w") as f:
        f.write(new_readme)

    print(f"✅ Updated table with {len(data['notebooks'])} notebooks.")
else:
    print("❌ Add <!-- TABLE_START --> and <!-- TABLE_END --> markers to README.md.")
