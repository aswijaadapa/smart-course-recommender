"""
generate_dataset.py
Generates dataset/courses.csv with 200+ realistic course records
for the Smart Course Recommendation System.

Run once with:  python dataset/generate_dataset.py
"""

import csv
import random

random.seed(42)

PLATFORMS = ["Coursera", "Udemy", "edX", "Udacity", "LinkedIn Learning", "Pluralsight"]
DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]

# Each domain: (category, career_domain, skills pool, tag pool, course name templates)
DOMAINS = {
    "Web Development": {
        "career_domain": "Software Engineering",
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Django", "REST APIs", "Git"],
        "tags": ["web development", "frontend", "backend", "full stack", "javascript"],
        "titles": [
            "Complete Web Development Bootcamp", "Modern JavaScript from Scratch",
            "React - The Complete Guide", "Django for Beginners", "Node.js API Masterclass",
            "HTML CSS JavaScript Fundamentals", "Full Stack Web Development",
            "Building REST APIs with Django", "Advanced React and Redux",
            "Responsive Web Design Bootcamp",
        ],
    },
    "Data Science": {
        "career_domain": "Data Analyst",
        "skills": ["Python", "Pandas", "NumPy", "Data Visualization", "Statistics", "SQL", "Excel"],
        "tags": ["data science", "data analysis", "python", "statistics", "beginner friendly"],
        "titles": [
            "Python for Data Science", "Data Analysis with Pandas", "Statistics for Data Science",
            "SQL for Data Analysts", "Data Visualization with Matplotlib and Seaborn",
            "Excel for Data Analysis", "Introduction to Data Science",
            "Exploratory Data Analysis Masterclass", "Data Science Bootcamp",
            "Applied Statistics with Python",
        ],
    },
    "Machine Learning": {
        "career_domain": "AI/ML Engineer",
        "skills": ["Python", "Scikit-learn", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning"],
        "tags": ["machine learning", "deep learning", "ai", "neural networks", "python"],
        "titles": [
            "Machine Learning A-Z", "Deep Learning Specialization", "Introduction to Neural Networks",
            "Machine Learning with Scikit-learn", "TensorFlow for Deep Learning",
            "PyTorch for Beginners", "Natural Language Processing Fundamentals",
            "Computer Vision with Deep Learning", "Applied Machine Learning",
            "Reinforcement Learning Basics",
        ],
    },
    "Cloud Computing": {
        "career_domain": "Cloud Engineer",
        "skills": ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "DevOps", "Linux"],
        "tags": ["cloud computing", "aws", "devops", "infrastructure", "kubernetes"],
        "titles": [
            "AWS Certified Solutions Architect", "Microsoft Azure Fundamentals",
            "Google Cloud Platform Essentials", "Docker and Kubernetes Complete Guide",
            "DevOps Engineering Bootcamp", "Linux for Cloud Engineers",
            "Cloud Infrastructure with Terraform", "AWS Lambda and Serverless Computing",
            "CI/CD Pipelines with Jenkins", "Cloud Security Fundamentals",
        ],
    },
    "Cybersecurity": {
        "career_domain": "Security Analyst",
        "skills": ["Network Security", "Ethical Hacking", "Cryptography", "Linux", "Python", "SIEM"],
        "tags": ["cybersecurity", "ethical hacking", "network security", "penetration testing"],
        "titles": [
            "Ethical Hacking Bootcamp", "Network Security Fundamentals",
            "Certified Cybersecurity Analyst Prep", "Penetration Testing with Kali Linux",
            "Cryptography Basics", "Security Operations and SIEM",
            "Introduction to Cybersecurity", "Web Application Security",
            "Malware Analysis Fundamentals", "Cloud Security Essentials",
        ],
    },
    "Mobile Development": {
        "career_domain": "Mobile App Developer",
        "skills": ["Flutter", "Dart", "Kotlin", "Swift", "React Native", "Firebase"],
        "tags": ["mobile development", "android", "ios", "flutter", "app development"],
        "titles": [
            "Flutter and Dart Complete Course", "Android Development with Kotlin",
            "iOS Development with Swift", "React Native for Beginners",
            "Cross Platform App Development", "Firebase for Mobile Apps",
            "Building Your First Mobile App", "Advanced Android Development",
            "Mobile UI/UX Design Principles", "App Store Deployment Guide",
        ],
    },
    "UI/UX Design": {
        "career_domain": "UI/UX Designer",
        "skills": ["Figma", "Adobe XD", "Wireframing", "User Research", "Prototyping", "Design Systems"],
        "tags": ["ui design", "ux design", "figma", "product design", "prototyping"],
        "titles": [
            "UI/UX Design Fundamentals", "Figma for Beginners", "User Research and Testing",
            "Design Systems Masterclass", "Adobe XD Complete Guide",
            "Prototyping and Wireframing", "Mobile App Design Principles",
            "Design Thinking Bootcamp", "Typography and Visual Design",
            "Portfolio Building for Designers",
        ],
    },
    "Business & Management": {
        "career_domain": "Business Analyst",
        "skills": ["Excel", "Project Management", "Agile", "Scrum", "Business Analysis", "Communication"],
        "tags": ["business analysis", "project management", "agile", "scrum", "leadership"],
        "titles": [
            "Business Analysis Fundamentals", "Agile and Scrum Masterclass",
            "Project Management Professional Prep", "Excel for Business Analysts",
            "Leadership and Team Management", "Introduction to Product Management",
            "Business Strategy Essentials", "Financial Analysis for Managers",
            "Digital Marketing Fundamentals", "Negotiation Skills for Professionals",
        ],
    },
    "Blockchain": {
        "career_domain": "Blockchain Developer",
        "skills": ["Solidity", "Ethereum", "Smart Contracts", "Web3.js", "Cryptography"],
        "tags": ["blockchain", "web3", "smart contracts", "ethereum", "crypto"],
        "titles": [
            "Blockchain Fundamentals", "Solidity and Smart Contract Development",
            "Ethereum Development Bootcamp", "Web3.js for Beginners",
            "Building Decentralized Applications", "Introduction to Cryptocurrency",
            "NFT Development Masterclass", "Blockchain Security Basics",
            "DeFi Fundamentals", "Smart Contract Auditing",
        ],
    },
    "Game Development": {
        "career_domain": "Game Developer",
        "skills": ["Unity", "C#", "Unreal Engine", "Game Design", "3D Modeling", "C++"],
        "tags": ["game development", "unity", "unreal engine", "game design", "programming"],
        "titles": [
            "Complete Unity Game Development", "Unreal Engine for Beginners",
            "C# Programming for Game Developers", "2D Game Design Fundamentals",
            "3D Game Development with Unity", "Game Physics and Animation",
            "Introduction to Game Design", "Building Your First Mobile Game",
            "Multiplayer Game Development", "Game Art and Asset Creation",
        ],
    },
}

DESC_TEMPLATES = [
    "A {difficulty_lower} level course covering {skills_str} for learners aiming to become a {career_domain}.",
    "Hands-on {category} training focused on {skills_str}, designed for {difficulty_lower} learners.",
    "Learn {skills_str} through practical projects in this {difficulty_lower} {category} course.",
    "This course builds real-world {category} skills including {skills_str}, ideal for aspiring {career_domain}s.",
    "A project-based {difficulty_lower} course teaching {skills_str} with real industry use cases.",
]

DURATIONS = ["2 weeks", "3 weeks", "4 weeks", "6 weeks", "8 weeks", "10 weeks", "12 weeks",
             "20 hours", "30 hours", "40 hours", "60 hours"]


def build_dataset():
    rows = []
    course_id = 1
    for category, meta in DOMAINS.items():
        titles = meta["titles"]
        for i, title in enumerate(titles):
            # generate 2 variants per title (different platform/difficulty) to reach 200+
            for variant in range(2):
                difficulty = DIFFICULTIES[(i + variant) % 3]
                platform = random.choice(PLATFORMS)
                skills_sample = random.sample(meta["skills"], k=min(4, len(meta["skills"])))
                tags_sample = random.sample(meta["tags"], k=min(4, len(meta["tags"])))
                skills_str = ", ".join(skills_sample)
                tags_str = ", ".join(tags_sample + [difficulty.lower()])
                desc_template = random.choice(DESC_TEMPLATES)
                description = desc_template.format(
                    difficulty_lower=difficulty.lower(),
                    skills_str=skills_str,
                    category=category,
                    career_domain=meta["career_domain"],
                )
                rating = round(random.uniform(3.6, 4.9), 1)
                duration = random.choice(DURATIONS)
                course_name = title if variant == 0 else f"{title} - Part 2"

                rows.append({
                    "course_name": course_name,
                    "platform": platform,
                    "category": category,
                    "career_domain": meta["career_domain"],
                    "skills_required": skills_str,
                    "tags": tags_str,
                    "difficulty": difficulty,
                    "duration": duration,
                    "rating": rating,
                    "description": description,
                })
                course_id += 1
    return rows


def main():
    rows = build_dataset()
    fieldnames = ["course_name", "platform", "category", "career_domain", "skills_required",
                  "tags", "difficulty", "duration", "rating", "description"]
    with open("dataset/courses.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {len(rows)} courses -> dataset/courses.csv")


if __name__ == "__main__":
    main()
