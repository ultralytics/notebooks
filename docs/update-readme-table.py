# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

# This file updates the notebooks table within the README.md file. It ensures that any
# newly added or modified notebooks are automatically reflected in the documentation.

import yaml

with open("docs/notebooks-data.yml") as f:
    data = yaml.safe_load(f)


def center_badges(*badges):
    """Center align badges, handling empty cells."""
    non_empty = [badge for badge in badges if badge.strip()]
    if not non_empty:
        return "<div align='center'>-</div>"
    return f"<div align='center'>{' '.join(non_empty)}</div>"


# Generate table with proper alignment
table = [
    "| Notebook | Open in colab / kaggle | Supporting materials | Discussion / arXiv / Repository |",
    "|:--------:|:----------------------:|:-------------------:|:-------------------------------:|",
]

for notebook in data["notebooks"]:
    # Title link
    if notebook.get("file"):
        title_link = f'<a href="{notebook["file"]}">{notebook["title"]}</a>'
    else:
        github_url = f"https://github.com/ultralytics/notebooks/blob/main/{notebook['file']}"
        title_link = f"[{notebook['title']}]({github_url})"

    # Generate all badges
    colab_url = f"https://colab.research.google.com/github/ultralytics/notebooks/blob/main/{notebook['file']}"
    colab_badge = f"[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})"
    
    kaggle_url = f"https://kaggle.com/kernels/welcome?src=https://github.com/ultralytics/notebooks/blob/main/{notebook['file']}"
    kaggle_badge = f"[![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)]({kaggle_url})"
    
    amazon_sagemaker_url = (
        f"https://studiolab.sagemaker.aws/import/github/ultralytics/notebooks/blob/main/{notebook['file']}"
    )
    amazon_sagemaker_badge = (
        f"[![Open in SageMaker Studio Lab](https://studiolab.sagemaker.aws/studiolab.svg)]({amazon_sagemaker_url})"
        if notebook.get("file")
        else ""
    )
    
    youtube_badge = (
        f"[![Watch on YouTube](https://badges.aleen42.com/src/youtube.svg)]({notebook['youtube']})"
        if notebook.get("youtube")
        else ""
    )
    dataset_badge = (
        f"[![Explore Dataset](https://img.shields.io/badge/Dataset-%23ff1b6c?logo=ultralytics)]({notebook['dataset']})"
        if notebook.get("dataset")
        else ""
    )
    blog_badge = (
        f"[![Ultralytics Blog](https://github.com/user-attachments/assets/c60c360b-69de-4228-8545-f83096d5a9ce)]({notebook['blog']})"
        if notebook.get("blog")
        else ""
    )
    arxiv_badge = (
        f"[![Read arXiv paper](https://img.shields.io/badge/arXiv-{notebook['arxiv'].split('/')[-1]}-b31b1b.svg)]({notebook['arxiv']})"
        if notebook.get("arxiv")
        else ""
    )
    documentation_badge = (
        f"[![Read Documentation](https://img.shields.io/badge/Documentation-042AFF?logo=ultralytics)]({notebook['documentation']})"
        if notebook.get("documentation")
        else ""
    )
    github_badge = f"[![GitHub](https://badges.aleen42.com/src/github.svg)]({notebook['github']})" if notebook.get("github") else ""

    # Add row with proper centering
    table.append(
        f"| {title_link} | "
        f"{center_badges(colab_badge, kaggle_badge, amazon_sagemaker_badge)} | "
        f"{center_badges(youtube_badge, dataset_badge, blog_badge)} | "
        f"{center_badges(arxiv_badge, documentation_badge, github_badge)} |"
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
