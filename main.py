"""Job Market Skill Analyzer - Assignment 01 (script version of the notebook)."""


# # Job Market Skill Analyzer
# Assignment 01 - Python Data Structures (Advanced Data Science Program)


# ## Data Setup
# Dataset (exact variable name `job_data`).

job_data = { "Job_ID": [1, 2, 3, 4, 5],
    "Role": ["Data Analyst", "Data Scientist", "Business Analyst", "Data Engineer", "ML Engineer"],
    "Company": ["ABC Corp", "XyZ Ltd", "DataWorks", "InfraTech", "AI Labs"],
    "Skills": [
        "Excel SQL Python",
        "Python ML Statistics",
        "Excel SQL PowerBI",
        "Python SQL Spark",
        "Python ML DeepLearning"
    ]}

print(job_data)


# ## 1) Print each job posting

def show_jobs():
    for i in range(len(job_data["Job_ID"])):
        print(f"ID: {job_data['Job_ID'][i]} | Role: {job_data['Role'][i]} | "
              f"Company: {job_data['Company'][i]} | Skills: {job_data['Skills'][i]}")

show_jobs()


# ## 2) Add new job postings (interactive)
# Job_ID auto-increments from the current maximum ID.

while True:
    try:
        n_new = int(input("How many job postings do you want to add? "))
        if n_new < 0:
            raise ValueError
        break
    except ValueError:
        print("Please enter a non-negative whole number.")

for _ in range(n_new):
    role = input("Enter role: ").strip()
    company = input("Enter company: ").strip()
    skills = input("Enter skills (space-separated or comma-separated): ").strip()

    new_id = max(job_data["Job_ID"]) + 1   # auto-increment from max existing ID
    job_data["Job_ID"].append(new_id)
    job_data["Role"].append(role)
    job_data["Company"].append(company)
    job_data["Skills"].append(skills)

print(f"\nAdded {n_new} posting(s). Total postings: {len(job_data['Job_ID'])}")
show_jobs()


# ## 3) Clean & normalize skills

import re

def clean_skills(skills):
    """Lowercase, replace commas with spaces, strip punctuation, normalize whitespace."""
    skills = skills.lower()
    skills = skills.replace(",", " ")
    skills = re.sub(r"[^\w\s]", "", skills)      # remove remaining punctuation
    skills = re.sub(r"\s+", " ", skills).strip()  # collapse extra spaces
    return skills

job_data["Skills"] = [clean_skills(s) for s in job_data["Skills"]]
print(job_data["Skills"])


# ## 4) Skill extraction & frequency

all_skills = []
for skill_string in job_data["Skills"]:
    all_skills.extend(skill_string.split())

skill_count = {}
for skill in all_skills:
    skill_count[skill] = skill_count.get(skill, 0) + 1

# sort by frequency (desc), then alphabetically for ties
sorted_skills = sorted(skill_count.items(), key=lambda kv: (-kv[1], kv[0]))

print("All skills:", all_skills)
print("\nTop skills by frequency:")
for skill, count in sorted_skills[:5]:
    print(f"{skill}: {count}")


# ## 5) Basic statistics & insights

total_jobs = len(job_data["Job_ID"])
unique_skill_count = len(set(all_skills))
python_jobs = [job_data["Role"][i] for i, s in enumerate(job_data["Skills"])
               if "python" in s.split()]

print("Total Jobs:", total_jobs)
print("Unique skills:", unique_skill_count)
print("Jobs mentioning Python:", python_jobs)


# ## 6) Skill search function

def find_jobs_by_skill(skill_query):
    """Return a list of (Job_ID, Role, Company) for postings containing the skill."""
    skill_query = skill_query.lower().strip()
    if skill_query == "":
        print("Empty query - please provide a skill.")
        return []
    results = []
    for i, skills in enumerate(job_data["Skills"]):
        if skill_query in skills.split():
            results.append((job_data["Job_ID"][i], job_data["Role"][i], job_data["Company"][i]))
    if not results:
        print(f"No jobs found for skill '{skill_query}'.")
    return results

print("sql    ->", find_jobs_by_skill("sql"))
print("Python ->", find_jobs_by_skill("  Python "))
print("rust   ->", find_jobs_by_skill("rust"))


# ## 7) Lambda filtering

has_common_skill = lambda i: any(skill_count[s] >= 2 for s in job_data["Skills"][i].split())
common_idx = list(filter(has_common_skill, range(len(job_data["Job_ID"]))))
common_roles = [job_data["Role"][i] for i in common_idx]

print("Roles with at least one common skill:", common_roles)


# ## 8) Unique skill set

unique_skills = sorted(set(all_skills))
print("Unique skills:")
print(unique_skills)


# ## 9) Save cleaned data to files

try:
    with open("job_skills.csv", "w", encoding="utf-8") as f:
        f.write("Job_ID,Role,Company,Skills\n")
        for i in range(len(job_data["Job_ID"])):
            f.write(f"{job_data['Job_ID'][i]},{job_data['Role'][i]},"
                    f"{job_data['Company'][i]},{job_data['Skills'][i]}\n")

    with open("top_skills.txt", "w", encoding="utf-8") as f:
        f.write("Top skills by frequency:\n")
        for skill, count in sorted_skills[:5]:
            f.write(f"{skill}: {count}\n")
except OSError as e:
    print("File error:", e)
else:
    print("job_skills.csv and top_skills.txt saved successfully.")
finally:
    print("File operations finished.")

print(open("job_skills.csv").read())
print(open("top_skills.txt").read())
