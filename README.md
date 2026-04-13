# [Movie Database Project]

**CS178: Cloud and Database Systems — Project #1**
**Author:** [Reece Dickerson]
**GitHub:** [reecedickerson]

---

## Overview

<!-- Describe your project in 2-4 sentences. What does it do? Who is it for? What problem does it solve? -->
<!-- This project allows the user to access movies held within the Movies database hosted on my EC2 instance.-->
<!-- In addition to looking up movies, it allows the user to add movies to the database and update their information.-->


---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for [describe what you stored]
- **AWS DynamoDB** — non-relational database for [describe what you stored]
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py          # Main Flask application — routes and app logic
├── dbCode.py            # Database helper functions (MySQL connection + queries)
├── creds_sample.py      # Sample credentials file (see Credential Setup below)
├── static/              # Folder housing images
├── templates/
│   ├── home.html        # Landing page
│   ├── add_movie.html   # Page that allows user to add movie to database
│   ├── delete_movie.html       # Page that allows user to delete movie from database
│   ├── update_movie.html       # Page that allows user to update information about movie in database   
│   ├── [other].html     # Add descriptions for your other templates
├── .gitignore           # Excludes creds.py and other sensitive files
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://32.192.1.102:8080/
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

<!-- Briefly describe your relational database schema. What tables do you have? What are the key relationships? -->
<!-- The primary table within the movies database is movie. -->

**Example:**

- `movie` — stores all the different movies in the database and their information; primary key is `movie_id`
- `movie_languages` — stores language and movie ids; foreign key links to `movie`
- `language` — stores the different languages used and their codes; foreign key links to `movie_languages`

The JOIN query used in this project: <!-- describe it in plain English -->
<!-- I joined genre, to moive_genres, to moive. I also joined language, to movie_languages, to movie-->
<!-- This allowed for the different functions to access genres and languages-->

### DynamoDB

<!-- Describe your DynamoDB table. What is the partition key? What attributes does each item have? How does it connect to the rest of the app? -->

- **Table name:** `movie`
- **Partition key:** `movie_id`
- **Used for:** <!-- Returned the corresponding movie and it's information-->
<!--  Each item has attributes such as: overview, budget, runtime, popularity, and release date-->

---

## CRUD Operations

| Operation | Route      | Description    |
| --------- | ---------- | -------------- |
| Create    | `/add-movie` | adds movie to the database |
| Read      | `/display-movies` | shows information about the desired moive(s) |
| Update    | `/update-movie` | allows user to add information to the desired movie |
| Delete    | `/delete-movie` | allows user to remove movie from database |

---

## Challenges and Insights

<!-- What was the hardest part? What did you learn? Any interesting design decisions? -->
<!-- If I'm being honest, the hardest part was finding time to work on the project, -->
<!-- and figure out what I wanted to do with it. I ended up opting for a very simple product.-->
<!-- I learned that its better to just do it instead of sitting and thinking about how to do it.-->
<!-- I also learned more about html and bootstrap in getting the pages to work.-->
<!-- And I decided to have some fun with the delete page. Because why not.-->

---

## AI Assistance

<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here. -->

<!-- By each section that used an AI tool, I provided a description of what it did.-->
<!-- I exclusively used GitHub's Copilot, easily accessible through VSCode. Some of my peers showed it to me and-->
<!-- demonstrated it's utility. It was very quick and very efficient. If there was a function that I was unsure how to-->
<!-- tackle, I would ask for guidance. Or if there was an error, I would ask if it saw some issue I missed.-->
<!-- However, there were a few errors it was entirely unable to fix, or didn't know how to. AI is no panacea.-->
