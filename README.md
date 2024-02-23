# Chat with Mutilple PDF Files Application

## Overview

This project introduces a conversational interface designed to interact with content extracted from multiple PDF files. By leveraging a chatbot framework, users can upload several PDF documents and ask questions, receiving answers based on the contents of those documents. Additionally, the system includes a demonstration of user verification through a SQL database, showcasing a complete user management system.

The application is capable of providing reference texts from the uploaded documents to substantiate its responses, enhancing the user experience by offering direct insights from the source material.

Deployed on Streamlit, this project exemplifies a practical application of natural language processing and document handling within a web application.


## OpenAI API Key Management and Usage

### Understanding OpenAI API Costs

The OpenAI API provides new users with a $18 credit, allowing for initial use without incurring costs. Once this credit is depleted, users will be switched to a pay-as-you-go model. It is crucial for users to monitor their usage to manage expenses effectively. Detailed pricing can be found on the OpenAI pricing page.

### Obtaining Your OpenAI API Key

To use the OpenAI API, an API key is required:

1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys) to obtain or create your API key.
2. If you do not have an account, sign up and navigate to the API keys section.
3. Create a new API key if you haven't already.

### Important Considerations for Hosting

- **Security Warning:** The OpenAI API key is unable to be hosted in public repositories (e.g., GitHub) as it can lead to unauthorized use and financial charges. OpenAI automatically disables exposed keys to prevent misuse.
- **Local Deployment:** It's recommended to run the application locally to keep your API key secure.


## Features

- **Interactive Chat Interface:** Ask questions and receive answers that reference the contents of uploaded PDF files.
- **Multi-Document Support:** Upload and process multiple PDF files simultaneously for comprehensive query support.
- **Secure User Verification:** Demonstrates user authentication and management through a SQL database.
- **Contextual Answers with References:** Provides reference excerpts directly from the uploaded documents to back up the chatbot's responses.

## Getting Started

### Prerequisites
- pip

### Installation

1. Clone the repository:
git clone https://github.com/<your-username>/final-chat-with-pdf.git

2. Navigate to the project directory and install the required dependencies:
cd final-chat-with-pdf
pip install -r requirements.txt

3. Set up your OpenAI API key in a `.env` file within the project directory:
OPENAI_API_KEY=your_api_key_here (OPENAI_API_KEY=sk-.....)

### Running the Application

Launch the application by running:
streamlit run app.py

## Usage

1. **Sign Up/Login:** Start by signing up for an account or logging in.
2. **Upload Documents:** Click on "Upload your PDFs" to select and process your documents.
3. **Query:** Use the chat interface to ask questions and receive information based on the content of your uploaded documents.

## Planned Improvements

1. **Reference Text Filtering:** 
- ***Current Limitation***: The application currently provides reference texts from uploaded documents even when the responses are not directly related to the user's query. This can lead to situations where users are presented with information that, while related, may not be directly relevant to their question.
- ***Proposed Enhancement***: Implement a filtering mechanism to restrict the provision of reference texts strictly to those directly relevant to the user's query. Currently, I used a UI element like a dropdown (expander) to allow users to choose when to view these references, thereby not cluttering the interface with potentially irrelevant information.
2. **Advanced Information Retrieval:** 
- ***Current Limitation***:The system is capable of retrieving reference text information from the uploaded documents but does not offer show specific source files or page numbers. This limits the user's ability to locate the exact source of the information within the documents.
- ***Proposed Enhancement***: Expand the retrieval capabilities to include options for users to select specific embeddings for extracting information. Utilize the retriever.get_relevant_documents(query) function to pinpoint and retrieve detailed document metadata, such as the source file and page number. Consider the implementation challenges within Streamlit and explore ways to integrate these advanced features into the user interface.
3. **User Interaction Enhancements:** 
- ***Current Limitation***: The application requires users to follow a sequence of actions: uploading and processing files before initiating any queries. This workflow can confuse new users or those who may inadvertently attempt to query before completing the necessary preliminary steps.
- ***Proposed Enhancement***: Develop a more intuitive and flexible user interaction flow that allows for non-linear actions. For example, enable the chat interface immediately upon login and guide users through the document upload and processing steps as needed.
4. **Secure API Key Management:** 
- ***Current Limitation***: Deploying the application on public platforms like GitHub or Streamlit sharing poses a challenge, especially concerning the secure management of the OpenAI API key. Exposing sensitive keys in public repositories or applications can lead to security risks and unauthorized usage.
- ***Proposed Enhancement***:Explore and implement secure methods for API key management in public deployments. Consider utilizing environment variables on deployment platforms that support them, or investigate services like HashiCorp Vault for API key encryption and access control. Provide clear documentation and guidelines for users on how to securely configure their API keys when deploying their instances of the application.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.