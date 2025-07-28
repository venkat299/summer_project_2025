import streamlit as st

# --- MOCK DATA ---
# This data simulates the input you would provide to the application.
# It follows the structure you defined: all_results and document_pairs.

def get_mock_data():
    """Generates mock data for demonstration purposes."""
    all_results = [
        # --- Document Pair 1 Results ---
        (
            [
                {
                    'rule_details': {'Extracted Rule': 'Must have 5+ years of experience in Python programming.'},
                    'status': 'Pass',
                    'explanation': 'The candidate explicitly mentions having 7 years of Python experience in their resume, which satisfies the requirement.',
                    'similarity_score': 0.92,
                    'best_match': 'Developed and maintained several large-scale applications over 7 years using Python.'
                },
                {
                    'rule_details': {'Extracted Rule': 'Experience with cloud platforms like AWS or Azure is required.'},
                    'status': 'Pass',
                    'explanation': 'The CV lists "AWS (S3, EC2, Lambda)" under the skills section, directly meeting the cloud platform requirement.',
                    'similarity_score': 0.88,
                    'best_match': 'Proficient with cloud services, including AWS (S3, EC2, Lambda).'
                },
                {
                    'rule_details': {'Extracted Rule': 'A Bachelor\'s degree in Computer Science is mandatory.'},
                    'status': 'Fail',
                    'explanation': 'The candidate\'s resume indicates a degree in Information Technology, not Computer Science. This does not meet the specific degree requirement.',
                    'similarity_score': 0.65,
                    'best_match': 'B.Sc. in Information Technology, University of Tech.'
                },
                {
                    'rule_details': {'Extracted Rule': 'Familiarity with containerization technologies (Docker, Kubernetes).'},
                    'status': 'Pass',
                    'explanation': 'The candidate mentions Docker in their project descriptions, indicating familiarity.',
                    'similarity_score': 0.78,
                    'best_match': 'Utilized Docker to containerize microservices for a deployment pipeline.'
                }
            ],
            {
                'compliance_rate': 0.75,
                'avg_similarity': 0.81,
                'passed_rules': 3,
                'failed_rules': 1
            }
        ),
        # --- Document Pair 2 Results ---
        (
            [
                {
                    'rule_details': {'Extracted Rule': 'Seeking a candidate with a Master\'s degree.'},
                    'status': 'Pass',
                    'explanation': 'The candidate\'s CV clearly states they hold a Master of Science degree.',
                    'similarity_score': 0.95,
                    'best_match': 'Education: Master of Science, Advanced University (2020).'
                },
                {
                    'rule_details': {'Extracted Rule': 'At least 3 years of project management experience.'},
                    'status': 'Fail',
                    'explanation': 'The candidate lists project coordination roles but does not explicitly state 3 years of project management experience. The roles described seem more junior.',
                    'similarity_score': 0.55,
                    'best_match': 'Coordinated project timelines and deliverables for the junior development team.'
                },
                {
                    'rule_details': {'Extracted Rule': 'Must be proficient in JavaScript and React.'},
                    'status': 'Fail',
                    'explanation': 'The CV mentions experience with vanilla JavaScript but does not list React or any similar modern frontend framework.',
                    'similarity_score': 0.40,
                    'best_match': 'Developed web interfaces using HTML, CSS, and JavaScript.'
                }
            ],
            {
                'compliance_rate': 0.33,
                'avg_similarity': 0.63,
                'passed_rules': 1,
                'failed_rules': 2
            }
        )
    ]

    document_pairs = [
        # --- Document Pair 1 Texts ---
        {
            'job_description': """
            **Senior Python Developer**

            We are looking for an experienced Senior Python Developer to join our dynamic team. The ideal candidate will have a strong background in building scalable web applications.

            **Responsibilities:**
            - Design and implement low-latency, high-availability applications.
            - Integrate user-facing elements with server-side logic.
            - Write reusable, testable, and efficient code.

            **Requirements:**
            - Must have 5+ years of experience in Python programming.
            - Experience with cloud platforms like AWS or Azure is required.
            - A Bachelor's degree in Computer Science is mandatory.
            - Familiarity with containerization technologies (Docker, Kubernetes).
            """,
            'candidate_cv': """
            **Jane Doe**
            Software Engineer

            **Summary:**
            A highly motivated software engineer with over 8 years of experience in software development.

            **Experience:**
            **Lead Python Developer, Tech Solutions Inc. (2016 - Present)**
            - Developed and maintained several large-scale applications over 7 years using Python.
            - Utilized Docker to containerize microservices for a deployment pipeline.

            **Skills:**
            - Languages: Python, Java, SQL
            - Cloud: Proficient with cloud services, including AWS (S3, EC2, Lambda).

            **Education:**
            - B.Sc. in Information Technology, University of Tech.
            """
        },
        # --- Document Pair 2 Texts ---
        {
            'job_description': """
            **Technical Project Manager**

            We need a Technical Project Manager to oversee software development projects from conception to delivery.

            **Key Qualifications:**
            - At least 3 years of project management experience.
            - Strong understanding of the software development lifecycle.
            - Seeking a candidate with a Master's degree.
            - Must be proficient in JavaScript and React.
            """,
            'candidate_cv': """
            **John Smith**
            IT Professional

            **Profile:**
            Detail-oriented IT professional with a passion for technology and teamwork.

            **Work History:**
            **Project Coordinator, Innovate Corp. (2021 - Present)**
            - Coordinated project timelines and deliverables for the junior development team.
            - Assisted senior managers in tracking project milestones.

            **Technical Skills:**
            - Developed web interfaces using HTML, CSS, and JavaScript.
            - Agile, Scrum, Jira

            **Education:**
            - Master of Science, Advanced University (2020).
            - Bachelor of Arts, State College (2018).
            """
        }
    ]
    return all_results, document_pairs

# --- STREAMLIT APP ---

st.set_page_config(layout="wide", page_title="Compliance Validation Visualizer")

# --- Load Data ---
# In a real application, you would load your variables here.
# For this demo, we are calling the mock data function.
all_results, document_pairs = get_mock_data()


# --- Sidebar for Selection and Metrics ---
st.sidebar.title("📋 Compliance Dashboard")

# 1. Document Pair Selection
pair_options = [f"Document Pair {i+1}" for i in range(len(document_pairs))]
selected_pair_str = st.sidebar.selectbox(
    "Select a Document Pair to Analyze",
    options=pair_options,
    help="Choose the document set you want to review."
)

# Get the index of the selected pair
selected_index = pair_options.index(selected_pair_str)

# Retrieve the specific data for the selected pair
selected_results, selected_metrics = all_results[selected_index]
selected_docs = document_pairs[selected_index]


# 5. Overall Metrics Display
st.sidebar.header("📊 Overall Metrics")

# Use columns for a cleaner layout of metrics
m_col1, m_col2 = st.sidebar.columns(2)
m_col1.metric(
    label="Compliance Rate",
    value=f"{selected_metrics['compliance_rate']:.0%}",
    help="Percentage of requirements met by the candidate's CV."
)
m_col2.metric(
    label="Avg. Similarity",
    value=f"{selected_metrics['avg_similarity']:.2f}",
    help="The average similarity score across all requirements."
)

st.sidebar.write(f"**Passed Rules:** {selected_metrics['passed_rules']}")
st.sidebar.write(f"**Failed Rules:** {selected_metrics['failed_rules']}")


# --- Main Panel for Details ---
st.title(f"Analysis for {selected_pair_str}")
st.markdown("---")


# 2. Display Document Texts
st.header("📄 Original Documents")
doc_col1, doc_col2 = st.columns(2)

with doc_col1:
    st.subheader("Job Description")
    st.text_area(
        "Job Description Text",
        selected_docs['job_description'],
        height=300,
        label_visibility="collapsed"
    )

with doc_col2:
    st.subheader("Candidate CV")
    st.text_area(
        "Candidate CV Text",
        selected_docs['candidate_cv'],
        height=300,
        label_visibility="collapsed"
    )

st.markdown("---")


# 3. & 4. Display Requirements List with Interactive Details
st.header("✅/❌ Requirement Validation Details")
st.markdown("Click on each requirement to see a detailed explanation and the best-matching text from the CV.")

if not selected_results:
    st.warning("No requirement results found for this document pair.")
else:
    # Iterate through each requirement's results and display them
    for result in selected_results:
        status_icon = "✅" if result['status'] == 'Pass' else "❌"
        rule = result['rule_details']['Extracted Rule']

        # Use an expander for each requirement
        with st.expander(f"{status_icon} **{result['status']}:** {rule}"):
            # Display detailed information inside the expander
            st.info(f"**Explanation:** {result['explanation']}")

            # Use columns for a neat layout of score and best match
            detail_col1, detail_col2 = st.columns([1, 3])

            with detail_col1:
                st.metric(label="Similarity Score", value=f"{result['similarity_score']:.2f}")

            with detail_col2:
                st.success(f"**Best Match from CV:**\n\n> {result['best_match']}")

