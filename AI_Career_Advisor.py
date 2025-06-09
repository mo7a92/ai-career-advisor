import os
import time
import json
from datetime import datetime

def clear_screen():
    """Clear the terminal screen for better user experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Display the program header with animation."""
    print("\n" + "=" * 60)
    print("          UNIVERSITY MAJOR RECOMMENDATION SYSTEM")
    print("=" * 60)
    print("\nThis system will help you find the best university major")
    print("based on your skills and interests.\n")

# Define questions and their associated skills with descriptions
questions = {
    1: ("Do you handle working under pressure?", "withstand", 
        "This measures your ability to perform well in stressful or time-sensitive situations."),
    2: ("Do you enjoy solving complex problems?", "problem_solving",
        "This evaluates your interest and ability in finding solutions to difficult challenges."),
    3: ("Are you good at mathematics?", "math",
        "This assesses your comfort level with numbers, formulas, and mathematical concepts."),
    4: ("Do you like creative work?", "creativity",
        "This gauges your ability to generate original ideas and think outside conventional boundaries."),
    5: ("Do you have strong public speaking skills?", "public_speaking",
        "This measures your comfort and effectiveness when presenting to groups."),
    6: ("Do you enjoy helping others?", "empathy",
        "This evaluates your ability to understand others' feelings and desire to assist them."),
    7: ("Do you think critically before making decisions?", "critical_thinking",
        "This assesses your ability to analyze situations objectively and make reasoned judgments."),
    8: ("Are you interested in science?", "science",
        "This gauges your curiosity about how the natural world works and scientific principles."),
    9: ("Are you persuasive in arguments?", "persuasion",
        "This measures your ability to convince others and effectively argue your viewpoint."),
    10: ("Do you have a keen eye for details?", "observation",
         "This evaluates your ability to notice and remember small details."),
    11: ("Do you enjoy logical reasoning and structured thinking?", "logic",
         "This assesses your ability to think in organized patterns and follow logical sequences."),
    12: ("Do you enjoy analyzing data and finding patterns?", "analysis",
         "This gauges your interest in working with information to identify trends and insights."),
    13: ("Do you have patience when working on long-term projects?", "patience",
         "This measures your ability to maintain focus and motivation on extended tasks.")
}

# Define majors with required skills and additional career information
majors = {
    "Medical": {
        "skills": {"withstand": 3, "critical_thinking": 3, "empathy": 5, "science": 4},
        "careers": ["Doctor", "Nurse", "Medical Researcher", "Pharmacist"],
        "avg_salary": "$80,000 - $200,000+",
        "study_length": "4-8+ years (depending on specialization)"
    },
    "Computer Science": {
        "skills": {"logic": 4, "creativity": 2, "problem_solving": 5, "math": 3},
        "careers": ["Software Developer", "Data Scientist", "IT Consultant", "AI Specialist"],
        "avg_salary": "$70,000 - $150,000",
        "study_length": "4 years (Bachelor's degree)"
    },
    "Engineering": {
        "skills": {"math": 4, "problem_solving": 4, "creativity": 3, "withstand": 3},
        "careers": ["Civil Engineer", "Mechanical Engineer", "Electrical Engineer", "Chemical Engineer"],
        "avg_salary": "$65,000 - $130,000",
        "study_length": "4-5 years"
    },
    "Art": {
        "skills": {"creativity": 5, "patience": 4, "observation": 4},
        "careers": ["Graphic Designer", "Illustrator", "Art Director", "Studio Artist"],
        "avg_salary": "$40,000 - $90,000",
        "study_length": "3-4 years"
    },
    "Politics": {
        "skills": {"public_speaking": 4, "persuasion": 5, "critical_thinking": 3},
        "careers": ["Political Analyst", "Campaign Manager", "Policy Advisor", "Diplomat"],
        "avg_salary": "$55,000 - $120,000",
        "study_length": "4 years (Bachelor's degree)"
    },
    "Economics": {
        "skills": {"math": 3, "logic": 4, "analysis": 4},
        "careers": ["Economist", "Financial Analyst", "Market Researcher", "Economic Consultant"],
        "avg_salary": "$65,000 - $125,000",
        "study_length": "4 years (Bachelor's degree)"
    },
    "Literature": {
        "skills": {"creativity": 4, "analysis": 3, "patience": 4},
        "careers": ["Writer/Author", "Editor", "Literary Agent", "Journalist"],
        "avg_salary": "$45,000 - $85,000",
        "study_length": "4 years (Bachelor's degree)"
    },
    "Business": {
        "skills": {"math": 2, "public_speaking": 3, "persuasion": 4, "analysis": 3, "logic": 2},
        "careers": ["Business Manager", "Marketing Specialist", "Entrepreneur", "Management Consultant"],
        "avg_salary": "$50,000 - $120,000",
        "study_length": "4 years (Bachelor's degree)"
    }
}

# Descriptions for why each major might be a good fit
major_reasons = {
    "Medical": "your combination of empathy for others, scientific aptitude, critical thinking, and ability to handle pressure. These qualities are essential for healthcare professionals who need to care for patients while solving complex medical problems.",
    
    "Computer Science": "your strong problem-solving abilities, logical thinking, mathematical skills, and creative approach to solutions. These attributes are vital for developing software, designing algorithms, and creating technological innovations.",
    
    "Engineering": "your mathematical prowess, problem-solving skills, creative thinking, and resilience under pressure. Engineers need these qualities to design solutions to complex real-world problems.",
    
    "Art": "your exceptional creativity, patience with long-term projects, and keen eye for detail and observation. These traits allow artists to express unique perspectives and create meaningful work.",
    
    "Politics": "your excellent public speaking abilities, persuasive communication style, and critical thinking skills. These are essential for influencing policy decisions and representing others effectively.",
    
    "Economics": "your mathematical abilities, logical reasoning, and talent for analyzing data and identifying patterns. Economists need these skills to understand complex systems and make informed predictions.",
    
    "Literature": "your creativity, analytical thinking, and patience with long-term projects. These qualities enable writers and literary scholars to craft and analyze compelling narratives.",
    
    "Business": "your persuasive abilities, public speaking skills, analytical thinking, and practical approach to mathematics and logic. Business professionals use these skills to lead organizations and make strategic decisions."
}

# CSP Algorithm Constants
SOFT_CONSTRAINT_WEIGHT = 0.7
HARD_CONSTRAINT_WEIGHT = 1.0
MINIMUM_SKILL_MATCH = 0.6
SKILL_IMPORTANCE_THRESHOLD = 4  # Skills rated 4 or 5 are considered important to the user

def save_results(name, user_skills, recommended_majors):
    """Save the user's results to a JSON file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{name.replace(' ', '_')}_{timestamp}.json"
    
    # Prepare data to save
    data = {
        "name": name,
        "date": timestamp,
        "skills": user_skills,
        "recommended_majors": [major for major, _ in recommended_majors]
    }
    
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        return filename
    except Exception as e:
        return None

def progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """Display a progress bar for visual feedback."""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total: 
        print()

def typing_effect(text, speed=0.01):
    """Create a typing effect for text."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()

def ask_questions():
    """Ask all questions and return the user's skills."""
    user_skills = {}
    print("Please rate your skills from 1 (lowest) to 5 (highest):\n")
    
    total_questions = len(questions)
    
    for q_num, (question_text, skill, description) in questions.items():
        progress_bar(q_num - 1, total_questions, prefix='Progress:', suffix='Complete', length=40)
        print(f"\n{q_num}. {question_text}")
        print(f"   ({description})")
        
        while True:
            try:
                rating = int(input(f"   Rate from 1 to 5: "))
                if 1 <= rating <= 5:
                    user_skills[skill] = rating
                    break
                else:
                    print("   Invalid input! Please enter a number between 1 and 5.")
            except ValueError:
                print("   Invalid input! Please enter a number between 1 and 5.")
    
    progress_bar(total_questions, total_questions, prefix='Progress:', suffix='Complete', length=40)
    print("\nAll questions completed!")
    return user_skills

def calculate_csp_match_scores(user_skills):
    """Calculate match scores using CSP-based approach."""
    match_scores = {}
    
    print("\nApplying Constraint Satisfaction Problem (CSP) algorithm...")
    total_majors = len(majors)
    
    # Identify important skills to the user (rated 4 or 5)
    important_user_skills = {skill: level for skill, level in user_skills.items() 
                            if level >= SKILL_IMPORTANCE_THRESHOLD}
    
    for i, (major_name, major_info) in enumerate(majors.items()):
        progress_bar(i, total_majors, prefix='CSP Analysis:', suffix=f'Processing {major_name}', length=40)
        time.sleep(0.1)  # Add a small delay for visual effect
        
        # Get required skills for this major
        major_requirements = major_info["skills"]
        
        # Initialize score components
        hard_constraint_score = 0
        soft_constraint_score = 0
        total_hard_constraints = 0
        total_soft_constraints = 0
        
        # Check hard constraints (required skills for the major)
        for skill, required_level in major_requirements.items():
            user_level = user_skills.get(skill, 0)
            skill_ratio = user_level / required_level if required_level > 0 else 0
            
            # Skills with high requirements are hard constraints
            if required_level >= 4:
                hard_constraint_score += min(skill_ratio, 1.0)
                total_hard_constraints += 1
            else:
                soft_constraint_score += min(skill_ratio, 1.0)
                total_soft_constraints += 1
        
        # Normalize hard constraint score
        if total_hard_constraints > 0:
            hard_constraint_score /= total_hard_constraints
        
        # Normalize soft constraint score
        if total_soft_constraints > 0:
            soft_constraint_score /= total_soft_constraints
        
        # User preference bonus: check if the major uses the user's important skills
        preference_score = 0
        preference_count = 0
        
        for skill, level in important_user_skills.items():
            if skill in major_requirements:
                preference_score += (level / 5)  # Normalize to 0-1 range
                preference_count += 1
        
        # Normalize preference score
        if preference_count > 0:
            preference_score /= preference_count
        
        # Calculate weighted total score (with CSP principles)
        # Hard constraints are must-haves, soft constraints are nice-to-haves, preferences boost score
        total_score = 0
        
        # If hard constraints meet minimum threshold, calculate final score
        if hard_constraint_score >= MINIMUM_SKILL_MATCH or not total_hard_constraints:
            total_score = (
                (hard_constraint_score * HARD_CONSTRAINT_WEIGHT) + 
                (soft_constraint_score * SOFT_CONSTRAINT_WEIGHT) + 
                (preference_score * 0.5)  # Preference bonus
            ) / (HARD_CONSTRAINT_WEIGHT + SOFT_CONSTRAINT_WEIGHT + 0.5)
            total_score *= 100  # Convert to percentage
        
        match_scores[major_name] = total_score
    
    progress_bar(total_majors, total_majors, prefix='CSP Analysis:', suffix='Complete', length=40)
    print("\nCSP analysis completed!")
    return match_scores

def recommend_majors(match_scores):
    """Find the best major(s) based on match scores."""
    if not match_scores:
        return []
    
    # Sort majors by score in descending order
    sorted_matches = sorted(match_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Filter out majors below 40% match
    filtered_matches = [(major, score) for major, score in sorted_matches if score >= 40]
    
    if not filtered_matches:
        return []
    
    # Get the top score
    top_score = filtered_matches[0][1]
    
    # Include matches within 85% of the top score
    top_matches = [(major, score) for major, score in filtered_matches if score >= top_score * 0.85]
    
    return top_matches

def display_skill_summary(user_skills):
    """Display a summary of the user's skills."""
    print("\n" + "-" * 60)
    print("                YOUR SKILLS SUMMARY")
    print("-" * 60)
    
    # Find highest and lowest skills
    if user_skills:
        sorted_skills = sorted(user_skills.items(), key=lambda x: x[1], reverse=True)
        
        print("\nYour strongest skills:")
        for skill, level in sorted_skills[:3]:
            for _, (question, skill_name, _) in questions.items():
                if skill_name == skill:
                    print(f"- {skill} ({level}/5): {question}")
                    break
        
        print("\nAreas for potential growth:")
        for skill, level in sorted(user_skills.items(), key=lambda x: x[1])[:2]:
            for _, (question, skill_name, _) in questions.items():
                if skill_name == skill:
                    print(f"- {skill} ({level}/5): {question}")
                    break
    
    print("\n" + "-" * 60)

def display_results(match_results, user_skills):
    """Display the results to the user with detailed information."""
    clear_screen()
    print("\n" + "=" * 60)
    print("                   RESULTS")
    print("=" * 60 + "\n")
    
    # Display a summary of the user's skills
    display_skill_summary(user_skills)
    
    if not match_results:
        print("\nNo suitable majors found based on your skills.")
        return
    
    typing_effect("\nBased on the CSP analysis of your responses, I recommend the following majors:\n", speed=0.01)
    time.sleep(0.5)
    
    for i, (major, score) in enumerate(match_results, 1):
        print(f"\n{i}. {major} (Compatibility: {score:.1f}%)")
        print("-" * (len(major) + 20))
        
        typing_effect(f"I recommend {major} because of {major_reasons[major]}", speed=0.005)
        
        print("\nKey skill matches:")
        for skill, required_level in majors[major]["skills"].items():
            user_level = user_skills.get(skill, 0)
            if user_level >= required_level:
                print(f"- {skill.capitalize()}: Your level {user_level}/5 meets or exceeds the required {required_level}/5")
            elif user_level >= required_level * 0.7:  # Close match
                print(f"- {skill.capitalize()}: Your level {user_level}/5 is close to the required {required_level}/5")
        
        print("\nPossible careers:")
        for career in majors[major]["careers"]:
            print(f"- {career}")
        
        print(f"\nAverage salary range: {majors[major]['avg_salary']}")
        print(f"Typical study duration: {majors[major]['study_length']}")
        print("-" * 60)
    
    print("\nThese recommendations are based on the CSP algorithm which analyzes how well your skills")
    print("satisfy the constraints (requirements) of each major, with special emphasis on critical skills.")

def get_user_name():
    """Get the user's name for personalized results."""
    name = input("\nBefore we begin, what's your name? ")
    return name if name.strip() else "User"

def main():
    """Main function to run the major recommendation system."""
    clear_screen()
    print_header()
    
    # Get user's name
    user_name = get_user_name()
    
    # Welcome the user
    typing_effect(f"\nHi {user_name}! I'll help you find the university major that best fits your skills and interests.")
    typing_effect("I'll ask you a series of questions about your abilities and preferences.")
    typing_effect("This system uses a Constraint Satisfaction Problem (CSP) algorithm to match your skills with major requirements.")
    typing_effect("Please answer honestly for the most accurate recommendations.\n")
    
    input("Press Enter to begin the assessment...")
    clear_screen()
    print_header()
    
    # Ask questions and get user skills
    user_skills = ask_questions()
    
    # Calculate match scores using CSP algorithm
    match_scores = calculate_csp_match_scores(user_skills)
    
    # Get recommended majors
    recommended_majors = recommend_majors(match_scores)
    
    # Display results
    display_results(recommended_majors, user_skills)
    
    # Ask if the user wants to save results
    save_choice = input("\nWould you like to save your results? (y/n): ").lower()
    if save_choice == 'y' or save_choice == 'yes':
        filename = save_results(user_name, user_skills, recommended_majors)
        if filename:
            print(f"\nYour results have been saved to {filename}")
        else:
            print("\nThere was an error saving your results.")
    
    print(f"\nThank you, {user_name}, for using the University Major Recommendation System!")
    print("Good luck with your academic journey!")

if __name__ == "__main__":
    main()