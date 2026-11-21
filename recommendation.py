from careers import CAREERS


def get_recommendations(selected_interests, selected_skills, selected_subjects):
    """Return careers ranked by how closely they match the student's choices."""
    results = []

    for career in CAREERS:
        interest_matches = set(selected_interests) & set(career["interests"])
        skill_matches = set(selected_skills) & set(career["skills"])
        subject_matches = set(selected_subjects) & set(career["subjects"])

        # Interests: 40%, skills: 40%, subjects: 20%.
        interest_score = (len(interest_matches) / len(career["interests"])) * 40
        skill_score = (len(skill_matches) / len(career["skills"])) * 40
        subject_score = (len(subject_matches) / len(career["subjects"])) * 20

        score = round(interest_score + skill_score + subject_score)

        if score > 0:
            results.append({
                "title": career["title"],
                "description": career["description"],
                "score": score,
                "matched_interests": sorted(interest_matches),
                "matched_skills": sorted(skill_matches),
                "matched_subjects": sorted(subject_matches)
            })

    return sorted(results, key=lambda item: item["score"], reverse=True)
