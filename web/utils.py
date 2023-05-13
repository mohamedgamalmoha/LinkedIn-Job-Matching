import spacy


# Load Spacy English language model
nlp = spacy.load("en_core_web_sm")


# Function to extract important named entities and noun phrases from job description
def extract_job_requirements(job_description):
    """
    Given a job description, this function extracts important named entities and noun phrases.
    Named entities are words or phrases that represent specific categories such as organizations, products, and people.
    Noun phrases are groups of words that function as a single unit and consist of a noun and any associated words (e.g., adjectives, determiners).
    The function uses Spacy's English language model to perform named entity recognition and noun chunking.
    Returns a list of extracted named entities and noun phrases.
    """
    # Analyze job description with Spacy
    doc = nlp(job_description)
    # Extract named entities and noun phrases
    entities = [entity.text for entity in doc.ents if entity.label_ in ["ORG", "PRODUCT", "PERSON"]]
    noun_chunks = [chunk.text for chunk in doc.noun_chunks]
    # Return extracted named entities and noun phrases
    return entities + noun_chunks


# Function to calculate matching score based on employee criteria and job requirements
def calculate_matching_score(employee_criteria, job_requirements):
    """
    Given employee criteria and job requirements, this function calculates a matching score between 0 and 2.
    The function takes into account two factors: skills and education.
    The skills factor is based on the overlap between the employee's skills and the job's required skills.
    The education factor is based on whether the employee's education level matches the job's required education level.
    The function returns the sum of the two factors as the matching score.
    """
    # Calculate skill factor
    skill_set = set(employee_criteria['skills'])
    required_skills = set(job_requirements)
    common_skills = skill_set.intersection(required_skills)
    skill_score = len(common_skills) / len(skill_set)

    # Calculate education factor
    if employee_criteria['education'] in job_requirements:
        education_score = 1.0
    else:
        education_score = 0.0

    # Calculate matching score as sum of skill factor and education factor
    matching_score = skill_score + education_score

    # Return matching score
    return matching_score
