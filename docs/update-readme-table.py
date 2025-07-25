# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

# Programmatically updating the notebooks table within the README.md file.
# It ensures that any newly added or modified notebooks are automatically
# reflected in the documentation.

import yaml

with open("docs/notebooks-data.yml") as f:  # Load notebooks from YAML
    data = yaml.safe_load(f)

# Generate table
table = [
    "| Notebook | Open in colab / kaggle | Supporting materials | Discussion / arXiv / repository |",
    "|-------------------------|--------------|---------------|----------------------------|",
]

for nb in data["notebooks"]:
    # Use link if available, otherwise use GitHub file link
    if nb.get("link"):
        title_link = f'<a href="{nb["link"]}">{nb["title"]}</a>'
    else:
        github_url = f"https://github.com/ultralytics/notebooks/blob/main/{nb['file']}"
        title_link = f"[{nb['title']}]({github_url})"

    # Colab badge
    colab_url = f"https://colab.research.google.com/github/ultralytics/notebooks/blob/main/{nb['file']}"
    colab_badge = f'<a href="{colab_url}"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>'

    # Ultralytics blog
    blog_badge = ""
    if nb.get("blog"):
        blog_badge = f'<a href="{nb["blog"]}"><img src="https://github.com/user-attachments/assets/c60c360b-69de-4228-8545-f83096d5a9ce" alt="YouTube"></a>'

    # YouTube badge with custom image
    youtube_badge = ""
    if nb.get("youtube"):
        youtube_badge = f'<a href="{nb["youtube"]}"><img src="https://badges.aleen42.com/src/youtube.svg" alt="Watch on YouTube"></a>'

    # Kaggle badge
    kaggle_badge = ""
    if nb.get("kaggle"):
        kaggle_badge = f'<a href="{nb["kaggle"]}"><img src="https://kaggle.com/static/images/open-in-kaggle.svg" alt="Open in Kaggle"></a>'

    arxiv_badge = ""
    if nb.get("arxiv"):
        arxiv_id = nb["arxiv"].split("/")[
            -1
        ]  # Extract ID directly from the URL (e.g., https://arxiv.org/abs/1234.56789)
        arxiv_badge = f"[![arXiv](https://img.shields.io/badge/arXiv-{arxiv_id}-b31b1b.svg)]({nb['arxiv']})"

    discussion_badge = ""
    if nb.get("discussion"):
        discussion_badge = f'<a href="{nb["discussion"]}"><img src="https://github.com/user-attachments/assets/c4a1b18a-c4db-4bb7-b539-313e11171619" alt="Open in Discussion"></a>'

    github_badge = ""
    if nb.get("github"):
        github_badge = f'<a href="{nb["github"]}"><img src="https://badges.aleen42.com/src/github.svg" alt="GitHub Repo"></a>'

    dataset_badge = ""
    if nb.get("dataset"):
        dataset_badge = f'<a href="{nb["dataset"]}"><img src="https://github.com/user-attachments/assets/af3ad2cb-8541-440f-8aed-d93085d1f4e7" alt="Explore dataset"></a>'

    table.append(
        f"| {title_link} | "
        f'<div align="center">{colab_badge} {kaggle_badge}</div> | '
        f'<div align="center">{youtube_badge} {dataset_badge} {blog_badge}</div> | '
        f'<div align="center">{arxiv_badge} {discussion_badge} {github_badge}</div> |'
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
