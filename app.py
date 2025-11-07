from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Alignr API is running."

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/score-job', methods=['POST'])
def score_job():
    try:
        data = request.get_json() or {}
        user_skills = set(data.get("user_skills", []))
        job_description = data.get("job_description", "").lower()
        job_words = set(job_description.split())

        matched = list(user_skills & job_words)
        missing = list(user_skills - job_words)

        return jsonify({
            "score": 75,
            "matched_skills": matched,
            "missing_skills": missing,
            "notes": "Score estimated by skill match count."
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/skills-gap', methods=['POST'])
def skills_gap():
    try:
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
                }
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cv-feedback', methods=['POST'])
def cv_feedback():
    try:
        data = request.get_json() or {}
        cv_text = data.get("cv_text", "")

        feedback_points = []
        prompt_questions = []

        if "team player" in cv_text.lower():
            feedback_points.append("Avoid vague phrases like 'team player'.")
            prompt_questions.append("What project did you do in a team?")

        if not feedback_points:
            feedback_points.append("Looks solid!")
            prompt_questions.append("Want help tailoring to a job?")

        return jsonify({
            "feedback_points": feedback_points,
            "prompt_questions": prompt_questions
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guidance-intake', methods=['POST'])
def guidance_intake():
    try:
        data = request.get_json() or {}
        goal = data.get("goal", "").lower()

        if "cv" in goal:
            return jsonify({"type": "cv_support", "next_step": "Upload your CV"}), 200
        return jsonify({"type": "career_exploration", "next_step": "Take quiz"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/career-quiz', methods=['POST'])
def career_quiz():
    try:
        data = request.get_json() or {}
        answers = data.get("answers", [])

        suggestion = "UX design" if "creative" in answers else "Data analysis"
        return jsonify({
            "personality_summary": "Based on traits",
            "career_suggestion": suggestion,
            "next_step": "Want tailored job suggestions?"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/career-discovery', methods=['POST'])
def career_discovery():
    try:
        data = request.get_json() or {}
        personality = data.get("personality", [])
        interests = data.get("interests", [])
        skills = data.get("skills", [])

        return jsonify({
            "suggested_careers": ["UX Designer", "Analyst"],
            "swot_summary": {
                "strengths": ["Analytical thinking"],
                "weaknesses": ["Limited experience"],
                "opportunities": ["Tech roles are growing"],
                "threats": ["Need to upskill"]
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/career-plan', methods=['POST'])
def career_plan():
    try:
        data = request.get_json() or {}
        goal_role = data.get("goal_role", "")
        current_skills = set(data.get("current_skills", []))
        required_skills = set(data.get("required_skills", []))

        missing_skills = list(required_skills - current_skills)

        return jsonify({
            "goal_role": goal_role,
            "missing_skills": missing_skills,
            "timeline_estimate_weeks": len(missing_skills) * 4,
            "step_by_step_plan": [{"skill": s} for s in missing_skills],
            "final_step": "Update CV"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/job-level-validation', methods=['POST'])
def job_level_validation():
    try:
        data = request.get_json() or {}
        skills = set(data.get("skills", []))
        experience_years = data.get("experience_years", 0)

        suggested_level = "Entry Level"
        reason = "Default reason"
        if experience_years >= 3:
            suggested_level = "Mid-Level"
            reason = "Sufficient experience"

        return jsonify({
            "suggested_level": suggested_level,
            "reason": reason,
            "suggestions": ["Build portfolio", "Show leadership"]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/job-tracker', methods=['POST'])
def job_tracker():
    try:
        data = request.get_json() or {}
        applications = data.get("applications", [])
        for app in applications:
            app["cv_tips"] = ["Add specific achievements"]
            app["next_action"] = "Submit soon"
        return jsonify({"applications": applications}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/skills-gap-table', methods=['POST'])
def skills_gap_table():
    try:
        data = request.get_json() or {}
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
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/extract-job-skills', methods=['POST'])
def extract_job_skills():
    try:
        data = request.get_json() or {}
        job_description = data.get("job_description", "").lower()

        skill_keywords = ["python", "sql", "tableau", "excel", "communication", "teamwork", "project management", "figma", "research", "analysis"]
        extracted_skills = [skill for skill in skill_keywords if skill in job_description]

        return jsonify({
            "extracted_skills": extracted_skills,
            "note": "This is a placeholder for smarter skill extraction. In the future, we'll use NLP for more accurate parsing."
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/check-skills-gap', methods=['POST'])
def check_skills_gap():
    try:
        data = request.get_json() or {}
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
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recommend-learning', methods=['POST'])
def recommend_learning():
    try:
        data = request.get_json() or {}
        missing_skills = data.get("missing_skills", [])

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
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

