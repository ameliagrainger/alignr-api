
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Alignr API is running."

@app.route('/score-job', methods=['POST'])
def score_job():
    data = request.get_json()
    return jsonify({
        "score": 78,
        "matched_skills": ["Python", "pandas"],
        "missing_skills": ["SQL", "Tableau"],
        "notes": "You're a strong match, but missing two key tools mentioned in the job ad."
    })

@app.route('/skills-gap', methods=['POST'])
def skills_gap():
    data = request.get_json()
    
    return jsonify({
        "job_title": "Junior Data Analyst",
        "skills_to_develop": [
            {
                "skill": "SQL",
                "why_needed": "Required for querying large datasets, a core task in the job ad.",
                "how_to_evidence": "Complete a portfolio project that analyzes open datasets using SQL queries.",
                "recommended_course": {
                    "name": "SQL for Data Analysis",
                    "provider": "Coursera",
                    "duration": "4 weeks",
                    "hours_per_week": 4
                }
            },
            {
                "skill": "Tableau",
                "why_needed": "Used for data visualization and dashboards, mentioned by multiple employers.",
                "how_to_evidence": "Create an interactive dashboard using Tableau Public with real data.",
                "recommended_course": {
                    "name": "Tableau Fundamentals",
                    "provider": "LinkedIn Learning",
                    "duration": "3 weeks",
                    "hours_per_week": 3
                }
            }
        ]
    })


@app.route('/cv-feedback', methods=['POST'])
def cv_feedback():
    data = request.get_json()
    cv_text = data.get("cv_text", "")

    # Simulated analysis logic
    feedback_points = []
    prompt_questions = []

    if "team player" in cv_text.lower() or "hard-working" in cv_text.lower():
        feedback_points.append("Avoid vague phrases like 'team player' — replace with specific examples.")
        prompt_questions.append("What’s a project where you worked in a team and what was the outcome?")

    if "summary" not in cv_text.lower() and "profile" not in cv_text.lower():
        feedback_points.append("Add a personal summary at the top — who you are, what you bring, and your goals.")
        prompt_questions.append("What kind of roles are you targeting, and what makes you a good fit?")

    if len(cv_text.split()) < 150:
        feedback_points.append("Your CV looks short — consider expanding with results, skills, and examples.")
        prompt_questions.append("Can you add a section for achievements, tools used, or quantified results?")

    if "figma" in cv_text.lower() or "sql" in cv_text.lower():
        feedback_points.append("Good job including industry tools — make sure they appear in key sections.")

    if not feedback_points:
        feedback_points.append("Looks solid. You might still customise it for the job you’re applying to.")
        prompt_questions.append("Would you like help tailoring this to a specific job description?")

    return jsonify({
        "feedback_points": feedback_points,
        "prompt_questions": prompt_questions
    })
@app.route('/guidance-intake', methods=['POST'])
def guidance_intake():
    data = request.get_json()
    goal = data.get("goal", "").lower()

    if "cv" in goal:
        return jsonify({
            "type": "cv_support",
            "next_step": "Upload your CV or list your experience. I’ll guide you to improve each section."
        })
    elif "career" in goal or "not sure" in goal:
        return jsonify({
            "type": "career_exploration",
            "next_step": "Let’s start with a quick personality and interests quiz."
        })
    elif "job" in goal or "applying" in goal:
        return jsonify({
            "type": "job_search",
            "next_step": "Tell me what kinds of jobs you're applying for — I’ll help you target each one."
        })
    else:
        return jsonify({
            "type": "unsure",
            "next_step": "Let’s clarify your goal — do you need help with your CV, finding a direction, or preparing for job applications?"
        })


@app.route('/career-quiz', methods=['POST'])
def career_quiz():
    data = request.get_json()
    answers = data.get("answers", [])

    # Basic personality matching (placeholder)
    if "creative" in answers:
        suggestion = "You may thrive in UX design, content creation, or branding roles."
    elif "logical" in answers:
        suggestion = "Data analysis, operations, or finance roles could fit you well."
    else:
        suggestion = "You might enjoy generalist roles — let’s explore your skills further."

    return jsonify({
        "personality_summary": "Based on your responses, we’ve identified core traits.",
        "career_suggestion": suggestion,
        "next_step": "Would you like job ideas in that area, or help building a CV for it?"
    })
@app.route('/career-discovery', methods=['POST'])
def career_discovery():
    data = request.get_json()
    personality = data.get("personality", [])
    interests = data.get("interests", [])
    skills = data.get("skills", [])

    # Simulated logic for career suggestions
    if "creative" in personality and "design" in interests:
        recommended_roles = ["UX Designer", "Graphic Designer"]
    elif "analytical" in personality and "data" in interests:
        recommended_roles = ["Data Analyst", "Business Intelligence Analyst"]
    else:
        recommended_roles = ["Project Coordinator", "Customer Success Associate"]

    return jsonify({
        "personality_traits": personality,
        "interests": interests,
        "skills": skills,
        "suggested_careers": recommended_roles,
        "swot_summary": {
            "strengths": ["Strong analytical mindset", "Good communication"],
            "weaknesses": ["Lack of industry experience"],
            "opportunities": ["High demand in tech and creative sectors"],
            "threats": ["Need to quickly upskill in modern tools"]
        }
    })
@app.route('/career-plan', methods=['POST'])
def career_plan():
    data = request.get_json()
    goal_role = data.get("goal_role", "")
    current_skills = set(data.get("current_skills", []))
    required_skills = set(data.get("required_skills", []))
    experience_years = data.get("experience_years", 0)

    missing_skills = list(required_skills - current_skills)
    estimated_weeks = len(missing_skills) * 4

    # Determine path level and validate against experience
    if "senior" in goal_role.lower():
        if experience_years < 5:
            return jsonify({
                "error": "Senior roles typically require 5+ years of experience. Try targeting a mid-level role first."
            }), 400
        path_level = "Senior Role"
        realistic_timeline = "12–24 months with leadership projects and real-world delivery."
    elif "mid" in goal_role.lower() or "associate" in goal_role.lower():
        if experience_years < 2:
            return jsonify({
                "error": "Mid-level roles usually require at least 2 years of experience. Consider an entry-level path first."
            }), 400
        path_level = "Intermediate Role"
        realistic_timeline = "6–12 months with real projects and collaboration experience."
    else:
        path_level = "Entry-Level Role"
        realistic_timeline = "3–6 months with focused learning and practical projects."

    learning_plan = [
        {
            "skill": skill,
            "suggested_course": f"{skill} Fundamentals (Coursera)",
            "duration": "3–4 weeks",
            "hours_per_week": 4
        }
        for skill in missing_skills
    ]

    return jsonify({
        "goal_role": goal_role,
        "path_level": path_level,
        "missing_skills": missing_skills,
        "realistic_timeline": realistic_timeline,
        "step_by_step_plan": learning_plan,
        "final_step": "Update CV and portfolio with projects demonstrating these skills"
    })
@app.route('/job-level-validation', methods=['POST'])
def job_level_validation():
    data = request.get_json()
    skills = set(data.get("skills", []))
    experience_years = data.get("experience_years", 0)

    if experience_years < 1:
        suggested_level = "Entry Level"
        reason = "You have limited experience — great for internships or junior roles."
    elif experience_years < 3 and "SQL" in skills and "Excel" in skills:
        suggested_level = "Junior Analyst"
        reason = "You meet common expectations for junior analytical roles."
    elif experience_years >= 3 and "Python" in skills and "SQL" in skills:
        suggested_level = "Mid-Level Analyst"
        reason = "Your technical skills and experience align with mid-level roles."
    else:
        suggested_level = "Needs Review"
        reason = "We’d need more context to recommend a level."

    return jsonify({
        "suggested_level": suggested_level,
        "reason": reason,
        "suggestions": [
            "Add projects to show applied skills.",
            "Highlight leadership or mentoring to aim higher."
        ]
    })


@app.route('/job-tracker', methods=['POST'])
def job_tracker():
    data = request.get_json()
    applications = data.get("applications", [])

    for app in applications:
        job_title = app.get("job_title", "")
        company = app.get("company", "")
        deadline = app.get("deadline", "")
        tailored = app.get("tailored_cv", False)
        status = app.get("status", "not started")

        app["next_step"] = "Tailor CV and cover letter" if not tailored else "Submit application"
        app["is_urgent"] = "Yes" if deadline and status == "not started" else "No"
        app["suggested_action"] = (
            "Focus on CV tailoring" if not tailored
            else "Check deadline and submit"
            if status == "in progress"
            else "Track response"
        )

    return jsonify({"applications": applications})
@app.route('/skills-gap-table', methods=['POST'])
def skills_gap_table():
    data = request.get_json()
    user_skills = set(data.get("user_skills", []))
    job_skills = set(data.get("job_skills", []))

    matched = list(user_skills & job_skills)
    missing = list(job_skills - user_skills)

    gap_table = []

    for skill in matched:
        gap_table.append({
            "skill": skill,
            "status": "Matched ✅",
            "action": "Ensure this is clearly mentioned on your CV and portfolio."
        })

    for skill in missing:
        gap_table.append({
            "skill": skill,
            "status": "Missing ❌",
            "action": f"Find a beginner course on {skill} or apply it in a project to gain experience."
        })

    return jsonify({
        "gap_table": gap_table,
        "summary": {
            "matched_skills": matched,
            "missing_skills": missing,
            "total_required": len(job_skills),
            "total_matched": len(matched),
            "total_missing": len(missing)
        }
    })
@app.route('/extract-job-skills', methods=['POST'])
def extract_job_skills():
    data = request.get_json()
    job_description = data.get("job_description", "").lower()

    # Simulated keyword extraction — in future, use NLP
    skill_keywords = ["python", "sql", "tableau", "excel", "communication", "teamwork", "project management", "figma", "research", "analysis"]
    
    extracted_skills = [skill for skill in skill_keywords if skill in job_description]

    return jsonify({
        "extracted_skills": extracted_skills,
        "note": "This is a placeholder for smarter skill extraction. In the future, we'll use NLP for more accurate parsing."
    })
@app.route('/check-skills-gap', methods=['POST'])
def check_skills_gap():
    data = request.get_json()
    job_description = data.get("job_description", "").lower()
    user_skills = set(skill.lower() for skill in data.get("user_skills", []))

    skill_keywords = ["python", "sql", "tableau", "excel", "communication", "teamwork", "project management", "figma", "research", "analysis"]

    extracted_skills = set([skill for skill in skill_keywords if skill in job_description])
    matched = list(user_skills & extracted_skills)
    missing = list(extracted_skills - user_skills)

    return jsonify({
        "job_skills_found": list(extracted_skills),
        "matched_skills": matched,
        "missing_skills": missing,
        "gap_note": "These are the skills mentioned in the job vs what you currently show."
    })
@app.route('/recommend-learning', methods=['POST'])
def recommend_learning():
    data = request.get_json()
    missing_skills = data.get("missing_skills", [])

    # Simple hardcoded resource mapping (expandable later)
    course_db = {
        "sql": {
            "name": "SQL for Data Analysis",
            "provider": "Coursera",
            "duration": "4 weeks",
            "hours_per_week": 3,
            "reason": "Covers querying, filtering, and joining data, core to analyst roles."
        },
        "tableau": {
            "name": "Tableau Fundamentals",
            "provider": "LinkedIn Learning",
            "duration": "3 weeks",
            "hours_per_week": 3,
            "reason": "Covers dashboard creation and storytelling with data."
        },
        "excel": {
            "name": "Excel Skills for Business",
            "provider": "Coursera",
            "duration": "6 weeks",
            "hours_per_week": 2,
            "reason": "Master formulas, data cleanup, and pivot tables."
        },
        "python": {
            "name": "Python Basics for Data Science",
            "provider": "edX",
            "duration": "5 weeks",
            "hours_per_week": 4,
            "reason": "Covers data manipulation, basic analysis, and scripting."
        }
    }

    recommendations = []
    for skill in missing_skills:
        skill_lower = skill.lower()
        if skill_lower in course_db:
            recommendations.append({
                "skill": skill,
                "course": course_db[skill_lower]
            })

    return jsonify({
        "recommendations": recommendations,
        "note": "These resources directly match the skills you need to develop."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
