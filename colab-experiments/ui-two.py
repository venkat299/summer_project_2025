import streamlit as st
import json
import os

# --- DATA LOADING ---
# This section handles loading the data from local JSON files.
# For this code to work, you must create the following files in the same
# directory as this script:
# 1. document_pairs.json
# 2. all_results.json
# 3. all_results2.json

# --- Example: document_pairs.json ---
# [
#     {
#         "job_description": "...",
#         "candidate_cv": "..."
#     },
#     {
#         "job_description": "...",
#         "candidate_cv": "..."
#     }
# ]

# --- Example: all_results.json / all_results2.json ---
# [
#     [
#         [
#             { "rule_details": {...}, "status": "Pass", ... },
#             { "rule_details": {...}, "status": "Fail", ... }
#         ],
#         { "compliance_rate": 0.50, "avg_similarity": 0.8, ... }
#     ]
# ]


@st.cache_data
def load_json_file(file_path):
    """Loads a JSON file from the given path with error handling."""
    if not os.path.exists(file_path):
        st.error(f"Error: File not found at `{file_path}`. Please make sure the file exists.")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.error(f"Error: Could not decode JSON from `{file_path}`. Please check the file for formatting errors.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while reading `{file_path}`: {e}")
        return None

# --- STREAMLIT APP ---

st.set_page_config(layout="wide", page_title="Compliance Validation Visualizer")

# --- Sidebar for Selection and Metrics ---
st.sidebar.title("📋 Compliance Dashboard")

# Load the document pairs data once.
document_pairs = load_json_file('document_pairs.json')

# Add a selector for the results file
result_file_options = {
    "Results 1": "all_results.json",
    "Results 2": "all_results2.json"
}
selected_result_key = st.sidebar.selectbox(
    "Select a Result Set",
    options=list(result_file_options.keys()),
    help="Choose which set of validation results you want to analyze."
)

# Load the selected results data
selected_result_file = result_file_options[selected_result_key]
all_results = load_json_file(selected_result_file)


# Proceed only if data was loaded successfully
if all_results and document_pairs:
    # 1. Document Pair Selection
    pair_options = [f"Document Pair {i+1}" for i in range(len(document_pairs))]
    if not pair_options:
        st.warning("No document pairs found in the data.")
    else:
        selected_pair_str = st.sidebar.selectbox(
            "Select a Document Pair to Analyze",
            options=pair_options,
            help="Choose the document set you want to review."
        )

        # Get the index of the selected pair
        selected_index = pair_options.index(selected_pair_str)

        # Check if the selected index is valid for the results
        if selected_index < len(all_results):
            # Retrieve the specific data for the selected pair
            selected_results, selected_metrics = all_results[selected_index]
            selected_docs = document_pairs[selected_index]

            # 5. Overall Metrics Display
            st.sidebar.header("📊 Overall Metrics")

            # Dynamically calculate passed and failed rules for accuracy
            passed_count = sum(1 for r in selected_results if r.get('status') == 'Pass')
            failed_count = sum(1 for r in selected_results if r.get('status') == 'Fail')

            # Use columns for a cleaner layout of metrics
            m_col1, m_col2 = st.sidebar.columns(2)
            m_col1.metric(
                label="Compliance Rate",
                value=f"{selected_metrics.get('compliance_rate', 0):.0%}",
                help="Percentage of requirements met by the candidate's CV."
            )
            m_col2.metric(
                label="Avg. Similarity",
                value=f"{selected_metrics.get('avg_similarity', 0):.2f}",
                help="The average similarity score across all requirements."
            )

            # Display the dynamically calculated counts
            st.sidebar.write(f"**Passed Rules:** {passed_count}")
            st.sidebar.write(f"**Failed Rules:** {failed_count}")


            # --- Main Panel for Details ---
            st.title(f"Analysis for {selected_pair_str} (from {selected_result_file})")
            st.markdown("---")


            # 2. Display Document Texts
            st.header("📄 Original Documents")
            doc_col1, doc_col2 = st.columns(2)

            with doc_col1:
                st.subheader("Job Description")
                st.text_area(
                    "Job Description Text",
                    selected_docs.get('job_description', 'Not available.'),
                    height=300,
                    label_visibility="collapsed"
                )

            with doc_col2:
                st.subheader("Candidate CV")
                st.text_area(
                    "Candidate CV Text",
                    selected_docs.get('candidate_cv', 'Not available.'),
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
                    status_icon = "✅" if result.get('status') == 'Pass' else "❌"
                    rule = ""
                    if result.get('rule_details', None):
                        rule = result.get('rule_details', {}).get('Extracted Rule', 'Rule not specified.')
                    else:
                        rule = result.get('requirement', 'Rule not specified.')

                    # Use an expander for each requirement
                    with st.expander(f"{status_icon} **{result.get('status', 'N/A')}:** {rule}"):
                        # Display detailed information inside the expander
                        st.info(f"**Explanation:** {result.get('explanation', 'No explanation provided.')}")

                        # Use columns for a neat layout of score and best match
                        detail_col1, detail_col2 = st.columns([1, 3])

                        with detail_col1:
                            st.metric(label="Similarity Score", value=f"{result.get('similarity_score', 0):.2f}")

                        with detail_col2:
                            st.success(f"**Best Match from CV:**\n\n> {result.get('best_match', 'No match found.')}")
        else:
            st.error(f"Data for 'Document Pair {selected_index + 1}' not found in `{selected_result_file}`.")
else:
    st.info("Please create the required JSON data files to begin analysis.")

