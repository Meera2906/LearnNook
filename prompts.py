"""
Prompt Engineering Module
=========================
All AI prompts are centralised here. These are configured for detailed lessons,
MCQ quizzes, and comprehensive feedback with explanations.
"""

GRADE_PERSONA = {
    "5th":  "a curious 10-year-old who loves stories and simple analogies",
    "6th":  "an 11-year-old with a basic grasp of math and science concepts",
    "7th":  "a 12-year-old who can handle slightly abstract ideas",
    "8th":  "a 13-year-old ready for more structured reasoning",
    "9th":  "a 14-year-old who can handle abstract concepts with guidance",
    "10th": "a 15-year-old preparing for board exams with solid fundamentals",
}

def get_persona(grade: str) -> str:
    return GRADE_PERSONA.get(grade, f"a student in {grade} grade")

def build_explain_prompt(grade: str, subject: str, topic: str) -> tuple[str, str]:
    persona = get_persona(grade)

    system = f"""You are a warm, encouraging tutor who explains things for {persona}.
Rules you MUST follow:
1. Use ONLY concepts that {grade} students would know.
2. Structure the explanation into 4 parts:
   - Part 1: Brief Hook / Introduction
   - Part 2: Core Concept (explained clearly and in-depth)
   - Part 3: A vivid analogy from everyday life
   - Part 4: Real-world practical application
3. Total word count: Exactly between 350 and 500 words.
4. Formatting requirements:
   - Sections & Spacing: Start each of the 4 parts on a NEW line.
   - Subheadings: Wrap in triple hashes like ### Subheading ✨ and include an appropriate emoticon.
   - Section Dividers: Use three dashes `---` on a new line between the 4 main parts.
   - Highlighting: Wrap important vocabulary or key concepts in double equals like ==keyword==.
   - Paragraphs: Use double newlines between paragraphs for clear breathing room.
5. Provide a specific, concrete object to search for on Wikimedia to illustrate this topic with a real-world photo.
   - DO NOT search for the topic name itself if it's abstract (like "Grammar"). Instead, suggest a photorealistic object (like "Antique dictionary" or "Parchment and ink").
6. ALWAYS return valid JSON — nothing outside the JSON object.

Return ONLY this JSON:
{{
  "explanation": "your detailed 400-word explanation here",
  "visual_search_query": "exactly 2-4 words naming a photorealistic physical object that represents this topic"
}}"""

    user = f"Provide a detailed, immersive explanation of {topic} from {subject} for a {grade} student."

    return system, user

def build_questions_prompt(grade: str, subject: str, topic: str, explanation: str) -> tuple[str, str]:
    persona = get_persona(grade)

    system = f"""You are a skilled educator creating a 5-question Multiple Choice Quiz (MCQ) for {persona}.
Rules you MUST follow:
1. Generate EXACTLY 5 questions.
2. For each question, provide 4 options (A, B, C, D) and specify the correct index (0-3).
3. Questions must be answerable from the explanation provided.
4. Format: Q1=easy, Q2=medium, Q3=medium, Q4=hard, Q5=hard (application).
5. Avoid trick questions.
6. ALWAYS return valid JSON.

Return ONLY this JSON:
{{
  "questions": [
    {{
      "question": "question text",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_index": 0,
      "explanation": "a short 1-2 sentence explanation of why the correct answer is right",
      "hint": "a brief one-line educational clue (don't give the answer away!)"
    }},
    ... (total 5)
  ]
}}"""

    user = f"""Topic: {topic} ({subject}, {grade})
Explanation:
\"\"\"{explanation}\"\"\"

Generate a 5-question MCQ quiz based on this text."""

    return system, user

def build_evaluate_prompt(grade: str, topic: str, questions: list, student_answers: list, actual_score: str) -> tuple[str, str]:
    """
    questions: list of dicts with 'question', 'options', 'correct_index'
    student_answers: list of indices chosen by the student
    actual_score: pre-calculated score string like '3/5'
    """
    qa_data = []
    for i, q in enumerate(questions):
        correct_text = q['options'][q['correct_index']]
        student_text = q['options'][student_answers[i]] if student_answers[i] < len(q['options']) else "Invalid"
        qa_data.append(f"Q{i+1}: {q['question']}\nStudent Answer: {student_text}\nCorrect Answer: {correct_text}")

    qa_summary = "\n\n".join(qa_data)

    system = f"""You are a kind teacher evaluating a {grade} student's quiz on {topic}.
Rules you MUST follow:
1. Be encouraging and focus on progress. 
2. The student's ACTUAL SCORE is {actual_score}. Provide feedback consistent with this grade.
3. For EVERY question, provide a detailed "Why?" explanation that reinforces the concept.
4. ALWAYS return valid JSON.

Return ONLY this JSON:
{{
  "score": "{actual_score}",
  "feedback": "overall feedback under 60 words reflecting the score",
  "per_question": [
    {{
      "correct": true/false,
      "comment": "brief encouragement",
      "explanation": "the 'why' behind the correct answer (reinforce the concept)"
    }},
    ...
  ]
}}"""

    user = f"""Quiz Results for {topic}:
{qa_summary}

Evaluate and provide the 'Why?' for each question."""

    return system, user
