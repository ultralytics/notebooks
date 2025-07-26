# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

# This file updates the notebooks table within the README.md file. It ensures that any
# newly added or modified notebooks are automatically reflected in the documentation.

import yaml

with open("docs/notebooks-data.yml") as f:
    data = yaml.safe_load(f)

# Generate table with proper alignment
table = [
    "| Notebook | Open in colab / kaggle | Supporting materials | Documentation / arXiv / Repository |",
    "|:--------:|:----------------------:|:-------------------:|:-------------------------------:|",
]

for nb in data["notebooks"]:
    # Title link
    if nb.get("link"):
        title_link = f'<a href="{nb["link"]}">{nb["title"]}</a>'
    else:
        github_url = f"https://github.com/ultralytics/notebooks/blob/main/{nb['file']}"
        title_link = f"[{nb['title']}]({github_url})"

    # Generate all badges
    colab_badge = f"[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ultralytics/notebooks/blob/main/{nb['file']})"
    kaggle_badge = (
        f"[![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)]({nb['kaggle']})"
        if nb.get("kaggle")
        else None
    )
    youtube_badge = (
        f"[![Watch on YouTube](https://badges.aleen42.com/src/youtube.svg)]({nb['youtube']})"
        if nb.get("youtube")
        else None
    )
    dataset_badge = (
        f"[![Explore Dataset](https://img.shields.io/badge/Dataset-%23ff1b6c?logo=ultralytics)]({nb['dataset']})"
        if nb.get("dataset")
        else None
    )
    blog_badge = (
        f"[![Ultralytics Blog](https://github.com/user-attachments/assets/c60c360b-69de-4228-8545-f83096d5a9ce)]({nb['blog']})"
        if nb.get("blog")
        else None
    )
    arxiv_badge = (
        f"[![Read arXiv paper](https://img.shields.io/badge/arXiv-{nb['arxiv'].split('/')[-1]}-b31b1b.svg)]({nb['arxiv']})"
        if nb.get("arxiv")
        else None
    )
    discussion_badge = (
        f"[![Explore documentation](https://img.shields.io/badge/Documentation-111F68?logo=ultralytics)]({nb['discussion']})"
        if nb.get("discussion")
        else None
    )
    github_badge = (
        f"[![GitHub](https://badges.aleen42.com/src/github.svg)]({nb['github']})" if nb.get("github") else None
    )

    # Add row with proper centering
    table.append(
        f"| {title_link} | "
        f"{colab_badge, kaggle_badge} | "
        f"{youtube_badge, dataset_badge, blog_badge} | "
        f"{arxiv_badge, discussion_badge, github_badge} |"
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
