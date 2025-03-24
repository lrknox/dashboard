import requests
import re

# GitHub repository details
owner = "cass-community"
repo = "cass-community.github.io"
path = "_software"

# GitHub API URL to list contents of the directory
url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
#url = f"https://github.com/cass-community/cass-community.github.io/tree/main/_software"

# Function to get the content of a file from GitHub
def get_file_content(file_url):
    response = requests.get(file_url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Send a GET request to the GitHub API
response = requests.get(url)

#Check if the request was successful
if response.status_code == 200:
    label = 'label: Repository'
    contents = response.json()
    # Filter and list .md files
    md_files = [file for file in contents if file['name'].endswith('.md')]

    github_list = []
    gitlab_list = []
    for md_file in md_files:
        file_url = md_file['download_url']
        content = get_file_content(file_url)
        if content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if re.match(r"(.*)label: Repository(.*)", line):
                    # Skip the next line if it contains 'note:'
                    next_line_index = i + 1
                    if next_line_index < len(lines) and "note:" in lines[next_line_index]:
                        next_line_index += 1
                    # Find the first line matching 'url: https://github.com(.*)' after 'label: Repository'
                    for j in range(i + 1, len(lines)):
                        github_match = re.match(r"(.*)url: https://github.com(.*)", lines[j])
                        gitlab_match = re.match(r"(.*)url: https://gitlab.com(.*)", lines[j])
                        if github_match:
                            part_after_url = github_match.group(2).strip().lstrip('/').lower()
                            part_after_url = re.sub(r'\.git$', '', part_after_url)
                            if part_after_url.endswith('/'):
                                part_after_url = part_after_url[:-1]
                            github_list.append((part_after_url))
                            break
                        elif gitlab_match:
                            part_after_url = gitlab_match.group(2).strip().lstrip('/').lower()
                            part_after_url = re.sub(r'\.git$', '', part_after_url)
                            if part_after_url.endswith('/'):
                                part_after_url = part_after_url[:-1]
                            gitlab_list.append((part_after_url))
                            break
                
                    # Sort the lists alphabetically by part_after_url
                    github_list.sort(key=lambda x: x[0])
                    gitlab_list.sort(key=lambda x: x[0])

                    #github_set = set(sorted(github_list, key=lambda x: x[0]))
                    #gitlab_set = set(sorted(gitlab_list, key=lambda x: x[0]))

    # Print the results
    print("Lines matching 'https://github.com':")
    for part_after_url in github_list:
        print(f"\"{part_after_url}\"")

    print("\nLines matching 'https://gitlab.com':")
    for part_after_url in gitlab_list:
        print(f"\"{part_after_url}\"")

else:
    print(f"Failed to retrieve contents: {response.status_code}")
