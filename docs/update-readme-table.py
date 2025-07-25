# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

# This Python script is responsible for programmatically updating the notebooks
# table within the README.md file. It ensures that any newly added or modified
# notebooks are automatically reflected in the documentation, keeping the table
# accurate and up to date without requiring manual edits.

import yaml

with open("notebooks-data.yml") as f:  # Load notebooks from YAML
    data = yaml.safe_load(f)

# Generate table
table = [
    "| Title and Documentation | Google Colab / Kaggle | YouTube Video | Resources / Discussion / Research Paper |",
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

    # YouTube badge with custom image
    youtube_badge = ""
    if nb.get("youtube"):
        youtube_badge = f'<a href="{nb["youtube"]}"><center><img width=30% src="https://raw.githubusercontent.com/ultralytics/assets/main/social/logo-social-youtube-rect.png" alt="Ultralytics Youtube Video"></center></a>'

    discussion = nb.get("discussion", "")

    table.append(f"| {title_link} | {colab_badge} | {youtube_badge} | {discussion} |")

table_md = "\n".join(table)
with open("README.md") as f:  # Update README
    readme = f.read()

start = readme.find("<!-- TABLE_START -->")
end = readme.find("<!-- TABLE_END -->")

if start != -1 and end != -1:
    new_readme = readme[: start + 20] + "\n\n" + table_md + "\n\n" + readme[end:]

    with open("README.md", "w") as f:
        f.write(new_readme)

    print(f"✅ Updated table with {len(data['notebooks'])} notebooks")
else:
    print("❌ Add <!-- TABLE_START --> and <!-- TABLE_END --> markers to README.md")
